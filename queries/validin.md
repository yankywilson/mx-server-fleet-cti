# Validin pivots

Validin keeps passive DNS and host-response history. These are the pivots used in v2.0. Exact menu names may change. The pivot types are stable.

| # | Purpose | Pivot |
|---|---|---|
| V1 | Every host serving the fleet Caddy page | Host response → body SHA-1 `2979831850c7003c34c4b1dcc8c38d2d0a4dd84c` |
| V2 | Server history for one IP | IP → `54.36.174.217` → DNS history and host responses |
| V3 | Reverse DNS changes on a broker | IP → PTR history (the broker became `tendersage.straightmembers.com` on 2026-07-25) |
| V4 | First and last seen for each front /24 | CIDR → `212.69.8.0/24` (repeat for all 8) |
| V5 | New fleet domains | Domain → name servers and A records on fleet IPs, first seen after the last export |

## Results recorded

| Pivot | Result |
|---|---|
| V1 | 246 hosts, 247 IPs, 50 apex domains |
| V4 | All 8 /24s last seen serving fleet content on 2026-11-12 |
| V2 | The 8 OVH servers active to 2026-11-23; Hetzner 95.216.122.0/24 nodes to 2026-11-20 |
