# Technical analysis

Source tags: **NOVEL** (first reported here), **CORROBORATED** (two or more independent sources), **PUBLISHED** (from prior public work), **EXCLUDED** (checked and rejected).

## 1. Scope

This is a fleet of templated SMTP servers, about **2,461 hosts**, observed in scan data between 2026-10-21 and 2026-11-20. It spans **OVH** (BYOIP and native), **H4Y Technologies**, **Tier.Net** and **Hetzner**. It uses **92 domains** and about **2,515 generated hostnames**.

## 2. Fleet fingerprint (NOVEL)

| Layer | Observation |
|---|---|
| SMTP (25/tcp) | Banner `220 <adjective><noun>.<domain> ESMTP`. Capabilities: STARTTLS, 8BITMIME, ENHANCEDSTATUSCODES, `SIZE 10485760`. |
| SMTP TLS | Self-signed ECDSA P-256 certificate, `O=mx_server`. CN is one of four values (section 3). STARTTLS key exchange includes X25519MLKEM768, consistent with Go 1.24 or later. |
| Primary IP | Bare EHLO `localhost.localdomain` on a server's main IP, which has no mail identity. |
| HTTP (80/tcp) | Caddy. `308 Permanent Redirect` to `https://<IP>/`. |
| HTTPS (443/tcp) | Go/Caddy TLS listener. Answers a plain-HTTP probe with `HTTP/1.0 400 Bad Request`. Shodan labels this "Ncat http proxy". That label is wrong (see the retraction log). |
| SSH (22/tcp) | `OpenSSH_9.6p1 Ubuntu-3ubuntu13.19`. Host keys differ per host. |
| Kafka (9092/9093) | Broker certificates from private CA `CN=Kafka-Cluster-CA`, AKI `AA:77:1C:B8:E5:D7:A5:98:2E:4F:FF:17:23:13:80:55:5C:65:50:3A`. |
| DNS (53) | Authoritative server that refuses outside queries. |
| High ports | On some nodes, about 70 sequential ports in the 12xxx–13xxx range answer `HTTP/1.1 400 Bad Request`. Purpose unexplained. A per-IP proxy gateway is possible, but unconfirmed. |

## 3. Certificate families

| Certificate CN (all `O=mx_server`) | Hosts | Domains in SAN | Where |
|---|---|---|---|
| `adamsethfox.com` | 1,660 | 46 | OVH BYOIP, OVH native |
| `agilehawk.gourmethazelnuts.com` | 529 | 39 | H4Y, Tier.Net |
| `agilebamboo.phoenixseniornews.com` | 242 | 44 | OVH |
| `alertbear.devriendenvanjacob.com` | 30 | 3 | Hetzner |

Example: the `adamsethfox.com` certificate seen on 2026-10-27 was valid from 2026-07-29 10:38:06 UTC to 2036-07-26 11:38:06 UTC. That is exactly 3,650 days, with a 1-hour backdate. Its SAN lists 45 wildcard domains, the apex names, about 250 hostnames, and `127.0.0.1` and `::1`. Hostname sets change between certificate generations. Domain sets mostly persist.

## 4. Address acquisition

### 4.1 IPXO leasing into OVH BYOIP (NOVEL)

Eight /24s were leased through IPXO (maintainer `netutils-mnt`, Internet Utilities Europe and Asia Ltd) and imported into OVH:

| Block | Registered holder (RIPE) |
|---|---|
| 31.77.120.0/24, 151.242.139.0/24, 212.69.8.0/24, 222.167.237.0/24 | "Company 6a53796d6yVdFmVm", ORG-PC1890-RIPE, country US, created 2026-07-15T17:45:43Z |
| 194.104.138.0/24 | Aiti Spektr ltd |
| 89.40.83.0/24, 77.67.28.0/24, 94.158.184.0/24 | Internet Utilities Europe and Asia Ltd |

All eight carry this OVH BYOIP validation token in `descr`:

```
1a3e6beb59b5181644fa95739c6f45c8fe51b67cb21c45f2ee2b0caadc5554bf440eaace09f2dfecece6b1c2e877039ddf11b8cebb58d09555eaa90b8f6df620
```

RIPE version history shows the token added at 14:32:17, 14:33:19, 14:34:11 and 14:53:17 UTC on 2026-07-17. IPXO's own guide says this field carries the certificate that the OVH customer generates (PUBLISHED). **Assessment:** the eight blocks very likely belong to one OVH account (moderate-high confidence).

### 4.2 BYOIP routed to a native server (NOVEL)

OVH delivers imported /24s as additional IPs attached to the importing customer's server (PUBLISHED, OVH BYOIP documentation). On 2026-10-27, `89.40.83.56:9092` served:

- Subject `CN=79.137.70.8`, SAN `IP:79.137.70.8`
- Issuer `CN=Kafka-Cluster-CA`, NotBefore 2026-08-17 15:37:11 UTC
- AKI `AA:77:1C:B8:E5:D7:A5:98:2E:4F:FF:17:23:13:80:55:5C:65:50:3A`

`79.137.70.8` is the main IP of OVH server `ns3066510`. **Assessment:** 89.40.83.0/24 was very likely routed onto `ns3066510` (moderate-high confidence). **Alternative:** the Kafka keystore was copied to a second server. Unlikely, because brokers normally get their own certificates.

### 4.3 Rented hosting

- **H4Y Technologies:** 216.158.220.0/24 (245 hosts, PTRs present since 2026-06-03/04) and 206.232.102.0/24 (235 hosts, H4Y reallocation under Aventice), plus hosts in 155.254.21/25/30/31.0/24 and 192.158.230/232/238.0/24.
- **Tier.Net:** 155.254.29.0/24 (H4Y reallocation), 192.158.225.170, 192.154.253.233.
- **Hetzner:** 95.216.122.225–253 and 65.109.58.141. Other tenants share 95.216.122.0/24 (EXCLUDED from this cluster).

## 5. Domains

92 domains (see [`../iocs/domains.csv`](../iocs/domains.csv)). Notable patterns:

- **Aged and expired names.** `roscoweb.com` (created 1999), `godsbarn.com` (2004, acquired through an aftermarket sale), `calicater.com` (2005). All three are now at GoDaddy on deSEC nameservers, with DNSSEC signed, last changed 2026-10-19/20.
- **Fresh names.** `adamsethfox.com` and `phoenixseniornews.com` were both registered at Spaceship on 2026-02-06. Both were last changed 2026-07-16 at 19:30 UTC, 18 seconds apart. Both use Cloudflare (`asa` / `miles` nameservers).
- **Typosquats** of real brands: `scraigslist.com`, `wwwpricechopper.com`, `pittsburghpostgazete.com`, `verginmoney.com`, `basproshops.com`.
- **Microsoft 365 verification records** (October–December 2025): `MS=ms76416861` and `MS=ms76477259` on `godsbarn.com`, and `MS=ms21570894` on `roscoweb.com`. This is consistent with Microsoft 365 tenants used for sending.

Prior owners of aged domains are EXCLUDED from attribution.

## 6. DNS edit timing (NOVEL technique)

The fleet's Cloudflare zones expose owner edit times through SOA serials (see [`../methodology/cloudflare-soa-serial-decoding.md`](../methodology/cloudflare-soa-serial-decoding.md)). Out of 79 decoded edits across five zones:

| Zones edited together | Times (UTC) | Gap |
|---|---|---|
| adamsethfox.com + phoenixseniornews.com | 2026-07-16 19:33:48 / 19:34:26 | 38 s |
| calicater.com + phoenixseniornews.com | 2026-08-21 11:18:19 / 11:19:56 | 97 s |
| devriendenvanjacob.com + gourmethazelnuts.com | 2026-06-09 12:57:53 / 12:58:47 | 54 s |

These pairs cross certificate families: the H4Y certificate family (`gourmethazelnuts`) with the Hetzner family (`devriendenvanjacob`), and the OVH families (`adamsethfox`, `phoenixseniornews`) with each other. Scripted, near-simultaneous edits across families support one operator. They do not prove it. The last edits before the BYOIP blocks went dark were at 2026-11-11 22:02 and 2026-11-12 02:05 UTC.

## 7. Activity outside mail

*Updated in v2.0.* Two fleet front addresses appeared in Microsoft Entra ID password-spray telemetry from a private source. Source, dates and target are withheld. SSH host keys tie them to two specific OVH servers: 54.36.174.217 (a Kafka broker) and 54.36.175.25 (a worker). See [`server-map.md`](server-map.md) and [`spray-infrastructure.md`](spray-infrastructure.md).

- The fleet carries spray traffic: **likely**. Confidence is moderate.
- The spray operator and the fleet operator are the same: **roughly even chance**. Confidence is low. (v1.0 said "likely not the same". Two observations on two different servers, one of them a broker, moved this.)

## 8. Shutdown of the BYOIP blocks

The eight blocks stopped answering on 2026-11-12. Shodan last saw `89.40.83.56` at 13:26 UTC that day. Routing data on 2026-11-20 still showed `194.104.138.0/24` and `89.40.83.0/24` announced by AS16276. Several blocks show new tenants after 2026-11-12. **The cause is unknown.** It could be a lease ending, a provider action or an operator move.

## 9. Attribution assessment

| Axis | Finding |
|---|---|
| Infrastructure ownership | Leased (IPXO) and rented (OVH, H4Y, Tier.Net, Hetzner). Registry holders are leasing identities, not operators. |
| Geolocation | Lessee geofeeds place blocks in Brazil, Poland and the US. EXCLUDED as evidence. |
| Time of activity | 86 events. Best working-day fit 64%; 28% on weekends. No time zone. See [`pattern-of-life.md`](pattern-of-life.md). |
| Tooling | Go-based mail stack, Caddy, Kafka, Ubuntu 24.04. Common and non-specific. |
| Overlap with known actors | None found. |

**Operator identity and nationality: attribution not supported.** Only the providers' customer records (OVH, IPXO, H4Y, Hetzner, the registrars and Microsoft) can identify the operator.

## 10. Excluded leads

- Cloudflare edge IPs (shared infrastructure; never pivoted on).
- Other tenants in Hetzner 95.216.122.0/24 and in OVH 79.137.69/70.0/24.
- New tenants on the BYOIP blocks after 2026-11-12.
- A stale forward DNS record on `vc-ovh.onappdev.com` from a previous tenant.
- A separate mail cluster using Alibaba DirectMail, with different hours, domain sources and nameservers. Assessed as a separate operator (unlikely to be the same).

---

# Part 2 (v2.0): from front IPs to the operator's hardware

## 11. Front-to-server map (NOVEL)

Seven of the eight BYOIP /24s present the **same SSH host key** as one OVH dedicated server. The eighth matches by elimination. Result: 8 /24s, 8 servers, 3 Kafka brokers and 5 workers. Full table: [`server-map.md`](server-map.md). Method: [`../methodology/ssh-hostkey-front-to-server-mapping.md`](../methodology/ssh-hostkey-front-to-server-mapping.md).

## 12. Kafka backend (NOVEL)

The brokers run Java Kafka on TLS 1.3 with no client-certificate check. One script minted all broker certificates in 11 seconds on 2026-08-17. Serial `…b7:4f` is missing from the run. Detail: [`kafka-backend.md`](kafka-backend.md). Method: [`../methodology/certificate-serial-sequence-pivot.md`](../methodology/certificate-serial-sequence-pivot.md).

## 13. One scripted deployment (NOVEL)

Caddy encodes file modification time (ns) and size in its ETag. The same 446-byte page was written on a new node and on a broker **10.2 seconds apart** on 2026-07-29 (12:02:12.611 and 12:02:22.823 UTC). One deployment run built both. Method: [`../methodology/caddy-etag-forensics.md`](../methodology/caddy-etag-forensics.md).

## 14. Fleet expansion by web body hash (NOVEL)

The 446-byte Caddy page (SHA-1 `2979831850c7003c34c4b1dcc8c38d2d0a4dd84c`, title "Server") sits on 246 hosts across 50 apex domains. The sweep added `reedjordan.com` (node 15.204.194.100) and Hetzner node 95.216.122.254. Both share the fleet's exact SMTP dialogue. Method: [`../methodology/web-body-hash-sweep.md`](../methodology/web-body-hash-sweep.md).

## 15. Spray exits: one IPv6 lease order (NOVEL)

The IPv6 exits of the second spray toolset fall inside **19 /48s created in the IRR within 13 seconds** on 2025-12-22. Neighbouring batches were not used. Detail: [`spray-infrastructure.md`](spray-infrastructure.md). Method: [`../methodology/irr-route-object-batch-clustering.md`](../methodology/irr-route-object-batch-clustering.md).

## 16. Where control sits

| Candidate | Likelihood | Confidence |
|---|---|---|
| The 8 OVH servers ran the spray tool themselves | Roughly even chance | Low |
| The 3 brokers are the single "main" control asset | Unlikely | Low |
| Control sits outside the visible fleet (operator workstation or a separate server) | Roughly even chance | Low |

The passive hunt for a control server is exhausted. The remaining questions need provider records. See [`diamond-model.md`](diamond-model.md).

## 17. Updated attribution

**Attribution not supported.** No working-day pattern, no language artifact, no overlap with a named actor. See [`pattern-of-life.md`](pattern-of-life.md) and [`closed-leads.md`](closed-leads.md).
