# SSH host-key front-to-server mapping

**Purpose.** Find the physical server behind leased, BYOIP or "additional" IP addresses.

**Principle.** `sshd` presents one host key per machine, on every address the machine owns. Two addresses with the same host key are the same `sshd` on the same machine. Host keys are generated at OS install, so a match is near-unique.

## Steps

1. **List the front addresses.** For each leased /24, pick hosts with port 22 open.
2. **Collect the key fingerprints.** Scanner data is enough. No connection is needed.

   | Tool | Query |
   |---|---|
   | Shodan | `net:212.69.8.0/24 port:22`, then read the "SSH fingerprint" (MD5) on each host |
   | Censys | `host.ip: "212.69.8.0/24"`, then read `ssh.server_host_key.fingerprint_sha256` on each host |
   | FOFA | `ip="212.69.8.0/24" && port="22"`, then read the banner |

3. **Pivot on the fingerprint.** Search it across the whole internet.

   | Tool | Query |
   |---|---|
   | Censys | `host.services.ssh.server_host_key.fingerprint_sha256 = "383801cf775dffbe7ccd2a938b0a0dc85ab6020be7bc13561872ff368b7d4e7e"` |
   | Shodan | Search the MD5 fingerprint as free text: `"d9:f9:6a:36:c3:48:25:87:4e:7d:7d:d3:d5:8b:23:af"` |

4. **Find the native address.** The hit that is **not** in a leased range, and whose reverse DNS or provider is the host's own, is the server.
5. **Confirm with a second signal.** Use one of: a TLS certificate whose CN or SAN names the native IP; a unique OpenSSH patch level; an identical port block; identical banners.
6. **Group and map.** Run [`../tools/ssh_front_map.py`](../tools/ssh_front_map.py) on a CSV of `ip,fingerprint` rows. Pass `--native` with the provider's native ranges, comma-separated.

```text
$ python3 tools/ssh_front_map.py data/ssh_hostkey_observations.csv --native 54.36.0.0/16,79.137.0.0/16
34:8f:68:2c:f2:b5:4f:47:cf:59:43:8b:b0:b3:b4:79
  server(native): 54.36.175.25
  fronts: 194.104.138.0/24
38:e8:b2:d0:af:94:21:c2:08:77:cb:51:4a:27:07:0b
  server(native): 79.137.70.34
  fronts: 151.242.139.0/24
…
```

## Pitfalls

| Pitfall | Control |
|---|---|
| Cloned VM images share host keys | Require a second signal (step 5). Clones on unrelated providers are a known false positive |
| Load balancers or SSH proxies in front | The key belongs to the proxy, not to the back end. Check the banner and port set |
| Key rotation after reinstall | Use observation dates. A key seen before and after a reinstall will not match |
| `sshd` that refuses scans ("Exceeded MaxStartups") | No key collected. Map by elimination and say so |

## Result in this case

7 of 8 /24s mapped by key, 1 by elimination. See [`../docs/server-map.md`](../docs/server-map.md).
