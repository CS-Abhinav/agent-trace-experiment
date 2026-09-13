import assert from "node:assert/strict";
import { thisWeek } from "../src/filters/weekFilter.js";
import { events } from "../src/data/events.js";

// 2026-09-17 is a Thursday. Its week runs Mon 14th to Sun 20th.
const TODAY = "2026-09-17";

let failures = 0;
function test(name, fn) {
  try {
    fn();
    console.log(`  PASS  ${name}`);
  } catch (error) {
    failures += 1;
    console.log(`  FAIL  ${name}`);
    console.log(`        ${error.message.split("\n")[0]}`);
  }
}
const titles = (list) => list.map((e) => e.title);

console.log("\nweek filter");

test("includes an event in the middle of the week", () => {
  assert.ok(titles(thisWeek(events, TODAY)).includes("Debate Society Open Floor"));
});

test("excludes an event from next month", () => {
  assert.ok(!titles(thisWeek(events, TODAY)).includes("Freshers Mixer"));
});

test("includes an event on the last day of the week (Sun 20th)", () => {
  assert.ok(
    titles(thisWeek(events, TODAY)).includes("Robotics Club Social"),
    'expected "Robotics Club Social" (2026-09-20) in the This week list'
  );
});

console.log(failures === 0 ? "\nall tests passed\n" : `\n${failures} failing\n`);
process.exit(failures === 0 ? 0 : 1);
