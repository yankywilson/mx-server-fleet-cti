#!/usr/bin/env python3
"""Working-hours test for operator activity timestamps.

For each UTC offset, count how many events fall inside a local working
window (default 09:00-21:00) and inside a local night window (01:00-07:00).
A uniform 24/7 spread puts about 50% inside a 12-hour window. Only a clear
excess, with quiet nights, supports a time-zone estimate. Never use the
output alone for nationality.

Input: one ISO 8601 UTC timestamp per line.
"""
import argparse
import collections
import datetime as dt


def load(path):
    with open(path) as f:
        return [dt.datetime.fromisoformat(l.strip().replace("Z", "+00:00")) for l in f if l.strip()]


def score(times, offset, day=(9, 21), night=(1, 7)):
    hours = [(t.hour + offset) % 24 for t in times]
    return (sum(day[0] <= h < day[1] for h in hours), sum(night[0] <= h < night[1] for h in hours))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file")
    a = p.parse_args(argv)
    t = load(a.file)
    print(f"events={len(t)}")
    h = collections.Counter(x.hour for x in t)
    print("UTC hours: " + " ".join(f"{k:02d}:{h.get(k, 0)}" for k in range(24)))
    wd = collections.Counter(x.strftime("%a") for x in t)
    print("weekdays:", dict(wd))
    for off in range(-11, 13):
        d, n = score(t, off)
        print(f"UTC{off:+d}\tday={d}/{len(t)} ({100*d/len(t):.0f}%)\tnight={n}")


if __name__ == "__main__":
    main()
