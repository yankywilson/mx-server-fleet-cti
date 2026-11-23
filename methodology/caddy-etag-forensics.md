# Caddy ETag forensics

**Purpose.** Recover the exact time a file was written on a Caddy web server, from a passive scan.

**Principle.** For static files, Caddy builds the ETag from two numbers written in base 36: the file's **modification time in nanoseconds** and its **size in bytes**. The two parts are joined with no separator. Scanners record the ETag in the HTTP headers, so no connection to the target is needed.

```text
ETag: "dkb1fqjbnd35ce"
        └──────┬─────┘└┬┘
   mtime (ns, base36)  size (base36)
   dkb1fqjbnd3 → 2026-07-29 12:02:12.611 UTC
                5ce → 446 bytes
```

## Steps

1. **Collect** the ETag and `Content-Length` from Shodan, FOFA, Validin or Censys HTTP data.
2. **Decode** with [`../tools/caddy_etag.py`](../tools/caddy_etag.py). The tool tries each split point, keeps splits where the size part matches `Content-Length` (if given) and the time part falls in 2000–2100, and strips a `W/` weak prefix.

```text
$ python3 tools/caddy_etag.py '"dkb1fqjbnd35ce"' '"dkb1fv87lqycce"' --content-length 446
"dkb1fqjbnd35ce"	mtime_utc=2026-07-29T12:02:12.611218+00:00	size=446
"dkb1fv87lqycce"	mtime_utc=2026-07-29T12:02:22.823208+00:00	size=446

Ordered by write time (delta from first):
  +     0.000s  "dkb1fqjbnd35ce"  size=446
  +    10.212s  "dkb1fv87lqycce"  size=446
```

3. **Compare across hosts.** The same file written seconds apart on different servers means one deployment run. Hours or days apart means separate runs.

## Checks

| Check | Why |
|---|---|
| `Last-Modified` header matches the decoded time to the second | Confirms the decode |
| Size part equals `Content-Length` | Confirms the split point |
| Same body hash on both hosts | Confirms it is the same file |

## Limits

- Works for files Caddy serves from disk. Responses from reverse-proxied back ends carry the back end's ETag.
- `mtime` is the write time on that host. Copying with time preserved (`rsync -t`, `cp -p`) carries the source time. Either way, two hosts 10 s apart show one coordinated action.

## Result in this case

Two hosts, one new node and one broker, wrote the same 446-byte page **10.2 seconds apart** on 2026-07-29. See [`../docs/technical-analysis.md`](../docs/technical-analysis.md) §13.
