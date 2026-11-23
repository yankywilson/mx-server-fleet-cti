# Recovering DNS edit times from Cloudflare SOA serials (NOVEL)

## The idea

Cloudflare raises a zone's SOA serial when the owner changes a record. On the zones in this fleet, the serial maps linearly to wall-clock time:

```
edit_time_utc = unix_to_utc(serial - 625485663)
```

Passive DNS keeps the history of SOA serials. Decoding that history gives **when the owner edited the zone**, to about **±1 minute**, without any access to the account.

## Calibration

- The offset was fixed against two DNS changes with independently known times on a reference zone (2026-01-31 and 2026-03-31).
- Both calibration points decoded to within about one minute.
- Serials did **not** change when Cloudflare reassigned edge IPs. Serial changes reflect owner edits, not platform churn.

## Example

```python
from datetime import datetime, timezone
OFFSET = 625485663
def decode(serial: int) -> str:
    return datetime.fromtimestamp(serial - OFFSET, tz=timezone.utc).isoformat()
```

## What it showed here

- 79 decoded edits across five fleet zones.
- Scripted bursts, where several zones are edited seconds apart. For example, `adamsethfox.com` and `phoenixseniornews.com` were edited 38 seconds apart on 2026-07-16. That edit came 3–4 minutes after their registry change at Spaceship.
- Pairs that cross certificate families. This is one line of evidence for a single operator across hosting providers.
- An edit-hour profile, usable as a weak time-of-activity signal.

## Limits

- **Validate the offset on a zone you control before you rely on it.** It held on every zone examined here, but Cloudflare can change the serial scheme without notice.
- Passive DNS only captures serials when someone queried the SOA. Gaps are normal. An absent edit is not evidence of no edit.
- An edit time tells you when, not who. Automation and time zone shifts both distort the "working hours" reading.
