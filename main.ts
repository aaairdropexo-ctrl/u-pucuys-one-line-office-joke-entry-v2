import { mkdirSync, writeFileSync } from "node:fs";

// One-line office joke, v2: the challenger that dethroned champion F.
// C4 beat F 2-0 in the champion test (margins 2 and 3), then beat C2
// 1-1 on total margin (3 vs 2) in the final between the two 2-0 winners.
const line =
  "I set my status to \"focusing\" so nobody would message me, and my manager just booked a meeting to discuss my focus.";

// The gate only accepts 1-200 characters of non-whitespace UTF-8 text.
// Refuse to write anything outside that window instead of shipping
// an entry the scorer would mark invalid.
if (line.length < 1 || line.length > 200 || line.trim().length === 0) {
  throw new Error("line must be 1-200 non-whitespace characters");
}

mkdirSync("/output", { recursive: true });
writeFileSync("/output/entry.txt", line, "utf8");
