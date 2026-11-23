#!/usr/bin/env python3
"""Decode a Caddy file-server ETag into file modification time and size.

Caddy builds the ETag for static files as:
    base36(modtime in Unix nanoseconds) + base36(file size in bytes)
The size part has no fixed width, so this tool tries each split and keeps
the ones whose size matches a known Content-Length (or lists all plausible
splits when no length is given).

Usage:
    python3 caddy_etag.py '"dkb1fqjbnd35ce"' --content-length 446
    python3 caddy_etag.py dkb1fv87lqycce dkb1fqjbnd35ce --content-length 446
"""
import argparse
import datetime as dt
import sys

MIN_NS = int(dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc).timestamp() * 1e9)
MAX_NS = int(dt.datetime(2100, 1, 1, tzinfo=dt.timezone.utc).timestamp() * 1e9)


def decode(etag, content_length=None):
    """Return a list of (mtime_utc, size) candidates for one ETag."""
    tag = etag.strip()
    if tag.startswith("W/"):
        tag = tag[2:]
    tag = tag.strip('"').lower()
    out = []
    for cut in range(1, min(8, len(tag) - 1) + 1):
        time_part, size_part = tag[:-cut], tag[-cut:]
        try:
            ns, size = int(time_part, 36), int(size_part, 36)
        except ValueError:
            continue
        if not MIN_NS <= ns <= MAX_NS:
            continue
        if content_length is not None and size != content_length:
            continue
        ts = dt.datetime.fromtimestamp(ns / 1e9, dt.timezone.utc)
        out.append((ts, size, ns))
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("etags", nargs="+")
    p.add_argument("--content-length", type=int, default=None)
    a = p.parse_args(argv)
    rows = []
    for e in a.etags:
        cands = decode(e, a.content_length)
        if not cands:
            print(f"{e}\tno plausible decode", file=sys.stderr)
        for ts, size, ns in cands:
            rows.append((ts, e, size))
            print(f"{e}\tmtime_utc={ts.isoformat(timespec='microseconds')}\tsize={size}")
    if len(rows) > 1:
        rows.sort()
        print("\nOrdered by write time (delta from first):")
        t0 = rows[0][0]
        for ts, e, size in rows:
            print(f"  +{(ts - t0).total_seconds():10.3f}s  {e}  size={size}")


if __name__ == "__main__":
    main()
