# Web body-hash sweep

**Purpose.** Find fleet members the certificate pivot missed.

**Principle.** An operator who deploys by script often serves the **same default page** on every node. The page body hash survives domain changes, certificate changes and new IPs.

## Steps

1. **Take a known node's page.** Record body hash, `Content-Length`, `<title>` and `Server` header. Here: SHA-1 `2979831850c7003c34c4b1dcc8c38d2d0a4dd84c`, 446 bytes, title "Server", `Server: Caddy`.
2. **Sweep.**

   | Tool | Query |
   |---|---|
   | Validin | Host response search on the body SHA-1 |
   | FOFA | `title=="Server" && server="Caddy"`, then filter by header hash `707484123` |
   | Shodan | `http.html_hash:<mmh3 of body>` (compute from the saved body) |

3. **Validate each hit** with at least one more fleet feature ([`fleet-fingerprint.md`](fleet-fingerprint.md)): the SMTP dialogue, `O=mx_server`, the Kafka AKI, or an adjective+noun hostname.
4. **Drop shared front ends.** A hit on a CDN or a shared hosting IP is not a fleet node.

## Result in this case

246 hosts, 50 apex domains. New members: `reedjordan.com` (15.204.194.100) and a Hetzner node (95.216.122.254), both with the fleet's exact SMTP banner and `HELP` response.

## Caution

A 446-byte "Server" page is simple. Unrelated Caddy users can produce the same body. The hash alone is **medium** strength. Always validate (step 3).
