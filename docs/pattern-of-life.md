# Pattern of life and the nationality question (v2.0)

**Bottom line.** Attribution not supported. The operator's activity times do not show a working day in any time zone. This is a null result, and it is reported as a finding.

## Data

- **86 operator-side events**, 2025-10-25 to 2026-11-12.
- 77 are DNS edits decoded from Cloudflare SOA serials ([`../methodology/cloudflare-soa-serial-decoding.md`](../methodology/cloudflare-soa-serial-decoding.md)).
- 9 are other timestamped operator actions: registry changes, certificate minting and IRR object creation.
- File: [`../data/operator_event_times_utc.txt`](../data/operator_event_times_utc.txt). Tool: [`../tools/pattern_of_life.py`](../tools/pattern_of_life.py).

## Method

For each UTC offset from −11 to +12, count the events that fall in a local **day window (09:00–21:00)** and a local **night window (01:00–07:00)**.

- A random 24/7 spread puts **about 50%** of events in any 12-hour window.
- A human operator in one time zone usually puts **75% or more** in the day window, with quiet nights.

## Result

| Measure | Value |
|---|---|
| Best day-window fit | **64%** (UTC−6 and UTC−2, tied) |
| Night events at the best fit | 24 (UTC−6) / 11 (UTC−2) |
| Weekend events | **24 of 86 (28%)**. A 7-day random spread gives 29% |
| Busiest UTC hours | 20:00–22:00 (22 events) |
| Quietest UTC hours | 03:00 and 14:00 (0 events each) |

UTC hour histogram:

```text
00 ████            12 ██████
01 ██              13 ██
02 ████            14
03                 15 ██
04 ███             16 ████
05 █               17 ████
06 █               18 ████
07 ███             19 █████
08 ███             20 ███████
09 ███             21 ████████
10 ███             22 ███████
11 ██████          23 ████
```

## Interpretation

- 64% is only 14 points above random. It is not a working day.
- Weekend activity matches a 7-day schedule. There is no weekend pause.
- Two readings fit: **automation** (scripted deploys and DNS updates), or **several operators in different time zones**.
- Each reading is a roughly even chance. Confidence is low.

## What else was checked for nationality

| Lead | Result | Tag |
|---|---|---|
| Language in certificates, pages, SMTP banners | None. Generated English adjective+noun hostnames only | NOVEL |
| Hosting and registrar choices | OVH (FR/PL), Hetzner (DE/FI), US hosting, a US registrar, a US-based leasing platform. No national pattern | NOVEL |
| A look-alike Kafka CA on Russian-hosted servers | Different CA key. Not this fleet. Closed (L1) | EXCLUDED |
| Earlier tenants of a broker IP (2019–2023) | Different operators. Closed (L2) | EXCLUDED |

## Judgment change

v1.0 said DNS edits peaked at 07–12 UTC (R2). That used a smaller set. With 86 events the peak moves to 20–22 UTC, and no offset gives a working day. The v1.0 conclusion ("undetermined") stands. The supporting detail changed. See [`retraction-log.md`](retraction-log.md).

## What would change this

- Provider records: the OVH account holder, the registrar account, the leasing platform's lessee.
- Payment data held by those providers.
- A language artifact in operator-written content.

Only providers or law enforcement can get the first two. This repository does not speculate past the data.
