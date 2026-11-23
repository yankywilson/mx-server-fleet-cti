# IRR route-object batch clustering

**Purpose.** Turn many leased prefixes into the lease orders behind them.

**Principle.** When a leasing platform provisions a customer's order, it creates the IRR `route` or `route6` objects for that order in one automated run. The objects get `created` timestamps seconds apart. Different orders, for different customers, fall on different days or hours.

## Steps

1. **Collect the objects.** Query the IRR for every route object under the parent block.

   | Source | Query |
   |---|---|
   | RADB / IRR whois | `whois -h whois.radb.net -- '-M 2602:fad4::/36'` (more-specific objects) |
   | ARIN IRR | `whois -h rr.arin.net -- '-M 2602:fad4::/36'` |
   | RIPE | `whois -h whois.ripe.net -- '-M -T route6 <prefix>'` |

2. **Keep four fields:** prefix, origin, mnt-by, created. Save as CSV ([`../data/irr_route6_2602-fad4.csv`](../data/irr_route6_2602-fad4.csv)).
3. **Cluster by time.** Run [`../tools/irr_batch_cluster.py`](../tools/irr_batch_cluster.py) with a 60-second window. Objects created within the window, with the same origin and maintainer, form one batch.

```text
$ python3 tools/irr_batch_cluster.py data/irr_route6_2602-fad4.csv --window 60
2025-10-16T11:36:38+00:00  +3s  origin=AS9009  mnt=MNT-DCL-577  objects=5  marked=0  [2602:fad4:10::/46, 2602:fad4:14::/48]
2025-12-17T20:17:09+00:00  +0s  origin=AS6079  mnt=MNT-DCL-577  objects=1  marked=0  [2602:fad4:16::/48]
2025-12-22T11:44:35+00:00  +13s  origin=AS6079  mnt=MNT-DCL-577  objects=19  marked=0  [2602:fad4:17::/48, 2602:fad4:18::/45, 2602:fad4:20::/45, 2602:fad4:28::/47]
2026-01-06T12:25:43+00:00  +90s  origin=AS215294  mnt=MNT-DCL-577  objects=3  marked=0  [2602:fad4:2a::/47, 2602:fad4:2c::/48]
…
```

Prefix lists are collapsed to the shortest covering set. Use `--mark` with a comma-separated list of observed prefixes to count hits per batch.

4. **Overlay the observations.** Mark which prefixes appear in your telemetry. If all observed prefixes fall in one batch, and none in the neighbours, the batch is one customer's order.

## What it does and does not show

| Shows | Does not show |
|---|---|
| Which prefixes were ordered together | Who the customer is |
| When the order was provisioned | Whether the customer is the attacker or a proxy seller |
| Which neighbouring prefixes are unrelated | Current use after a lease ends |

## Result in this case

All nine spray-exit /48s fall in the 19-object batch of 2025-12-22 11:44:35–48 UTC. See [`../docs/spray-infrastructure.md`](../docs/spray-infrastructure.md).
