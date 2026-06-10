#!/usr/bin/env python3
"""fab — single entry point for the Agent-Fabric toolchain.

One command, subcommands for each stage. Thin dispatcher over the same module
mains, so `fab compile` == `afc`, `fab query` == `bql`, `fab sim` == `sim`.

    fab compile EXAMPLE.af [--validate] [-o out.json]   # author  (afc)
    fab query   GRAPH.json "QUERY" [--events ...]        # query   (bql)
    fab sim     BASE.json EVENTS.json [--explode] ...    # emulate (sim)
    fab test                                             # run the e2e suite

Pure standard library; no install.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

USAGE = __doc__


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]

    if cmd in ("compile", "afc", "author"):
        import afc
        return afc.main(rest)
    if cmd in ("query", "bql"):
        import bql
        return bql.main(rest)
    if cmd in ("sim", "emulate", "rebuild"):
        import sim
        return sim.main(rest)
    if cmd in ("test", "e2e"):
        import runpy
        try:
            runpy.run_path(os.path.join(ROOT, "tests", "e2e.py"), run_name="__main__")
        except SystemExit as exc:
            return exc.code or 0
        return 0

    print(f"fab: unknown command {cmd!r}\n", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
