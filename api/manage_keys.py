#!/usr/bin/env python3
"""Create, list, and revoke Agent-Fabric API keys.

    python api/manage_keys.py create --customer domain:acme [--tier provider] [--label "acme prod"]
    python api/manage_keys.py list
    python api/manage_keys.py revoke <raw-key>

`--tier` mirrors the Partnership Model tiers in docs/partnership-model.md, so
a key's access can later be scoped by the same vocabulary the partnership
contracts use, instead of inventing a separate one for the API.

The raw key is printed exactly once, at creation time. Only its SHA-256 hash
is ever persisted (see api/keystore.py) — losing the printed value means
issuing a new key, not recovering the old one.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import keystore  # noqa: E402

TIERS = [
    "vendor", "provider", "certifiedProvider", "deliveryPartner",
    "strategicPartner", "ecosystemPartner",
]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="issue a new API key")
    p_create.add_argument("--customer", required=True,
                          help="customer/tenant id, e.g. domain:acme")
    p_create.add_argument("--tier", default="provider", choices=TIERS)
    p_create.add_argument("--label", default=None)

    sub.add_parser("list", help="list issued keys (metadata only, no raw keys)")

    p_revoke = sub.add_parser("revoke", help="revoke a key")
    p_revoke.add_argument("raw_key")

    args = ap.parse_args(argv)

    if args.cmd == "create":
        result = keystore.create_key(args.customer, args.tier, args.label)
        print("API key created — store it now, it will not be shown again:\n")
        print(f"  {result['key']}\n")
        print(f"  id:       {result['id']}")
        print(f"  customer: {result['customer']}")
        print(f"  tier:     {result['tier']}")
        return 0

    if args.cmd == "list":
        rows = keystore.list_keys()
        if not rows:
            print("no keys issued yet")
            return 0
        for row in rows:
            state = "revoked" if row["revokedAt"] else "active"
            print(f"{row['id']}  {row['customer']:<28} {row['tier']:<18} "
                  f"{state:<8} {row['label'] or ''}")
        return 0

    if args.cmd == "revoke":
        ok = keystore.revoke_key(args.raw_key)
        print("revoked" if ok else "no matching active key found")
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
