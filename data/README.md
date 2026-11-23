# Data

Raw observations behind the findings. Every file is public-source data or a value derived from it. Nothing here identifies a victim.

| File | Rows | What it holds | Used by |
|---|---|---|---|
| `ssh_hostkey_observations.csv` | 14 | IP, SSH host-key fingerprint, front or native | `tools/ssh_front_map.py`, `docs/server-map.md` |
| `kafka_broker_certs.csv` | 4 | Broker certificate serials (hex and decimal), CN, notBefore, AKI; the missing serial | `tools/kafka_serial.py`, `docs/kafka-backend.md` |
| `caddy_etag_observations.csv` | 2 | Host, IP, ETag, Content-Length, Last-Modified, source | `tools/caddy_etag.py` |
| `irr_route6_2602-fad4.csv` | 31 | IRR route6 objects: prefix, origin, maintainer, created | `tools/irr_batch_cluster.py`, `docs/spray-infrastructure.md` |
| `cloudflare_soa_edits.csv` | 77 | Decoded DNS edit times per zone | `tools/cf_soa_decode.py`, `docs/timeline.md` |
| `operator_event_times_utc.txt` | 86 | All timestamped operator actions (DNS edits + 9 others) | `tools/pattern_of_life.py`, `docs/pattern-of-life.md` |

## Sources

Shodan, Censys, FOFA, Validin, RIPE and ARIN registry data, RADB and ARIN IRR, RDAP, passive DNS, and public sandbox captures.

## Reproduce

```bash
python3 -m unittest discover -s tests
```
