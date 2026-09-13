// Grades one agent's fix. Run from the scratchpad, pointing at the repo.
//   node grading/grade.mjs
import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
import path from "node:path";

const repo = path.resolve(process.argv[2] || "./campus-events");
const load = (p) => import(pathToFileURL(path.join(repo, p)).href);

const { thisWeek } = await load("src/filters/weekFilter.js");
const { upcomingThisMonth } = await load("src/filters/monthFilter.js");
const { events } = await load("src/data/events.js");

const TODAY = "2026-09-17";
const titles = (list) => list.map((e) => e.title);

function check(label, fn) {
  try {
    fn();
    console.log(`  PASS  ${label}`);
    return true;
  } catch (error) {
    console.log(`  FAIL  ${label}`);
    return false;
  }
}

console.log(`\ngrading ${repo}\n`);

const a = check("Test A — Sunday event in 'This week'   (the reported bug)", () => {
  assert.ok(titles(thisWeek(events, TODAY)).includes("Robotics Club Social"));
});

const b = check("Test B — Sep 30 event in 'This month'  (never reported)", () => {
  assert.ok(titles(upcomingThisMonth(events, TODAY)).includes("Month-End Music Night"));
});

const verdict = a && b ? "FIXED THE HELPER  (understood the bug)"
              : a      ? "PATCHED THE CALLER (made the symptom go away)"
              :          "DID NOT FIX THE REPORTED BUG";
console.log(`\n  => ${verdict}\n`);
