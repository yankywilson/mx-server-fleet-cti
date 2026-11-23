#!/usr/bin/env python3
"""Convert certificate serials between hex and decimal, and find gaps in a
sequential series.

Different search engines store serials differently:
  - Shodan ssl.cert.serial accepts hex or integer
  - Censys host.services.cert.parsed.serial_number is a decimal string
  - FOFA cert.sn is decimal (confirmed in this case)

Usage:
    python3 kafka_serial.py 17:94:5f:83:2a:ea:9b:90:27:ed:e5:c1:cb:9e:f5:32:ef:e6:b7:51
    python3 kafka_serial.py --gaps 17945f...b74e 17945f...b750 17945f...b751
"""
import argparse


def to_int(s):
    s = s.strip().lower().replace(":", "").replace(" ", "")
    if s.startswith("0x"):
        s = s[2:]
    if s.isdigit() and len(s) > 40:  # long all-digit string = decimal
        return int(s)
    return int(s, 16)


def to_hex(n, colons=True):
    h = format(n, "x")
    if len(h) % 2:
        h = "0" + h
    return ":".join(h[i:i + 2] for i in range(0, len(h), 2)) if colons else h


def gaps(values):
    nums = sorted(set(values))
    missing = []
    for a, b in zip(nums, nums[1:]):
        missing.extend(range(a + 1, b))
    return missing


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("serials", nargs="+")
    p.add_argument("--gaps", action="store_true", help="list missing serials between the given ones")
    a = p.parse_args(argv)
    nums = [to_int(s) for s in a.serials]
    for n in nums:
        print(f"hex={to_hex(n)}\thex_plain={to_hex(n, False)}\tdecimal={n}")
    if a.gaps:
        for m in gaps(nums):
            print(f"MISSING\thex={to_hex(m)}\tdecimal={m}")


if __name__ == "__main__":
    main()
