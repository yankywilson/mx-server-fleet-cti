# MITRE ATT&CK mapping (v2.0)

Each technique is mapped only where this repository holds evidence. "Observed" means seen in public data or in the private telemetry. "Inferred" means a judgment, with the likelihood given.

| Tactic | Technique | ID | Evidence | Status |
|---|---|---|---|---|
| Resource Development | Acquire Infrastructure: Domains | T1583.001 | 93 domains, including aged and expired domains and typosquats | Observed |
| Resource Development | Acquire Infrastructure: Server | T1583.004 | Eight OVH dedicated servers, Hetzner and US-hosted nodes | Observed |
| Resource Development | Acquire Infrastructure: Virtual Private Server | T1583.003 | US-hosted single nodes (for example 15.204.194.100) | Observed |
| Resource Development | Develop Capabilities: Digital Certificates | T1587.003 | Private `Kafka-Cluster-CA`; self-signed `O=mx_server` SMTP certificates | Observed |
| Resource Development | Stage Capabilities: Install Digital Certificate | T1608.003 | Certificates deployed across 2,463 hosts | Observed |
| Defense Evasion / C2 | Hide Infrastructure | T1665 | Leased BYOIP /24s in front of the operator's own servers; three leasing identities in front of one OVH account | Observed |
| Command and Control | Proxy: External Proxy | T1090.002 | Spray traffic leaves through fleet servers and through a leased IPv6 pool | Observed (exits). Whether the fleet relays for others: roughly even chance |
| Credential Access | Brute Force: Password Spraying | T1110.003 | Entra ID ROPC and Azure Portal attempts in private telemetry | Observed |
| Initial Access | Valid Accounts: Cloud Accounts | T1078.004 | Goal of the spray. No success observed | Attempted |

## Not mapped

- **Phishing (T1566).** The fleet runs a mail stack at scale. No phishing message from the fleet is in this dataset. Not mapped.
- **Application Layer Protocol (T1071).** The Kafka backend may coordinate workers. No traffic content was seen. Not mapped.

## ATT&CK Navigator

```json
{
  "name": "mx_server fleet",
  "versions": {"attack": "16", "navigator": "5.1.0", "layer": "4.5"},
  "domain": "enterprise-attack",
  "techniques": [
    {"techniqueID": "T1583.001", "color": "#e60d0d"},
    {"techniqueID": "T1583.003", "color": "#e60d0d"},
    {"techniqueID": "T1583.004", "color": "#e60d0d"},
    {"techniqueID": "T1587.003", "color": "#e60d0d"},
    {"techniqueID": "T1608.003", "color": "#e60d0d"},
    {"techniqueID": "T1665", "color": "#e60d0d"},
    {"techniqueID": "T1090.002", "color": "#fc8d59"},
    {"techniqueID": "T1110.003", "color": "#e60d0d"},
    {"techniqueID": "T1078.004", "color": "#fee08b"}
  ]
}
```

Red: observed. Orange: observed in part. Yellow: attempted.
