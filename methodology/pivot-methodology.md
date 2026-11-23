# Pivot methodology

Each step is reproducible with public tools. Queries are in [`../queries/`](../queries/).

```mermaid
flowchart TD
    A["Seed: one fleet IP<br/>SMTP banner + O=mx_server cert"] --> B["Certificate pivot<br/>Censys / Shodan: O=mx_server"]
    B --> C["2,461 hosts, 4 cert families"]
    C --> D["SAN harvest<br/>92 domains, about 2,500 hostnames"]
    A --> E["RIPE inetnum<br/>OVH BYOIP token in descr"]
    E --> F["Full-text token search<br/>8 ranges, 1 OVH account"]
    F --> G["Version history<br/>token written 2026-07-17"]
    C --> H["Kafka 9092 cert on BYOIP IP<br/>CN = native OVH server"]
    H --> I["BYOIP routed to ns3066510"]
    D --> J["Passive DNS SOA serials<br/>decoded edit times"]
    J --> K["Cross-family edit bursts"]
    D --> L["RDAP + TXT history<br/>registrars, MS= tenant codes"]
    I --> M["SSH host-key pivot<br/>8 /24s → 8 OVH servers"]
    M --> N["Kafka serial sequence<br/>3 brokers in 11 s, gap …4f"]
    M --> O["Caddy ETag decode<br/>one deploy, 10.2 s apart"]
    O --> P["Body-hash sweep<br/>246 hosts, new nodes"]
    Q["Private spray telemetry<br/>exit IPs"] --> M
    Q --> R["IRR batch clustering<br/>19 × /48 lease order"]
```

## Step by step

1. **Seed.** Start from one fleet IP. Record the SMTP banner, the certificate subject and the issuer.
2. **Certificate pivot.** Search for `O=mx_server`. Group the results by CN to get the certificate families.
3. **SAN harvest.** Pull the SAN lists. Separate the apex domains from the hostnames.
4. **Registry pivot.** For each BYOIP block, read the RIPE inetnum. Extract the `descr` token. Search the token in full text.
5. **Routing pivot.** Use routing history to get announcement start and end dates.
6. **Kafka pivot.** Search for `Kafka-Cluster-CA`. Keep only hits with the fleet AKI. A CN naming another IP shows routing.
7. **DNS timing.** Pull SOA serial history for Cloudflare-hosted fleet zones and decode the edit times.
8. **Domain history.** Use RDAP for registrar and dates, and TXT history for `MS=` and other verification tokens.
9. **Exclusions.** Drop shared infrastructure (Cloudflare edges, shared /24 neighbours, re-leased blocks after 2026-11-12).

## v2.0 steps

10. **SSH host-key pivot.** Map each leased /24 to the server behind it. [ssh-hostkey-front-to-server-mapping.md](ssh-hostkey-front-to-server-mapping.md)
11. **Serial sequence.** Order the private CA's certificates and hunt the gaps. [certificate-serial-sequence-pivot.md](certificate-serial-sequence-pivot.md)
12. **ETag decode.** Turn web ETags into write times to find one deployment run. [caddy-etag-forensics.md](caddy-etag-forensics.md)
13. **Body-hash sweep.** Find nodes the certificate pivot missed. [web-body-hash-sweep.md](web-body-hash-sweep.md)
14. **IRR batch clustering.** Group leased exit prefixes into lease orders. [irr-route-object-batch-clustering.md](irr-route-object-batch-clustering.md)
15. **Sandbox sanity check.** Separate the sandbox's network from the target's. [sandbox-egress-artifacts.md](sandbox-egress-artifacts.md)
