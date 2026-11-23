# Shodan queries

| # | Purpose | Query |
|---|---|---|
| S1 | Fleet SMTP certificate format | `ssl:"mx_server"` |
| S2 | Fleet SMTP on port 25 | `port:25 ssl:"mx_server"` |
| S3 | Private Kafka CA (then check the AKI) | `ssl.cert.issuer.cn:"Kafka-Cluster-CA"` |
| S4 | Fleet hosts at one provider | `ssl:"mx_server" org:"H4Y Technologies LLC"` |
| S5 | Fleet hosts on OVH | `ssl:"mx_server" asn:AS16276` |

## v2.0 additions

| # | Purpose | Query |
|---|---|---|
| S6 | One broker certificate by serial | `ssl.cert.serial:17945f832aea9b9027ede5c1cb9ef532efe6b751` |
| S7 | The missing serial …b7:4f | `ssl.cert.serial:17945f832aea9b9027ede5c1cb9ef532efe6b74f` |
| S8 | SSH keys in one front /24 | `net:212.69.8.0/24 port:22` |
| S9 | A server's SSH key across the internet (MD5, free text) | `"d9:f9:6a:36:c3:48:25:87:4e:7d:7d:d3:d5:8b:23:af"` |
| S10 | The high-port blocks on two servers | `net:79.137.70.0/24 hash:-1246004407` |
| S11 | IPv6 exit ranges | `net:2602:fad4:17::/48` |
| S12 | Fleet SMTP on OVH without the leased fronts | `ssl:"mx_server" asn:AS16276 -net:212.69.8.0/24` |

## Known false positive

Shodan labels the fleet's port 443 "Ncat http proxy" with banner `HTTP/1.0 400 Bad Request`. That is Go's `net/http` answering plain HTTP on a TLS listener. It is **not** a proxy indicator (retraction R5). Don't hunt on that label.
