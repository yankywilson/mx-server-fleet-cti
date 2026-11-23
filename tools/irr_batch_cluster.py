#!/usr/bin/env python3
"""Cluster IRR route/route6 objects into creation batches.

Leasing platforms often register a customer's whole order in one automated
burst. Objects created within --window seconds of each other, with the same
origin ASN and maintainer, form one batch. A batch is a strong hint of one
lease order (one customer).

Input CSV columns: prefix,origin,mnt_by,created_utc   (ISO 8601)

Usage:
    python3 irr_batch_cluster.py route6_objects.csv --window 60
    python3 irr_batch_cluster.py route6_objects.csv --mark 2602:fad4:1d::/48,2602:fad4:23::/48
"""
import argparse
import csv
import datetime as dt
import ipaddress


def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["created"] = dt.datetime.fromisoformat(r["created_utc"].replace("Z", "+00:00"))
    return rows


def cluster(rows, window=60):
    rows = sorted(rows, key=lambda r: (r["origin"], r["mnt_by"], r["created"]))
    batches, cur = [], []
    for r in rows:
        if cur and (r["origin"] != cur[-1]["origin"] or r["mnt_by"] != cur[-1]["mnt_by"]
                    or (r["created"] - cur[-1]["created"]).total_seconds() > window):
            batches.append(cur)
            cur = []
        cur.append(r)
    if cur:
        batches.append(cur)
    return batches


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--window", type=int, default=60)
    p.add_argument("--mark", default="", help="comma-separated prefixes seen in your telemetry")
    a = p.parse_args(argv)
    marked = {ipaddress.ip_network(x) for x in a.mark.split(",") if x}
    for b in sorted(cluster(load(a.csv), a.window), key=lambda x: x[0]["created"]):
        nets = [ipaddress.ip_network(r["prefix"]) for r in b]
        hits = sum(1 for n in nets if n in marked)
        span = (b[-1]["created"] - b[0]["created"]).total_seconds()
        collapsed = ", ".join(str(n) for n in ipaddress.collapse_addresses(nets))
        print(f"{b[0]['created'].isoformat()}  +{span:.0f}s  origin={b[0]['origin']}  mnt={b[0]['mnt_by']}  "
              f"objects={len(b)}  marked={hits}  [{collapsed}]")


if __name__ == "__main__":
    main()
