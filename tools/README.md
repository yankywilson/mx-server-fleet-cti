# Tools

Small, dependency-free Python 3 tools used in this investigation. Each one
implements a technique documented in [`../methodology/`](../methodology/).
Run `python3 -m unittest discover -s tests` from the repository root to
check them against the case values.

| Tool | What it does | Technique |
|---|---|---|
| `caddy_etag.py` | Decodes a Caddy ETag into file write time (ns) and size | [Caddy ETag forensics](../methodology/caddy-etag-forensics.md) |
| `cf_soa_decode.py` | Turns Cloudflare SOA serials into owner edit times | [SOA serial decoding](../methodology/cloudflare-soa-serial-decoding.md) |
| `kafka_serial.py` | Converts serials hex ↔ decimal; lists gaps in a sequence | [Certificate serial pivot](../methodology/certificate-serial-sequence-pivot.md) |
| `irr_batch_cluster.py` | Groups IRR route/route6 objects into lease-order batches | [IRR batch clustering](../methodology/irr-route-object-batch-clustering.md) |
| `ssh_front_map.py` | Maps front IPs to the physical server by SSH host key | [SSH host-key mapping](../methodology/ssh-hostkey-front-to-server-mapping.md) |
| `pattern_of_life.py` | Working-hours test over operator timestamps | [Pattern of life](../docs/pattern-of-life.md) |

All tools read local files or arguments only. None of them contacts the
infrastructure in this report.
