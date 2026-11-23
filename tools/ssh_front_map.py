#!/usr/bin/env python3
"""Map front IPs (BYOIP / additional IPs) to the physical server behind them
by grouping on SSH host-key fingerprint.

sshd answers on every address routed to a server with the same host key.
A front address and a provider-native address that share a key are the
same machine.

Input CSV columns: ip,ssh_fingerprint[,label]
  ssh_fingerprint may be MD5 (aa:bb:...) or SHA-256 hex; keep one type per run.

Usage:
    python3 ssh_front_map.py observations.csv --native 54.36.0.0/16,79.137.64.0/18
"""
import argparse
import collections
import csv
import ipaddress


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--native", default="", help="comma-separated provider-native ranges")
    a = p.parse_args(argv)
    native = [ipaddress.ip_network(x) for x in a.native.split(",") if x]
    groups = collections.defaultdict(list)
    with open(a.csv, newline="") as f:
        for r in csv.DictReader(f):
            groups[r["ssh_fingerprint"].strip().lower()].append(r)
    for fp, rows in sorted(groups.items()):
        ips = sorted({r["ip"] for r in rows}, key=ipaddress.ip_address)
        nat = [i for i in ips if any(ipaddress.ip_address(i) in n for n in native)]
        fronts = sorted({str(ipaddress.ip_network(i + "/24", strict=False)) for i in ips if i not in nat})
        print(f"{fp}\n  server(native): {', '.join(nat) or 'NOT FOUND'}\n  fronts: {', '.join(fronts) or '-'}")


if __name__ == "__main__":
    main()
