#!/usr/bin/env python3
"""Decode Cloudflare-hosted zone SOA serials into owner edit times (UTC).

Observed on the zones in this case: edit_time = serial - 625485663, read as
Unix time, accurate to about +/- 1 minute. Validate on a zone you control
before relying on it for a new provider or a new time period.

Usage:
    python3 cf_soa_decode.py 2417968479
    python3 cf_soa_decode.py --csv soa_history.csv   (columns: domain,serial)
"""
import argparse
import csv
import datetime as dt

OFFSET = 625485663


def decode(serial, offset=OFFSET):
    return dt.datetime.fromtimestamp(int(serial) - offset, dt.timezone.utc)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("serials", nargs="*")
    p.add_argument("--csv", help="CSV with columns domain,serial")
    p.add_argument("--offset", type=int, default=OFFSET)
    a = p.parse_args(argv)
    rows = [("", s) for s in a.serials]
    if a.csv:
        with open(a.csv, newline="") as f:
            rows += [(r["domain"], r["serial"]) for r in csv.DictReader(f)]
    out = sorted((decode(s, a.offset), d, s) for d, s in rows)
    for t, d, s in out:
        print(f"{t.isoformat()}\t{d}\t{s}")


if __name__ == "__main__":
    main()
