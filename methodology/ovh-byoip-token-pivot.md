# The OVH BYOIP token pivot (NOVEL)

## Why it works

To import a range through OVH Bring Your Own IP, the customer generates a validation certificate (token) in its OVH account. The token must be published in the range's registry object. For IPXO-leased RIPE space, IPXO writes it into the inetnum `descr` field (PUBLISHED, IPXO knowledge base).

A token is tied to the OVH account that generated it. **Every range carrying the same token was imported by the same OVH customer.**

## Steps

1. Pull the RIPE inetnum for a known fleet block. Copy the long hex string from `descr`.
2. Search the RIPE database full-text index for the token. Each hit is another range imported by the same account.
3. Use the version history (`/versions/<n>`) to see when the token was written. A burst of edits within minutes points to one setup session.
4. Use routing history to confirm when each range began to be announced by AS16276.
5. Cross-check with TLS: a certificate naming a native OVH server's IP, served on an imported address, shows which server the range was routed to.

## Result in this case

- 8 ranges, 1 token, written between 14:32:17 and 14:53:17 UTC on 2026-07-17.
- Announced by AS16276 from 2026-07-18.
- 89.40.83.0/24 routed to `ns3066510` (79.137.70.8), shown by its Kafka certificate.

## Limits

- The token identifies an **account**, not a person. Only OVH can map the account to a customer.
- Tokens can be removed when a lease ends. Use the version history, not only the current object.
- Leasing identities, such as "Company 6a53796d6yVdFmVm", are placeholders, not operators.
