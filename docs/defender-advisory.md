# Defender advisory (v2.0)

**For:** SOC, identity and mail teams. **Action:** block, hunt, harden. **TLP:** CLEAR.

## 1. Block

| What | Where | File |
|---|---|---|
| 8 OVH server IPs (durable) | Firewall, EDR network block, Entra named location | [`../iocs/servers.csv`](../iocs/servers.csv) |
| 2,463 fleet IPs | Mail gateway, firewall | [`../iocs/fleet-ips.csv`](../iocs/fleet-ips.csv) |
| 8 BYOIP /24s and other netblocks | Mail gateway; **review after the lease ends** | [`../iocs/netblocks.csv`](../iocs/netblocks.csv) |
| IPv6 exit ranges | Entra named location (block the 2602:fad4 batch; **monitor the two /29s first**, they are large shared ranges), sign-in alerting | [`../iocs/ipv6-exit-ranges.csv`](../iocs/ipv6-exit-ranges.csv) |
| 93 domains | DNS filter, web proxy, mail gateway | [`../iocs/domains.csv`](../iocs/domains.csv) |

**Do not block** Cloudflare edge IPs that some fleet apex domains resolve to. Block the domain names instead (closed lead L7).

**Leased space changes hands.** The /24s and IPv6 /48s belong to a leasing platform. Set a review date. Remove the block when passive DNS shows a new tenant.

## 2. Hunt

| Hunt | Data source | File |
|---|---|---|
| H1–H5 | Fleet IPs and domains in mail, network and sign-in data | [`../detections/kql-hunts.md`](../detections/kql-hunts.md) |
| H6 | Azure AD PowerShell sign-ins with an empty or bare `Mozilla/5.0` user agent | same |
| H7 | `Go-http-client` against the Azure Portal | same |
| H8 | Sign-ins from the IPv6 lease batch | same |
| H9 | Sign-ins or mail from the 8 servers or their fronts | same |
| Sigma | Generic SIEM versions | [`../detections/sigma/`](../detections/sigma/) |
| Suricata | Kafka CA, serial prefix, `O=mx_server` | [`../detections/suricata/mx-server-fleet.rules`](../detections/suricata/mx-server-fleet.rules) |

## 3. Harden Entra ID

The spray succeeds only where a password is valid **and** nothing else stops it.

| Control | Why |
|---|---|
| MFA for all users on all cloud apps | A valid password alone is not enough |
| Block legacy authentication | Removes protocols that cannot do MFA |
| Restrict the Azure management app to admin roles | Toolset B targets the Azure Portal |
| Review ROPC use | Toolset A uses the resource-owner password flow |
| Tune smart lockout | Slows per-account guessing |
| Named-location block for the ranges above | Adds signal. Note: Conditional Access runs **after** the password check, so attempts still reach the log |

## 4. What a hit means

| Result in the sign-in log | Meaning |
|---|---|
| `50126` | Wrong password |
| `50053` | Account locked or IP flagged as malicious. **Says nothing about the password** |
| `53003` | Blocked by Conditional Access **after** a correct password. **Reset the password** |
| `50074` / `50076` | MFA required after a correct password. **Reset the password** |
| `0` | Success. Start incident response |

## 5. Sharing

Indicators are also in STIX 2.1: [`../stix/mx-server-fleet.json`](../stix/mx-server-fleet.json).
