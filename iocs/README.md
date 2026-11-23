# IOCs

| File | Contents | Rows |
|---|---|---|
| `fleet-ips.csv` | Every fleet IP with provider, ASN, SMTP banner hostname, certificate CN and last-seen date | 2,463 |
| `servers.csv` | **v2.0.** The 8 OVH dedicated servers behind the 8 BYOIP /24s, with SSH host keys, role and mapping evidence | 8 |
| `netblocks.csv` | /24s with fleet host counts, and whether the whole /24 is safe to block | 28 |
| `ipv6-exit-ranges.csv` | **v2.0.** IPv6 ranges used as password-spray exits, with registry evidence | 6 |
| `domains.csv` | 93 domains with certificate family, plus registrar, created date and DNS host where confirmed | 93 |
| `hostnames.txt` | Generated fleet hostnames from banners, PTRs and certificate SANs | 2,515 |
| `certificates.csv` | SMTP certificate families, the Kafka broker certificates (with serials) and a web certificate | 9 |
| `web-fingerprints.csv` | **v2.0.** Web, SMTP and port fingerprints, each rated by how well it isolates the fleet | 11 |
| `provider-identifiers.csv` | BYOIP token, IRR batch, IPXO lessee, registrar, nameserver pair, OVH server names | 12 |

Raw evidence behind these lists (IRR objects, certificate serials, SSH observations, ETags, SOA edits) is in [`../data/`](../data/).

## Usage

- **Inbound mail blocking:** safe for all IPs and domains.
- **Sign-in blocking (Entra ID Conditional Access named locations):** the 8 servers in `servers.csv`, the IPv4 netblocks marked `yes`, and the IPv6 ranges in `ipv6-exit-ranges.csv`. The two /29s are large shared ranges: monitor before you block.
- **Outbound blocking:** check `netblocks.csv`. The eight OVH BYOIP /24s may be re-leased to new tenants. Hetzner 95.216.122.0/24 has other tenants.
- **Freshness:** IPs are the least durable indicator. The durable ones are the Kafka CA key identifier, the `O=mx_server` certificate format, the 446-byte page body hash and the SMTP dialogue. Re-run the queries in `../queries/` for current hosts.
- **Name reuse:** some fleet domains imitate real brands (`scraigslist.com`, `wwwpricechopper.com`) or reuse names that belong to real people or businesses. Those people and businesses are not involved. Block the listed domain only.
- **Do not block** Cloudflare addresses that front a fleet apex domain (for example `musclecaradz.com`). They are shared.
