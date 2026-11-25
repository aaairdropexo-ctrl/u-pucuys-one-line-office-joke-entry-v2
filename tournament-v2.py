#!/usr/bin/env python3
"""Champion test for office-joke v2: champion F vs 4 challengers.
Judge = z-ai/glm-5.3-flash on OpenRouter (the kit's actual jury model).
Method mirrors the kit: pairwise, BOTH directions, no tie, margin 1-5,
criteria in kit order. One attempt per match (OpenRouter free budget
is nearly used today); a failed call is recorded as failed, not retried.
A challenger becomes v2 only by beating F head-to-head: 2-0, or 1-1
with a bigger total margin.
"""
import json
import re
import subprocess
import time

HELPER = "/home/hatch/workspace/custom-connectors/custom.openrouter/bin/openrouter_call.py"
MODEL = "z-ai/glm-5.3-flash"

CHAMPION = "F"
CANDIDATES = {
    "F": 'I set my status to "in a meeting" so I could eat lunch at my desk in peace, and now three people want to join the meeting.',
    "C1": "I spent the whole call on mute rehearsing the perfect point, unmuted to deliver it, and found out the meeting had ended ten minutes ago.",
    "C2": "I turned on my out-of-office reply to escape email for a day, and it has now started a three-email argument with another auto-reply.",
    "C3": 'I set my status to "away" so I could think in peace, and the app helpfully told my boss I have been away for three hours.',
    "C4": 'I set my status to "focusing" so nobody would message me, and my manager just booked a meeting to discuss my focus.',
}

PROMPT = """You are judging entries for the competition 'One-Line Office Joke: 24-Hour Sprint'. Two entries are shown as A and B. Judge them by these criteria, in this order: (1) Is it a one-line joke about office life, a single line that lands as a joke about working in an office? (2) Is it funny: does the punchline surprise and pay off the setup in a way anyone who has sat in an office recognises? (3) Is it one line: the whole joke reads as a single sentence, or a setup and punchline on one line, with no rambling around it? (4) Is it fresh: does it find a specific detail of office life rather than a generic complaint, and is it not a joke everyone has already heard? (5) Is it clear on first read: no explanation needed, no reference the reader cannot follow, and the wording is tight? Either joke may be dry, silly or absurd. Pick exactly one winner. No tie is allowed. Give a margin from 1 (by a hair) to 5 (overwhelmingly better). Reply in exactly this format, nothing else:
Winner: A
Margin: 3
Reason: <one short sentence>

Entry A: {a}
Entry B: {b}"""


def judge(a_key, b_key):
    prompt = PROMPT.format(a=CANDIDATES[a_key], b=CANDIDATES[b_key])
    r = subprocess.run(
        ["python3", HELPER, "chat", MODEL, prompt, "2500"],
        capture_output=True, text=True, timeout=180,
    )
    out = r.stdout + r.stderr
    content = None
    try:
        data = json.loads(r.stdout)
        content = data["choices"][0]["message"]["content"]
    except Exception:
        pass
    if not content:
        m = re.search(r'"content":\s*"((?:[^"\\]|\\.)*)"', out)
        if m:
            try:
                content = json.loads('"' + m.group(1) + '"')
            except Exception:
                content = None
    if content:
        wm = re.search(r"Winner:\s*([AB])", content)
        mm = re.search(r"Margin:\s*([1-5])", content)
        rm = re.search(r"Reason:\s*(.+)", content)
        if wm and mm:
            return {
                "a": a_key, "b": b_key,
                "winner_side": wm.group(1),
                "winner": a_key if wm.group(1) == "A" else b_key,
                "margin": int(mm.group(1)),
                "reason": rm.group(1).strip()[:200] if rm else "",
                "raw": content.strip()[:500],
            }
    return {"a": a_key, "b": b_key, "winner": None, "margin": 0,
            "reason": "CALL FAILED", "raw": out[:500]}


def main():
    results = []
    for challenger in ("C1", "C2", "C3", "C4"):
        for a_key, b_key in ((CHAMPION, challenger), (challenger, CHAMPION)):
            res = judge(a_key, b_key)
            results.append(res)
            print(f"{a_key} vs {b_key}: winner={res['winner']} margin={res['margin']} :: {res['reason']}", flush=True)
            time.sleep(2)
    wins = {k: 0 for k in CANDIDATES}
    margins = {k: 0 for k in CANDIDATES}
    for r in results:
        if r["winner"]:
            wins[r["winner"]] += 1
            margins[r["winner"]] += r["margin"]
    summary = {"matches": results, "wins": wins, "margin_sum": margins}
    with open("/home/hatch/workspace/makefun/u-pucuys-one-line-office-joke-entry-v2/tournament-v2.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("WINS:", wins)
    print("MARGIN SUM:", margins)


if __name__ == "__main__":
    main()
