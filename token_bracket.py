#!/usr/bin/env python3
"""
Per-site token/cost + time + turns bracket tool for practice-testing runs.

Usage:
    python3 token_bracket.py --snapshot               # token baseline only
    python3 token_bracket.py --snapshot --time        # token baseline + timestamp + turn count
    python3 token_bracket.py --diff "BASE"            # delta (time + turns shown if BASE has them)
    python3 token_bracket.py --diff "BASE" --json     # machine-readable delta

Snapshot string format (comma-separated):
    4 values:  input,write,read,output                        (legacy — no ts, no turns)
    5 values:  ts,input,write,read,output                     (legacy — no turns)
    6 values:  ts,input,write,read,output,msg_count           (current — includes turns)

Workflow (CLI phase — snapshot MUST be a separate preliminary bash call):
    BASE=$(python3 token_bracket.py --snapshot --time)
    # next bash call: generate + execute CLI test (cost now inside bracket)
    vibium stop; vibium go URL && vibium map && ...
    # then diff:
    python3 token_bracket.py --diff "$BASE" --json

Workflow (MCP phase — snapshot already correct as separate call):
    BASE=$(python3 token_bracket.py --snapshot --time)
    # MCP tool calls follow in next Claude turn
    python3 token_bracket.py --diff "$BASE" --json

claude-sonnet-4-6 pricing (per 1M tokens):
    Input (non-cached):          $3.00
    Cache write (ephemeral):     $3.75
    Cache read:                  $0.30
    Output:                     $15.00
"""

import json
import glob
import sys
import time
import argparse
from pathlib import Path

PRICE_INPUT  = 3.00 / 1_000_000
PRICE_WRITE  = 3.75 / 1_000_000
PRICE_READ   = 0.30 / 1_000_000
PRICE_OUTPUT = 15.00 / 1_000_000

MODEL = "sonnet-4-6"


def read_totals():
    """
    Read all jsonl files, deduplicate by message.id (last occurrence wins),
    filter to claude-sonnet-4-6, and return summed token counts + message count.
    Returns (input, cache_write, cache_read, output, msg_count).
    """
    seen = {}  # message_id → usage dict (last occurrence wins)

    pattern = str(Path.home() / ".claude" / "projects" / "**" / "*.jsonl")
    for fpath in glob.glob(pattern, recursive=True):
        try:
            with open(fpath, encoding="utf-8", errors="replace") as f:
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

                    model = msg.get("model", "")
                    if MODEL not in model:
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

    total_input = total_write = total_read = total_output = 0
    for usage in seen.values():
        total_input  += usage.get("input_tokens", 0)
        total_write  += usage.get("cache_creation_input_tokens", 0)
        total_read   += usage.get("cache_read_input_tokens", 0)
        total_output += usage.get("output_tokens", 0)

    return total_input, total_write, total_read, total_output, len(seen)


def cost(inp, write, read, out):
    return inp * PRICE_INPUT + write * PRICE_WRITE + read * PRICE_READ + out * PRICE_OUTPUT


def snapshot_str(totals, include_time=False):
    """
    totals: (input, write, read, output, msg_count)
    Emits: ts,input,write,read,output,msg_count  (with --time)
           input,write,read,output,msg_count      (without --time)
    """
    inp, write, read, out, msg_count = totals
    parts = [inp, write, read, out, msg_count]
    if include_time:
        parts = [int(time.time() * 1000)] + parts
    return ",".join(str(p) for p in parts)


def parse_snapshot(s):
    """
    Returns (ts_ms_or_None, (input, write, read, output), msg_count_or_None).

    Handles all three formats:
      4 values: input,write,read,output              (legacy)
      5 values: ts,input,write,read,output           (legacy with timestamp)
      6 values: ts,input,write,read,output,msg_count (current)
    """
    parts = s.strip().split(",")
    n = len(parts)
    if n == 4:
        return None, tuple(int(p) for p in parts), None
    elif n == 5:
        ts = int(parts[0])
        tokens = tuple(int(p) for p in parts[1:])
        return ts, tokens, None
    elif n == 6:
        ts = int(parts[0])
        tokens = tuple(int(p) for p in parts[1:5])
        msg_count = int(parts[5])
        return ts, tokens, msg_count
    raise ValueError(f"Expected 4, 5, or 6 comma-separated values, got {n}: {s!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--snapshot", action="store_true", help="Print baseline snapshot string")
    group.add_argument("--diff", metavar="BASE", help="Compute delta from snapshot string")
    parser.add_argument("--time", action="store_true", help="Include timestamp in snapshot (with --snapshot)")
    parser.add_argument("--json", action="store_true", help="Output diff as JSON (with --diff)")
    args = parser.parse_args()

    if args.snapshot:
        totals = read_totals()
        print(snapshot_str(totals, include_time=args.time))
        return

    # --diff mode
    base_ts, base_tok, base_msg_count = parse_snapshot(args.diff)
    cur = read_totals()  # (input, write, read, output, msg_count)

    d_input  = cur[0] - base_tok[0]
    d_write  = cur[1] - base_tok[1]
    d_read   = cur[2] - base_tok[2]
    d_output = cur[3] - base_tok[3]
    d_cost   = cost(d_input, d_write, d_read, d_output)
    elapsed  = int(time.time() * 1000) - base_ts if base_ts else None
    d_turns  = cur[4] - base_msg_count if base_msg_count is not None else None

    if args.json:
        result = {
            "input":       d_input,
            "cache_write": d_write,
            "cache_read":  d_read,
            "output":      d_output,
            "cost_usd":    round(d_cost, 6),
        }
        if d_turns is not None:
            result["turns"] = d_turns
        if elapsed is not None:
            result["elapsed_ms"] = elapsed
        print(json.dumps(result))
    else:
        total_tok = d_input + d_write + d_read + d_output
        time_str  = f"time:{elapsed:>7}ms  " if elapsed is not None else ""
        turns_str = f"  turns:{d_turns:>4}" if d_turns is not None else ""
        print(f"{time_str}input:{d_input:>8}  write:{d_write:>8}  read:{d_read:>9}  "
              f"output:{d_output:>7}  total:{total_tok:>9}  cost:${d_cost:.4f}{turns_str}")


if __name__ == "__main__":
    main()
