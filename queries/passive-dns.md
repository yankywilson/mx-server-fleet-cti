# Passive DNS patterns

| Goal | Pattern |
|---|---|
| Find new fleet hostnames | Subdomains of the 92 domains matching `^[a-z]+[a-z]+\.` (adjective+noun), A records in fleet netblocks |
| Find new fleet domains | Domains with A/MX records pointing at fleet IPs, first seen after 2026-11-20 |
| Recover DNS edit times | SOA serial history of Cloudflare-hosted fleet zones, decoded with `serial - 625485663` (see methodology) |
| Find tenant and site verification | TXT history for `MS=ms` and `google-site-verification=` on fleet domains |
| Detect re-hosting | PTR history on the 8 BYOIP /24s after 2026-11-12 (new tenants mean the IPs are no longer fleet) |
