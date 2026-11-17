"""Command-line interface for explicit local state and fixture files."""
import argparse
import json
import sys
from . import core


def main(argv=None):
    parser = argparse.ArgumentParser(prog="kwvp-core")
    parser.add_argument("--state", required=True, help="explicit local state directory")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("ingest", "evaluate"):
        p = sub.add_parser(name)
        p.add_argument("file")
    for name in ("refine", "list", "demo"):
        sub.add_parser(name)
    p = sub.add_parser("promote")
    p.add_argument("hash", help="SHA-256 of the reviewed current draft")
    p = sub.add_parser("recall")
    p.add_argument("query")
    args = parser.parse_args(argv)
    try:
        if args.command == "evaluate":
            result = core.evaluate(core.read_jsonl(args.file, core.validate_judgment))
            print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        state = core.load(args.state)
        if args.command in ("ingest", "demo"):
            if args.command == "demo":
                events = [{"schema_version": 1, "id": "example1", "session_id": "session1", "kind": "Decision", "text": "Use staged rollout for releases", "tags": ["rollout"]}]
            else:
                events = core.read_jsonl(args.file, core.validate_event)
            core.ingest(state, events)
            if args.command == "demo":
                core.refine(state)
            core.save(args.state, state)
            result = state["drafts"] if args.command == "demo" else {"events": len(state["events"])}
        elif args.command == "refine":
            result = core.refine(state)
            core.save(args.state, state)
        elif args.command == "list":
            result = state
        elif args.command == "promote":
            core.promote(state, args.hash)
            core.save(args.state, state)
            result = {"approved_hash": args.hash}
        elif args.command == "recall":
            result = core.recall(state, args.query)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print("error: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
