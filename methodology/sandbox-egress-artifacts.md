# Sandbox egress-proxy artifacts

**Purpose.** Stop a public sandbox's own network stack from being read as the target's.

**Principle.** Public sandboxes often route analysed traffic through an egress proxy. For ports the proxy handles (often 80 and 443), the SYN-ACK comes from the proxy, a few hops away. For other ports, it comes from the real target, across the internet. The TCP fields differ.

## Steps

1. Open the sandbox PCAP in Wireshark or `tshark`.
2. For each destination port, take the first SYN-ACK and record TTL, MSS, window and handshake RTT.

```text
tshark -r capture.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==1" \
  -T fields -e ip.src -e tcp.srcport -e ip.ttl -e tcp.options.mss_val \
  -e tcp.window_size_value -e tcp.analysis.initial_rtt
```

3. Compare port groups.

| Field | Proxy-answered port | Real target |
|---|---|---|
| TTL | Close to 64 or 128 (few hops) | Lower (many hops) |
| MSS | Proxy-specific (for example 1380) | Usually 1460 |
| RTT | Short and constant | Longer, matches geography |

## Result in this case

| Ports | TTL | MSS | Window | RTT | Source |
|---|---|---|---|---|---|
| 80, 443 | 62 | 1380 | 64860 | ~42 ms | Sandbox egress proxy |
| 9092 | 48/49 | 1460 | — | ~80 ms | Real broker |

Retraction R8 records the claim this test corrected.
