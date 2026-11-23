# Censys queries (CenQL)

Field names were checked against docs.censys.com. `=` is an exact match. `:` is a case-insensitive contains match. Nested service conditions use `host.services: ( ... )`.

| # | Purpose | Query |
|---|---|---|
| C1 | Every host with the fleet SMTP certificate format | `host.services.cert.parsed.subject.organization = "mx_server"` |
| C2 | One certificate family | `host.services.cert.parsed.subject.organization = "mx_server" and host.services.cert.parsed.subject.common_name = "agilehawk.gourmethazelnuts.com"` |
| C3 | SMTP on 25 with the fleet certificate | `host.services: (port = "25" and protocol = "SMTP") and host.services.cert.parsed.subject.organization = "mx_server"` |
| C4 | The fleet's private Kafka CA (then keep only AKI `AA:77:1C:B8...50:3A`) | `host.services.cert.parsed.issuer.common_name = "Kafka-Cluster-CA"` |
| C5 | Kafka CA and fleet SMTP on the same host | `host.services.cert.parsed.issuer.common_name = "Kafka-Cluster-CA" and host.services.cert.parsed.subject.organization = "mx_server"` |
| C6 | Caddy hosts that also carry the fleet certificate | `host.services.software.product: "caddy" and host.services.cert.parsed.subject.organization = "mx_server"` |
| C7 | Fleet hosts on OVH | `host.autonomous_system.asn = 16276 and host.services.cert.parsed.subject.organization = "mx_server"` |

## v2.0 additions

| # | Purpose | Query |
|---|---|---|
| C8 | Every address that presents one server's SSH host key | `host.services.ssh.server_host_key.fingerprint_sha256 = "383801cf775dffbe7ccd2a938b0a0dc85ab6020be7bc13561872ff368b7d4e7e"` |
| C9 | Same, for the worker behind 194.104.138.0/24 | `host.services.ssh.server_host_key.fingerprint_sha256 = "db3d5455d3bdb57095d338af30199487f06106018bc9e2e9a87fbb72d773ac20"` |
| C10 | One broker certificate by serial (decimal) | `host.services.cert.parsed.serial_number = "134615618319530153631244838655347924586237179729"` |
| C11 | The missing serial …b7:4f | `host.services.cert.parsed.serial_number = "134615618319530153631244838655347924586237179727"` |
| C12 | One front /24 | `host.ip: "212.69.8.0/24"` |
| C13 | New node from the body-hash sweep | `host.ip: "15.204.194.100"` |

**Validation rule:** a hit is a fleet member when it matches C1 **and** at least one of: a known certificate CN, a fleet domain in the SAN, a generated adjective+noun hostname, or the Kafka AKI.
