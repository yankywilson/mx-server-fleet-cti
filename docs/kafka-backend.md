# The Kafka backend (v2.0)

**Bottom line.** Three of the eight OVH servers form an **Apache Kafka cluster on Java**, secured with a hand-built CA that was generated in one scripted run. Its certificates are the most durable fingerprint of this operator. The listener accepts TLS from anyone, without client certificates.

## The certificate series

All three broker certificates come from one private CA, `CN=Kafka-Cluster-CA`, Authority Key Identifier `AA:77:1C:B8:E5:D7:A5:98:2E:4F:FF:17:23:13:80:55:5C:65:50:3A`.

| Serial (hex) | Subject CN = SAN IP | Not before (UTC) | Front /24 that presents it |
|---|---|---|---|
| `17:94:5f:83:2a:ea:9b:90:27:ed:e5:c1:cb:9e:f5:32:ef:e6:b7:4e` | 79.137.69.148 | 2026-08-17 15:37:01 | 77.67.28.0/24 |
| `…:b7:4f` | **not observed** | between 15:37:01 and 15:37:11 | — |
| `…:b7:50` | 79.137.70.8 | 2026-08-17 15:37:11 | 89.40.83.0/24 |
| `…:b7:51` | 54.36.174.217 | 2026-08-17 15:37:12 | 212.69.8.0/24 |

Decimal forms (Censys and FOFA store decimal): [`../data/kafka_broker_certs.csv`](../data/kafka_broker_certs.csv). Convert with [`../tools/kafka_serial.py`](../tools/kafka_serial.py).

### Certificate profile

| Property | Value | Why it matters |
|---|---|---|
| Key | RSA-4096, SHA256withRSA | Uncommon for auto-generated broker certs |
| Subject / SAN | CN and SAN = the server's own native IP; no organization | Reveals the server behind every front IP |
| Validity | 10 years (2026-08-17 → 2036-08-14) | Scripted, not a managed PKI |
| EKU | serverAuth + clientAuth | Standard Kafka inter-broker setup |
| Chain | Leaf only; CA certificate not sent | — |
| Serials | Sequential, 11 seconds end to end | One script run issued the whole set |

### The missing serial …b7:4f

The series skips `…b7:4f`. It was minted between the first and second broker certificates. Searches of Shodan host data, Censys (serial as decimal) and FOFA (`cert.sn`, decimal confirmed) returned **no host**. It is most likely an internal broker, a client certificate or a discarded certificate. This is a null result, kept on record.

## The listener (packet capture)

A sandbox browser session against `54.36.174.217:9092` completed 17 TLS handshakes. Decoding them as TLS:

| Property | Value |
|---|---|
| TLS version / cipher | TLS 1.3, `TLS_AES_256_GCM_SHA384`, x25519 |
| ServerHello extensions | supported_versions (43), key_share (51) only |
| ALPN | none selected |
| Session ticket lifetime | 86,400 s, the Java (JDK) TLS default |
| Client certificate request | **None.** The handshake carries EncryptedExtensions, Certificate, CertificateVerify and Finished, but no CertificateRequest |
| Response to an HTTP request | Clean `close_notify` |
| JA3S | `15af977ce25de452b96affa2addb1036`. **Not a fingerprint**: an unrelated Kafka deployment shows the same value |

**Meaning.** Anyone on the internet can complete a TLS session with the broker. Any authentication would have to happen in the Kafka layer (SASL), which the capture cannot show.

**Boundary.** This repository does not connect to the brokers with a Kafka client. Listing topics or reading messages on someone else's system is unauthorized access, whoever runs it. That step belongs to the hosting provider or law enforcement.

## Topology

- **3 brokers, 5 workers.** Only the brokers expose 9092/9093. The workers run the same mail and web build, plus port 9101 on some nodes.
- All eight servers expose **TCP 53**. Content not captured.
- 79.137.70.8 (broker) and 79.137.70.17 (worker) expose **blocks of about 45–60 high ports** (121xx–125xx) that answer plain HTTP with `HTTP/1.1 400 Bad Request` and `Connection: close` (Shodan banner hash `-1246004407`). Adjacent, non-overlapping blocks on different servers look like a **port-per-session allocation**.

## Assessment

| Judgment | Likelihood | Confidence |
|---|---|---|
| The brokers are a Java Apache Kafka cluster under one operator | Very likely | Moderate |
| Kafka is the fleet's coordination backend (job or message queue for the workers) | Likely | Low-moderate |
| The high-port blocks are a proxy service sold or used on the side | Roughly even chance | Low |
| The brokers control the password spray | Roughly even chance | Low |

## Hunting

| Tool | Query |
|---|---|
| Shodan | `ssl.cert.issuer.cn:"Kafka-Cluster-CA"`, then keep AKI `AA:77:1C…` |
| Shodan | `ssl.cert.serial:17945f832aea9b9027ede5c1cb9ef532efe6b74f` (the missing serial) |
| Censys | `host.services.cert.parsed.serial_number = "134615618319530153631244838655347924586237179727"` |
| FOFA | `cert.sn="134615618319530153631244838655347924586237179727"` |
| Suricata | [`../detections/suricata/mx-server-fleet.rules`](../detections/suricata/mx-server-fleet.rules) |

The issuer name alone is **not** enough. "Kafka Cluster CA" variants are common. One look-alike cluster with a different AKI and its own organization name turned up during this research and was excluded. See [`closed-leads.md`](closed-leads.md) (L1).
