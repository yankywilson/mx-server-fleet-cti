# Closed leads and null results (v2.0)

A lead that goes nowhere is still a result. It saves the next analyst the same work. Each lead below was tested and closed.

| # | Lead | Test | Result | Tag |
|---|---|---|---|---|
| L1 | A second "Kafka Cluster CA" cluster on Russian-hosted servers might be this fleet, and a nationality lead | Compare AKI, subject organization, hostnames and certificate profile | Different CA key, different organization name, different hostname scheme. Unrelated | EXCLUDED |
| L2 | Earlier reverse-DNS names on the broker 54.36.174.217 might identify the operator | Passive DNS PTR history | Earlier tenants from 2019–2023 belong to unrelated organizations. The current name `tendersage.straightmembers.com` appeared on 2026-07-25 | EXCLUDED |
| L3 | The broker's JA3S might fingerprint the fleet | Compare JA3S `15af977ce25de452b96affa2addb1036` against unrelated Kafka servers | Same JA3S on unrelated deployments. Java TLS 1.3 defaults. Not usable | EXCLUDED |
| L4 | Sandbox captures showed the brokers answering on 80/443 with odd TCP values | Compare TTL, MSS, window and RTT against the real 9092 session in the same capture | 80/443 answers came from the sandbox's own egress proxy (TTL 62, MSS 1380, window 64860, RTT ~42 ms). The real broker shows TTL 48/49, MSS 1460, RTT ~80 ms. Artifact | EXCLUDED |
| L5 | The missing Kafka serial `…b7:4f` might be a fourth, hidden broker | Shodan, Censys and FOFA serial searches | No host presents it. Null result | NOVEL (null) |
| L6 | The broker might require client certificates (mTLS), which would suggest closed tooling | Decode the TLS 1.3 handshake | No CertificateRequest. Anyone can complete TLS | NOVEL |
| L7 | A fleet domain whose apex resolves to Cloudflare might expose an origin | DNS history | The apex sits behind Cloudflare. **Do not block those Cloudflare IPs**: they serve many unrelated sites | EXCLUDED |
| L8 | Port 443 "Ncat http proxy" might show a proxy service | Banner and server software review | Shodan mislabel of the Go/Caddy TLS listener (R5) | EXCLUDED |
| L9 | Operator activity times might show a nationality | 86-event working-hours test | No working day in any time zone. Attribution not supported | NOVEL (null) |
| L10 | The spray client's control server might be visible from the target side | Review of all spray telemetry fields | The client talks only to Microsoft, through exits. Control server not observable | NOVEL (null) |

## Lesson from L4

Public sandboxes put their own proxy in front of the analysed traffic. Ports that the proxy handles (often 80 and 443) show the proxy's TCP stack, not the target's. Compare TTL and MSS between ports before you call a port "open on the target". Method: [`../methodology/sandbox-egress-artifacts.md`](../methodology/sandbox-egress-artifacts.md).

## Boundary kept

No test in this list connected to the operator's Kafka service with a Kafka client, logged in to any service, or sent mail. Everything is passive data, public scanner data or a sandbox's own capture.
