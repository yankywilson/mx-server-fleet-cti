# FOFA queries

Field names were checked against FOFA's search syntax page. `=` is a contains match. `==` is an exact match. `cert.sn` takes the **decimal** serial (confirmed in this case).

| # | Purpose | Query |
|---|---|---|
| F1 | Fleet SMTP certificate format | `cert.subject.org="mx_server"` |
| F2 | The fleet's private Kafka CA (then check the AKI) | `cert.issuer.cn="Kafka-Cluster-CA"` |
| F3 | One broker certificate by serial (…b7:51) | `cert.sn="134615618319530153631244838655347924586237179729"` |
| F4 | The missing serial …b7:4f | `cert.sn="134615618319530153631244838655347924586237179727"` |
| F5 | The fleet's 446-byte Caddy page | `title=="Server" && server="Caddy"` |
| F6 | Same page by header hash | `header_hash="707484123"` |
| F7 | One front /24 with the Caddy page | `ip="194.104.138.0/24" && title=="Server"` |
| F8 | The fleet SMTP dialogue | `banner="501 5.5.4 Invalid domain name"` |
| F9 | Fleet hosts on OVH | `asn="16276" && cert.subject.org="mx_server"` |
| F10 | All services on one server | `ip="54.36.174.217"` |

## Validation

A FOFA hit is a fleet member only with a second feature: `O=mx_server`, the Kafka AKI, the SMTP dialogue, or a fleet domain. F5 and F8 alone are medium strength.

## Results recorded

| Query | Result |
|---|---|
| F4 | 0 hosts (null result, 2026-11-23) |
| F2 | Several "Kafka-Cluster-CA" clusters; only AKI `AA:77:1C…50:3A` is this fleet |
