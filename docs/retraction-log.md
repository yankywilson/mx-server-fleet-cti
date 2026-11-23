# Retraction log

Claims I made during the investigation that were wrong or overstated, and what replaced them. Kept public on purpose: a correction is a finding.

| # | Original claim | Corrected to | What changed it |
|---|---|---|---|
| R1 | The fleet moved to H4Y after the BYOIP blocks went dark on 2026-11-12. | The fleet has been on H4Y 216.158.220.0/24 since 2026-06-03/04. H4Y ran in parallel the whole time. | Passive DNS PTR history. |
| R2 | The operator is likely US-based. | Undetermined. DNS edits peak at 07–12 UTC, which is night in the US. | Edit-time decoding across 79 edits. |
| R3 | OVH shut down the eight BYOIP blocks. | The blocks went dark on 2026-11-12. Cause unknown. | The operator was editing DNS hours before. No provider statement exists. |
| R4 | The node at 89.40.83.56 moved to 79.137.70.8, a freshly deployed server. | Same server. 89.40.83.0/24 was routed onto `ns3066510` (79.137.70.8) through BYOIP. | Kafka certificate CN=79.137.70.8 served on 89.40.83.56 on 2026-10-27. |
| R5 | Port 443 "Ncat http proxy" proves an HTTP proxy service on fleet nodes. | Very likely a Shodan mislabel of the Go/Caddy TLS listener. | Go's `net/http` answers plain HTTP on a TLS port with exactly `HTTP/1.0 400 Bad Request`. Shodan gives the same label to unrelated Caddy hosts. |
| R6 | The BYOIP /24s were withdrawn from routing on 2026-11-12. | Still announced by AS16276 on 2026-11-20. Only the fleet's services stopped. | Routing snapshot, 2026-11-20. |
| R7 | The H4Y nodes present the same certificate, covering the same domains, as the OVH nodes. | Same certificate format (`O=mx_server`). Different certificate: `CN=agilehawk.gourmethazelnuts.com`, 39 domains. | Per-IP certificate review of all 529 H4Y and Tier.Net hosts. |
| R8 | Sandbox captures show the brokers open on 80 and 443. | Those answers came from the sandbox's egress proxy. Only 9092/9093 are confirmed broker ports in that capture. | TTL 62 vs 48/49, MSS 1380 vs 1460, RTT ~42 ms vs ~80 ms between the two port groups. |
| R9 | The broker JA3S is a fleet fingerprint. | Not usable. The same JA3S appears on unrelated Kafka servers. | Comparison against unrelated Java TLS 1.3 hosts. |

## Judgment changes (v2.0)

A judgment that moves is not an error. It is recorded so readers can see what moved it.

| Judgment | v1.0 | v2.0 | What moved it |
|---|---|---|---|
| The fleet carries password-spray traffic | Not assessed | **Likely** (moderate) | A second fleet address in the telemetry, tied by SSH key to a different server |
| The spray operator and the fleet operator are the same | Unlikely | **Roughly even chance** (low) | One of the two servers is a Kafka broker, a core asset, not a rented exit |
| The brokers control the spray | Not assessed | **Roughly even chance** (low) | Broker in telemetry; no traffic content available |
| The brokers are the single "main" asset | Not assessed | **Unlikely** (low) | A worker also sent spray traffic; control may sit outside the fleet |
| Operator time zone (R2 detail) | DNS edits peak 07–12 UTC | Peak 20–22 UTC; no offset gives a working day | 86 events instead of a smaller set. Conclusion unchanged: undetermined |

