# Certificate serial-sequence pivot

**Purpose.** Date a private CA's issuing run and find members you have not seen.

**Principle.** Many hand-built CAs (OpenSSL with a serial file, Java `keytool`, simple scripts) issue **sequential serials**. A sequence with known `notBefore` times shows the order and timing of issuance. A gap is a certificate that was issued but has not been observed.

## Steps

1. **Collect** every certificate with the CA's Authority Key Identifier (not just its name).
2. **Sort** by serial. Convert hex to decimal for tools that store decimal.

```text
$ python3 tools/kafka_serial.py --gaps \
    17:94:5f:83:2a:ea:9b:90:27:ed:e5:c1:cb:9e:f5:32:ef:e6:b7:4e \
    17:94:5f:83:2a:ea:9b:90:27:ed:e5:c1:cb:9e:f5:32:ef:e6:b7:50 \
    17:94:5f:83:2a:ea:9b:90:27:ed:e5:c1:cb:9e:f5:32:ef:e6:b7:51
hex=…:b7:4e  decimal=134615618319530153631244838655347924586237179726
hex=…:b7:50  decimal=134615618319530153631244838655347924586237179728
hex=…:b7:51  decimal=134615618319530153631244838655347924586237179729
MISSING	hex=17:94:5f:83:2a:ea:9b:90:27:ed:e5:c1:cb:9e:f5:32:ef:e6:b7:4f	decimal=134615618319530153631244838655347924586237179727
```

3. **Hunt the gap** in each scanner, in the format it stores.

   | Tool | Format | Query |
   |---|---|---|
   | Censys | decimal string | `host.services.cert.parsed.serial_number = "134615618319530153631244838655347924586237179727"` |
   | FOFA | decimal | `cert.sn="134615618319530153631244838655347924586237179727"` |
   | Shodan | hex or integer | `ssl.cert.serial:17945f832aea9b9027ede5c1cb9ef532efe6b74f` |
   | Suricata | uppercase hex with colons | `tls.cert_serial; content:"17:94:5F:…:B7:4F";` |

4. **Read the timing.** `notBefore` values seconds apart mean one scripted run.

## Interpreting a gap

| Explanation | How to test |
|---|---|
| An internal broker or host not exposed to the internet | Not testable passively |
| A client certificate (no listener) | Not testable passively |
| A certificate issued and discarded (failed run) | Not testable passively |
| A host the scanners have not reached yet | Re-run the hunt over time |

Report a gap that stays empty as a null result. Do not claim a hidden host.

## Result in this case

Three brokers in 11 seconds; serial `…b7:4f` not found in Shodan, Censys or FOFA. See [`../docs/kafka-backend.md`](../docs/kafka-backend.md).
