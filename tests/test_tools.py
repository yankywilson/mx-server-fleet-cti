"""Regression tests: each tool must reproduce the values reported in this case."""
import datetime as dt
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import caddy_etag  # noqa: E402
import cf_soa_decode  # noqa: E402
import irr_batch_cluster  # noqa: E402
import kafka_serial  # noqa: E402
import pattern_of_life  # noqa: E402
import ssh_front_map  # noqa: E402

DATA = os.path.join(ROOT, "data")


class CaddyEtag(unittest.TestCase):
    def test_reedjordan_page(self):
        (ts, size, _), = caddy_etag.decode('"dkb1fqjbnd35ce"', 446)
        self.assertEqual(size, 446)
        self.assertEqual(ts.strftime("%Y-%m-%d %H:%M:%S"), "2026-07-29 12:02:12")

    def test_broker_page_is_ten_seconds_later(self):
        (a, _, _), = caddy_etag.decode("dkb1fqjbnd35ce", 446)
        (b, _, _), = caddy_etag.decode("dkb1fv87lqycce", 446)
        self.assertAlmostEqual((b - a).total_seconds(), 10.21, places=1)

    def test_weak_etag_prefix(self):
        self.assertTrue(caddy_etag.decode('W/"dkb1fqjbnd35ce"', 446))


class SoaSerial(unittest.TestCase):
    def test_reedjordan_serial(self):
        self.assertEqual(cf_soa_decode.decode(2417968479),
                         dt.datetime(2026, 10, 20, 7, 53, 36, tzinfo=dt.timezone.utc))


class KafkaSerial(unittest.TestCase):
    def test_hex_to_decimal(self):
        n = kafka_serial.to_int("17:94:5f:83:2a:ea:9b:90:27:ed:e5:c1:cb:9e:f5:32:ef:e6:b7:51")
        self.assertEqual(n, 134615618319530153631244838655347924586237179729)

    def test_decimal_round_trip(self):
        n = kafka_serial.to_int("134615618319530153631244838655347924586237179729")
        self.assertTrue(kafka_serial.to_hex(n).endswith("b7:51"))

    def test_gap_is_b74f(self):
        base = "17945f832aea9b9027ede5c1cb9ef532efe6b7"
        missing = kafka_serial.gaps([kafka_serial.to_int(base + x) for x in ("4e", "50", "51")])
        self.assertEqual([kafka_serial.to_hex(m, False)[-2:] for m in missing], ["4f"])


class IrrBatch(unittest.TestCase):
    def test_one_batch_of_19(self):
        rows = irr_batch_cluster.load(os.path.join(DATA, "irr_route6_2602-fad4.csv"))
        batches = irr_batch_cluster.cluster(rows, window=60)
        big = max(batches, key=len)
        self.assertEqual(len(big), 19)
        self.assertEqual(big[0]["prefix"], "2602:fad4:17::/48")
        self.assertEqual(big[-1]["prefix"], "2602:fad4:29::/48")
        self.assertLessEqual((big[-1]["created"] - big[0]["created"]).total_seconds(), 13)


class SshMap(unittest.TestCase):
    def test_seven_servers_mapped(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ssh_front_map.main([os.path.join(DATA, "ssh_hostkey_observations.csv"),
                                "--native", "54.36.0.0/16,79.137.64.0/18"])
        out = buf.getvalue()
        self.assertEqual(out.count("server(native):"), 7)
        self.assertNotIn("NOT FOUND", out)
        self.assertIn("54.36.175.25", out)
        self.assertIn("194.104.138.0/24", out)


class PatternOfLife(unittest.TestCase):
    def test_no_timezone_fits(self):
        t = pattern_of_life.load(os.path.join(DATA, "operator_event_times_utc.txt"))
        best = max(pattern_of_life.score(t, off)[0] / len(t) for off in range(-11, 13))
        self.assertLess(best, 0.70)  # no offset puts 70% of events in a 12-hour day


if __name__ == "__main__":
    unittest.main()
