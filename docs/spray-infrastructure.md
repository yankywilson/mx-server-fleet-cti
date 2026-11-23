# Password-spray infrastructure (v2.0)

**Bottom line.** Private Microsoft Entra ID password-spray telemetry (source, dates and target withheld) shows **two toolsets** reaching Entra ID through **two kinds of exit infrastructure**. One uses this fleet's servers. The other uses a commercial-looking IPv6 proxy pool that was leased as **one 19-prefix batch**, found through IRR object timestamps. The operator's own control server is not visible from the victim side in either case.

## Two toolsets

| | Toolset A | Toolset B |
|---|---|---|
| Client | Azure Active Directory PowerShell (ROPC) | Go HTTP client against the Azure Portal app |
| User agent | empty, or bare `Mozilla/5.0` | `Go-http-client/1.1`; a stale Edge 130 string ending in `OS/10.0.26100` |
| Exits | mx_server fleet servers (2 observations) and unrelated IPv4 hosts | IPv6 lease batch announced by AS6079 |
| Share of observed attempts | Small | Large majority |

This repository does not claim that the two toolsets belong to one actor. They appear in the same private telemetry. The infrastructure under each one is documented separately below.

## Toolset A on the fleet

Two front addresses in the telemetry map to specific OVH servers by SSH host key ([`server-map.md`](server-map.md)):

- a 212.69.8.0/24 address → **54.36.174.217** (Kafka broker)
- a 194.104.138.0/24 address → **54.36.175.25** (worker)

## Toolset B: one IPv6 lease order (NOVEL)

The IPv6 exits rotate through random interface IDs across nine different /48s in `2602:fad4::/36`. That looks like many networks. The IRR shows it is one order:

| Prefixes | Origin | Maintainer | IRR object created (UTC) |
|---|---|---|---|
| **2602:fad4:17::/48 – 2602:fad4:29::/48 (19 × /48)** | **AS6079** | **MNT-DCL-577** | **2025-12-22 11:44:35 – 11:44:48** |
| 2602:fad4:10–14::/48 | AS9009 | MNT-DCL-577 | 2025-10-16 11:36 |
| 2602:fad4:15::/48 | AS6079 | MAINT-AS11404 | 2026-09-17 01:13 |
| 2602:fad4:16::/48 | AS6079 | MNT-DCL-577 | 2025-12-17 20:17 |
| 2602:fad4:2a–2c::/48 | AS215294 | MNT-DCL-577 | 2026-01-06 12:25–12:27 |
| 2602:fad4:2d::/48 | AS6079 | MNT-DCL-577 | 2026-02-26 13:30 |
| 2602:fad4:2e::/48 | AS29802 | MNT-DCL-577 | 2026-05-20 11:22 |

**All nine /48s seen in the telemetry fall inside the 13-second batch.** None falls in the neighbouring batches. Reproduce with [`../tools/irr_batch_cluster.py`](../tools/irr_batch_cluster.py) and [`../data/irr_route6_2602-fad4.csv`](../data/irr_route6_2602-fad4.csv).

Two further /29s used by toolset B are announced by the same origin (AS6079): `2a0d:4b40::/29` (RIPE maintainer `netutils-mnt`, the same leasing platform) and `2a0a:7e00::/29`.

### Why this looks like an "ISP proxy" pool

- The space is **leased** through the same leasing platform as the fleet's IPv4 /24s, and it is **announced by a residential broadband ASN** (AS6079, Astound/RCN). Leased space announced by an eyeball ASN is the usual setup for proxies sold as "static residential" or "ISP" addresses.
- Interface IDs are random and change across /48s from one attempt to the next. A single server with a routed block could do this. So does a proxy pool.

| Judgment | Likelihood | Confidence |
|---|---|---|
| The 19 /48s are one lessee's order | Very likely | Moderate |
| Toolset B exits are a commercial ISP-proxy pool | Likely | Low-moderate |
| Toolset B exits are one operator-owned server | Unlikely | Low |

## Where the control server is

From the victim side, **nowhere visible**. The spray client talks only to Microsoft, through exits. What the evidence supports:

- **Toolset A:** two attempts physically left two fleet servers. Whether those servers **ran** the tool or **relayed** it is a roughly even chance (low confidence).
- **Toolset B:** the next hop back is the lessee of the 2025-12-22 batch. Only the leasing platform, the proxy operator or law enforcement can name it.

## Detection

- Sign-ins from the IPv6 ranges in [`../iocs/ipv6-exit-ranges.csv`](../iocs/ipv6-exit-ranges.csv) and the servers in [`../iocs/servers.csv`](../iocs/servers.csv).
- Azure AD PowerShell with an empty or bare `Mozilla/5.0` user agent.
- `Go-http-client` against the Azure Portal application.
- Queries: [`../detections/kql-hunts.md`](../detections/kql-hunts.md) H6–H9. Sigma: [`../detections/sigma/`](../detections/sigma/).

## Defensive note

Conditional Access is evaluated **after** the password check. Blocking these networks with a named location still lets attempts arrive and be logged, and a correct password then returns `53003` instead of `50126`. The controls that change the outcome are MFA on every app, blocking the Azure management API for non-admins, legacy-authentication blocking and smart lockout tuning.
