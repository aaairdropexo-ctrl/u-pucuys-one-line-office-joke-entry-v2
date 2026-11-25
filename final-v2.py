#!/usr/bin/env python3
"""Final: C2 vs C4 — both beat champion F 2-0 in the champion test.
Winner of this 2-call final (both orders) is the v2 entry.
Judge = z-ai/glm-5.3-flash, margin 1-5, kit criteria order.
"""
import json
import re
import subprocess
import sys
import time

import importlib.util
_spec = importlib.util.spec_from_file_location(
    "tournament_v2",
    "/home/hatch/workspace/makefun/u-pucuys-one-line-office-joke-entry-v2/tournament-v2.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
CANDIDATES, PROMPT, judge = _mod.CANDIDATES, _mod.PROMPT, _mod.judge

results = []
for a_key, b_key in (("C2", "C4"), ("C4", "C2")):
    res = judge(a_key, b_key)
    results.append(res)
    print(f"{a_key} vs {b_key}: winner={res['winner']} margin={res['margin']} :: {res['reason']}", flush=True)
    time.sleep(2)

wins = {"C2": 0, "C4": 0}
margins = {"C2": 0, "C4": 0}
for r in results:
    if r["winner"]:
        wins[r["winner"]] += 1
        margins[r["winner"]] += r["margin"]
print("FINAL WINS:", wins)
print("FINAL MARGIN SUM:", margins)

with open("/home/hatch/workspace/makefun/u-pucuys-one-line-office-joke-entry-v2/tournament-v2.json") as f:
    summary = json.load(f)
summary["final"] = {"matches": results, "wins": wins, "margin_sum": margins}
with open("/home/hatch/workspace/makefun/u-pucuys-one-line-office-joke-entry-v2/tournament-v2.json", "w") as f:
    json.dump(summary, f, indent=2)
