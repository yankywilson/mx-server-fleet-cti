# Fleet fingerprint

Use these features **together**. One alone is weak. Three or more together is strong.

| # | Feature | Strength | Notes |
|---|---|---|---|
| 1 | SMTP certificate `O=mx_server`, self-signed ECDSA P-256 | Strong | CN is one of four known values or a new one. |
| 2 | Kafka broker certificate from `Kafka-Cluster-CA` with AKI `AA:77:1C:B8:E5:D7:A5:98:2E:4F:FF:17:23:13:80:55:5C:65:50:3A` | Strong | Match the AKI, not the name. |
| 3 | Generated adjective+noun hostnames (`eagercrest`, `agilehawk`, `velvetdeer`) on fleet domains | Medium | Also the SMTP banner. |
| 4 | Caddy on 80 redirecting to `https://<IP>/`, with OpenSSH 9.6p1 Ubuntu | Weak | Very common on its own. |
| 5 | SMTP `SIZE 10485760` with STARTTLS offering X25519MLKEM768 | Medium | Go 1.24+ mail stack. |
| 6 | `localhost.localdomain` EHLO on a server's primary IP | Weak | Marks the main IP of a multi-IP server. |
| 7 | Many sequential high ports answering `HTTP/1.1 400` | Weak | Seen on some nodes. Purpose unexplained. |
| 8 | 446-byte Caddy page, title "Server", body SHA-1 `2979831850c7003c34c4b1dcc8c38d2d0a4dd84c` | Medium | v2.0. Validate with another feature. |
| 9 | SMTP dialogue: `501 5.5.4 Invalid domain name`; `214` HELP lists `HELO EHLO MAIL RCPT DATA RSET NOOP QUIT VRFY EXPN HELP STARTTLS` | Medium | v2.0. Identical across nodes and providers. |
| 10 | OpenSSH 9.6p1 Ubuntu-3ubuntu13.18/.19/.20 with an SSH host key listed in `iocs/servers.csv` | Strong | v2.0. A key match is near-unique. |

**Do not use** Shodan's "Ncat http proxy" label on port 443 as a fleet feature. It is a mislabel of the Go/Caddy TLS listener (retraction R5).
