# Changelog

## v2.0 - 2026-11-23

### Added
- **Server map.** 8 BYOIP /24s mapped to 8 OVH dedicated servers by SSH host key (`docs/server-map.md`, `iocs/servers.csv`).
- **Kafka backend.** 3 brokers, CA issuing run of 11 s, missing serial `…b7:4f`, TLS 1.3 profile without client certificates (`docs/kafka-backend.md`).
- **Spray infrastructure.** Two toolsets; two fleet servers in private telemetry; IPv6 lease batch of 19 × /48 (`docs/spray-infrastructure.md`, `iocs/ipv6-exit-ranges.csv`).
- **Pattern of life.** 86-event working-hours test; nationality null result (`docs/pattern-of-life.md`).
- **Closed leads** (10), **defender advisory**, **MITRE ATT&CK mapping** with Navigator layer, **diamond model**.
- **Methodology:** SSH host-key mapping, IRR batch clustering, Caddy ETag forensics, certificate serial-sequence pivot, sandbox egress artifacts, web body-hash sweep.
- **Tools:** six dependency-free Python tools and 10 unit tests (`tools/`, `tests/`).
- **Data:** raw observations behind each finding (`data/`).
- **Detections:** KQL H6–H9, 3 Sigma rules, 5 Suricata rules.
- **Queries:** FOFA and Validin; new Censys (C8–C13) and Shodan (S6–S12) queries.
- `CITATION.cff`.

### Changed
- Fleet: 2,463 hosts (+`15.204.194.100`, +`95.216.122.254`), 93 domains (+`reedjordan.com`).
- STIX bundle: 384 → 427 objects (8 server infrastructure objects, new indicators, an assessment note).
- Technical analysis §7 and §9 updated; Part 2 (§11–17) added.
- Judgment on spray/fleet relationship moved from "unlikely" to "roughly even chance" (see retraction log).

### Corrected
- R8: sandbox egress-proxy artifact on 80/443.
- R9: JA3S is not a fleet fingerprint.

## v1.0 - 2026-11-20
- Initial public release.
- 2,461 fleet IPs, 92 domains, 2,515 hostnames, 4 certificate families.
- Methods: OVH BYOIP token clustering, BYOIP-to-server routing proof, Cloudflare SOA serial decoding.
- Detections: 5 Defender KQL hunts, 3 Sigma rules. STIX 2.1 bundle.
- Retraction log with 7 corrections.
