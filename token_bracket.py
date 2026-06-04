#!/usr/bin/env python3
"""
Per-site token/cost + time + turns bracket tool for practice-testing runs.

Snapshot format v2 (JSON, per-session isolated — use --session flag):
    {"v":2,"ts":TS,"sf":"/path/session.jsonl","so":OFFSET}
    Diff reads ONLY that file from OFFSET onwards → immune to parallel-session
    cross-contamination. Correct for parallel CLI agents.

Snapshot format v1 (legacy comma-separated — global, NOT safe for parallel runs):
    ts,input,write,read,output,msg_count   (6 values)
    ts,input,write,read,output             (5 values)
    input,write,read,output                (4 values)

Usage:
    python3 token_bracket.py --snapshot --session     # v2 per-session (recommended for CLI)
    python3 token_bracket.py --snapshot --time        # v1 global with timestamp (legacy)
    python3 token_bracket.py --snapshot               # v1 global no timestamp (legacy)
    python3 token_bracket.py --diff "BASE"            # auto-detects v1 or v2
    python3 token_bracket.py --diff "BASE" --json     # machine-readable

Workflow — CLI agents (parallel-safe):
    BASE=$(python3 token_bracket.py --snapshot --session)
    # next bash call: run CLI test
    vibium go URL && vibium map && ...
    python3 token_bracket.py --diff "$BASE" --json

Workflow — MCP agents (sequential, either mode works):
    BASE=$(python3 token_bracket.py --snapshot --session)
    # MCP tool calls follow
    python3 token_bracket.py --diff "$BASE" --json

claude-sonnet-4-6 pricing (per 1M tokens):
    Input (non-cached):       $3.00
    Cache write (ephemeral):  $3.75
    Cache read:               $0.30
    Output:                  $15.00
"""

import json
import glob
import os
import sys
import time
import argparse
from pathlib import Path

PRICE_INPUT  = 3.00  / 1_000_000
PRICE_WRITE  = 3.75  / 1_000_000
PRICE_READ   = 0.30  / 1_000_000
PRICE_OUTPUT = 15.00 / 1_000_000

MODEL = "sonnet-4-6"


# ---------------------------------------------------------------------------
# JSONL helpers
# ---------------------------------------------------------------------------

def _all_jsonl_files():
    pattern = str(Path.home() / ".claude" / "projects" / "**" / "*.jsonl")
    return glob.glob(pattern, recursive=True)


def _parse_file(filepath, start_offset=0):
    """
    Parse token usage entries from one JSONL file starting at byte offset.
    Returns dict of {msg_id: usage_dict}.
    """
    seen = {}
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            if start_offset:
                f.seek(start_offset)
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = entry.get("message", {})
                if not isinstance(msg, dict):
                    continue
                if MODEL not in msg.get("model", ""):
                    continue
                msg_id = msg.get("id")
                if not msg_id:
                    continue
                usage = msg.get("usage")
                if not isinstance(usage, dict):
                    continue
                seen[msg_id] = usage
    except (OSError, IOError):
        pass
    return seen


def _sum_usage(seen):
    inp = write = read = out = 0
    for u in seen.values():
        inp   += u.get("input_tokens", 0)
        write += u.get("cache_creation_input_tokens", 0)
        read  += u.get("cache_read_input_tokens", 0)
        out   += u.get("output_tokens", 0)
    return inp, write, read, out, len(seen)


def read_totals_global():
    """Sum tokens across ALL sessions (legacy v1 behavior)."""
    seen = {}
    for fpath in _all_jsonl_files():
        seen.update(_parse_file(fpath))
    return _sum_usage(seen)


def read_totals_session(filepath, start_offset=0):
    """Sum tokens from ONE session file, optionally from a byte offset."""
    seen = _parse_file(filepath, start_offset)
    return _sum_usage(seen)


# ---------------------------------------------------------------------------
# Session file detection
# ---------------------------------------------------------------------------

def find_current_session_file():
    """
    Return the JSONL file belonging to the current Claude session.

    Heuristic: the file most recently modified. This works because the current
    session just wrote a message (the LLM call that generated this bash command)
    making its file the newest on disk.
    """
    files = _all_jsonl_files()
    if not files:
        return None
    return max(files, key=lambda f: os.path.getmtime(f))


# ---------------------------------------------------------------------------
# Snapshot encode / decode
# ---------------------------------------------------------------------------

def make_snapshot_v2(session_file):
    """
    Build a v2 JSON snapshot string.
    Records: timestamp, session file path, current EOF offset.
    No token counts needed — diff reads new messages from the file directly.
    """
    offset = os.path.getsize(session_file) if os.path.exists(session_file) else 0
    snap = {
        "v": 2,
        "ts": int(time.time() * 1000),
        "sf": session_file,
        "so": offset,
    }
    return json.dumps(snap, separators=(",", ":"))


def make_snapshot_v1(include_time=False):
    """Build a legacy v1 comma-separated snapshot string (global totals)."""
    inp, write, read, out, msg_count = read_totals_global()
    parts = [inp, write, read, out, msg_count]
    if include_time:
        parts = [int(time.time() * 1000)] + parts
    return ",".join(str(p) for p in parts)


def parse_snapshot(s):
    """
    Detect v1 vs v2 and return a dict with keys:
      version, ts (or None), session_file (or None), session_offset (or None),
      base_tokens ((inp, write, read, out) or None), base_msg_count (or None)
    """
    s = s.strip()
    # v2: JSON object
    if s.startswith("{"):
        d = json.loads(s)
        if d.get("v") == 2:
            return {
                "version": 2,
                "ts": d.get("ts"),
                "session_file": d["sf"],
                "session_offset": d["so"],
                "base_tokens": None,
                "base_msg_count": None,
            }
        raise ValueError(f"Unknown JSON snapshot version: {d}")

    # v1: comma-separated
    parts = s.split(",")
    n = len(parts)
    if n == 4:
        return {"version": 1, "ts": None,
                "base_tokens": tuple(int(p) for p in parts),
                "base_msg_count": None,
                "session_file": None, "session_offset": None}
    elif n == 5:
        ts = int(parts[0])
        return {"version": 1, "ts": ts,
                "base_tokens": tuple(int(p) for p in parts[1:]),
                "base_msg_count": None,
                "session_file": None, "session_offset": None}
    elif n == 6:
        ts = int(parts[0])
        return {"version": 1, "ts": ts,
                "base_tokens": tuple(int(p) for p in parts[1:5]),
                "base_msg_count": int(parts[5]),
                "session_file": None, "session_offset": None}
    raise ValueError(f"Expected 4/5/6 comma-separated values or JSON, got {n}: {s!r}")


# ---------------------------------------------------------------------------
# Cost helper
# ---------------------------------------------------------------------------

def cost(inp, write, read, out):
    return inp * PRICE_INPUT + write * PRICE_WRITE + read * PRICE_READ + out * PRICE_OUTPUT


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--snapshot", action="store_true",
                       help="Print baseline snapshot string")
    group.add_argument("--diff", metavar="BASE",
                       help="Compute delta from snapshot string")
    parser.add_argument("--time", action="store_true",
                        help="Include timestamp in v1 snapshot (with --snapshot)")
    parser.add_argument("--session", action="store_true",
                        help="Use per-session v2 snapshot (parallel-safe, with --snapshot)")
    parser.add_argument("--json", action="store_true",
                        help="Output diff as JSON (with --diff)")
    args = parser.parse_args()

    # ---- SNAPSHOT ----
    if args.snapshot:
        if args.session:
            sf = find_current_session_file()
            if not sf:
                print("{}", file=sys.stderr)
                sys.exit(1)
            print(make_snapshot_v2(sf))
        else:
            print(make_snapshot_v1(include_time=args.time))
        return

    # ---- DIFF ----
    snap = parse_snapshot(args.diff)

    if snap["version"] == 2:
        # Per-session: read only new messages in the session file
        sf = snap["session_file"]
        so = snap["session_offset"]
        d_input, d_write, d_read, d_output, d_turns = read_totals_session(sf, so)
        elapsed = int(time.time() * 1000) - snap["ts"] if snap["ts"] else None

    else:
        # v1 global (legacy)
        cur_inp, cur_write, cur_read, cur_out, cur_msg = read_totals_global()
        base = snap["base_tokens"]
        d_input  = cur_inp   - base[0]
        d_write  = cur_write - base[1]
        d_read   = cur_read  - base[2]
        d_output = cur_out   - base[3]
        d_turns  = (cur_msg - snap["base_msg_count"]
                    if snap["base_msg_count"] is not None else None)
        elapsed  = (int(time.time() * 1000) - snap["ts"]
                    if snap["ts"] else None)

    d_cost = cost(d_input, d_write, d_read, d_output)

    if args.json:
        result = {
            "input":       d_input,
            "cache_write": d_write,
            "cache_read":  d_read,
            "output":      d_output,
            "cost_usd":    round(d_cost, 6),
        }
        if snap["version"] == 2:
            result["turns"] = d_turns
        elif d_turns is not None:
            result["turns"] = d_turns
        if elapsed is not None:
            result["elapsed_ms"] = elapsed
        print(json.dumps(result))
    else:
        total_tok = d_input + d_write + d_read + d_output
        time_str  = f"time:{elapsed:>7}ms  " if elapsed else ""
        turns_str = f"  turns:{d_turns:>4}" if d_turns is not None else ""
        print(
            f"{time_str}input:{d_input:>8}  write:{d_write:>8}  "
            f"read:{d_read:>9}  output:{d_output:>7}  "
            f"total:{total_tok:>9}  cost:${d_cost:.4f}{turns_str}"
        )


if __name__ == "__main__":
    main()
