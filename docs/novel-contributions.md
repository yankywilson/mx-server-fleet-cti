# Novel contributions

"NOVEL" in this repository means first reported here, for this fleet. Every item below is reproducible from public data using the steps in [`../methodology/`](../methodology/).

## Summary

| # | Contribution | Type | Why it matters to defenders |
|---|---|---|---|
| N1 | One OVH account behind eight IPXO-leased /24s, proven by a shared BYOIP token | Finding + reusable technique | Collapses eight "unrelated" netblocks with different registry holders into one actor account |
| N2 | Proof that a leased BYOIP block was routed onto a specific dedicated server | Finding + reusable technique | Links rented IP space to the operator's own hardware, which is the real takedown target |
| N3 | DNS edit times recovered from Cloudflare SOA serials (±1 min) | Reusable technique | Adds timestamps to infrastructure that otherwise has none, with no account access |
| N4 | A private Kafka CA key identifier as a durable fleet fingerprint | Finding | Survives IP rotation, domain rotation and certificate regeneration |
| N5 | A Shodan false positive: "Ncat http proxy" on Go/Caddy TLS listeners | Analyst correction | Stops other hunters from inferring proxy services from a mislabel |
| N6 | Full map of a 2,463-host cross-provider fleet with four certificate families | Finding | Gives defenders a complete, current blocklist and a hunting pattern |
| N7 | SSH host-key map from 8 leased /24s to 8 OVH servers | Finding + reusable technique | Gives the durable block targets behind rotating fronts |
| N8 | IRR route-object batch clustering of an IPv6 lease order | Reusable technique | Turns "many networks" into one lessee's order |
| N9 | Caddy ETag decoding to nanosecond file-write times | Reusable technique | Proves one scripted deployment across hosts |
| N10 | Certificate serial-sequence analysis of a private CA | Finding + reusable technique | Dates a CA run to the second; exposes missing members |
| N11 | Web body-hash sweep that found new fleet nodes | Finding | Extends the blocklist past the certificate pivot |
| N12 | Sandbox egress-proxy artifact test (TTL/MSS/RTT) | Analyst correction + technique | Stops false "open port" claims from sandbox captures |
| N13 | Pattern-of-life null result on 86 operator events | Null result | Shows why nationality is not supported |

## N1. BYOIP token clustering

- **Observation.** One 128-character OVH BYOIP token appears in the RIPE `descr` field of eight /24s held by three different leasing identities.
- **Inference.** OVH binds the token to the importing account, so all eight ranges were imported by one OVH customer.
- **Timing.** The token was written to all eight objects within 21 minutes on 2026-07-17. The ranges were announced the next day.
- **Reuse.** Any BYOIP range on OVH can be clustered this way. Search the token in registry full text and in version history.

## N2. BYOIP-to-server routing proof

- **Observation.** `89.40.83.56:9092`, a leased BYOIP address, served a Kafka certificate issued to `CN=79.137.70.8 / SAN IP:79.137.70.8`, the main IP of OVH server `ns3066510`.
- **Inference.** The imported range was delivered as additional IPs on that server. The leased block and the native server are one machine.
- **Reuse.** Look for a certificate CN or SAN naming a different IP than the one serving it. That mismatch reveals the host behind added IPs.

## N3. Cloudflare SOA serial decoding

- **Formula.** `edit_time_utc = serial − 625485663`, read as Unix time. Calibrated to about ±1 minute against independently timed changes.
- **Result.** 79 owner edits decoded across five zones. These include cross-family bursts seconds apart, and the operator's last edits before the BYOIP blocks went dark.
- **Reuse.** Works on any passive DNS SOA history for zones that behave this way. Validate on a zone you control first.

## N4. Kafka CA fingerprint

- **Observation.** Fleet brokers use a private CA named `Kafka-Cluster-CA` with AKI `AA:77:1C:B8:E5:D7:A5:98:2E:4F:FF:17:23:13:80:55:5C:65:50:3A`.
- **Why it's durable.** Operators rotate IPs and domains. Re-issuing a private CA means redeploying every broker.

## N5. Shodan "Ncat http proxy" false positive

- **Observation.** Shodan labels port 443 on fleet nodes "Ncat http proxy" with banner `HTTP/1.0 400 Bad Request`. The same label and hash appear on unrelated Caddy servers.
- **Cause.** Go's `net/http` writes exactly `HTTP/1.0 400 Bad Request` when plain HTTP reaches a TLS listener. Ncat's proxy returns the same first line, so the signature collides.
- **Lesson.** I first read this as a proxy service and retracted it (R5). Verify a scanner's service label against the server software before building a theory on it.

## N6. Fleet map

- 2,463 hosts across OVH (BYOIP and native), H4Y, Tier.Net, Hetzner and US-hosted single nodes.
- Four certificate families, 93 domains, about 2,515 hostnames.
- Per-IP evidence: [`../iocs/fleet-ips.csv`](../iocs/fleet-ips.csv).

## N7. SSH host-key front-to-server map

- **Observation.** Front addresses in 7 of 8 /24s present the same SSH host key as one OVH server's native IP. Two unique OpenSSH patch levels (13.18, 13.19) confirm two of the pairs.
- **Inference.** Each /24 is routed onto one dedicated server. The servers, not the /24s, are the durable targets.
- **Reuse.** Any BYOIP or additional-IP setup. See [`../methodology/ssh-hostkey-front-to-server-mapping.md`](../methodology/ssh-hostkey-front-to-server-mapping.md).

## N8. IRR batch clustering

- **Observation.** The nine IPv6 /48s seen as spray exits all fall in a 19-object batch created in 13 seconds on 2025-12-22.
- **Reuse.** IRR `created` timestamps reveal lease orders. See [`../methodology/irr-route-object-batch-clustering.md`](../methodology/irr-route-object-batch-clustering.md).

## N9. Caddy ETag forensics

- **Observation.** Two hosts wrote the same 446-byte page 10.2 s apart.
- **Reuse.** Caddy's ETag is base36(mtime ns) + base36(size). See [`../methodology/caddy-etag-forensics.md`](../methodology/caddy-etag-forensics.md).

## N10. Certificate serial sequence

- **Observation.** Three broker serials end `…4e`, `…50`, `…51`, minted over 11 seconds. `…4f` is missing.
- **Reuse.** See [`../methodology/certificate-serial-sequence-pivot.md`](../methodology/certificate-serial-sequence-pivot.md).

## N11. Web body-hash sweep

- **Observation.** The 446-byte Caddy page sits on 246 hosts and 50 apex domains. New members include `reedjordan.com`.
- **Reuse.** See [`../methodology/web-body-hash-sweep.md`](../methodology/web-body-hash-sweep.md).

## N12. Sandbox egress artifacts

- **Observation.** In a public sandbox capture, 80/443 answered with the sandbox proxy's TCP stack, not the broker's.
- **Reuse.** See [`../methodology/sandbox-egress-artifacts.md`](../methodology/sandbox-egress-artifacts.md).

## N13. Pattern-of-life null result

- **Observation.** Best working-day fit 64%; 28% of events on weekends.
- **Meaning.** No time zone. See [`pattern-of-life.md`](pattern-of-life.md).

## Tradecraft documented

| Technique | Evidence |
|---|---|
| IP leasing to hide ownership | Three leasing identities in front of one OVH account |
| BYOIP to borrow a reputable network (AS16276) | Eight leased ranges announced by OVH |
| Snowshoe distribution | 2,461 sending IPs, low volume per IP, generated hostnames |
| Aged and expired domains | Domains created in 1999, 2004 and 2005 |
| Typosquats of real brands | `scraigslist.com`, `wwwpricechopper.com`, `pittsburghpostgazete.com` |
| Microsoft 365 tenants on aged domains | `MS=` verification records, October–December 2025 |
| Scripted DNS management | Multi-zone edits seconds apart |
| Scripted server deployment | Same page written on two hosts 10.2 s apart; CA run of 11 s |
| Leased IPv6 exits on a residential ASN | 19 × /48 lease batch announced by AS6079 |

## Analytic standard

- ICD-203 likelihood language, with confidence stated separately.
- Every source tagged NOVEL, CORROBORATED, PUBLISHED or EXCLUDED.
- A public [retraction log](retraction-log.md) with nine corrections and a judgment-change record.
- [Closed leads](closed-leads.md) and null results reported as findings.
- Attribution withheld where the evidence does not support it.
