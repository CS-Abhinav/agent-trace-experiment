# One bug, three agents

A tiny, reproducible experiment: plant one bug, hand the identical report to
several coding agents, and compare what they actually did — not just what they
produced.

The bug is a date-range off-by-one. Two homepage filters, **This week** and
**Upcoming this month**, both call one shared helper:

```js
// campus-events/src/lib/dateRange.js
export function getEventsInRange(events, start, end) {
  return events.filter((e) => e.date >= start && e.date < end);
}
```

`weekBounds()` returns Monday *through Sunday*. `monthBounds()` returns the 1st
*through the last day*. Both are inclusive ranges handed to an exclusive
comparison, so every filter silently drops its own final day.

The bug report mentions only the weekly filter. It never mentions that the
monthly filter is broken in exactly the same way.

## Run it

1. Reset, so every agent starts from the same state:

   ```
   git checkout . && git clean -fd
   ```

2. Start your agent **inside `campus-events/`** — not at the repo root. The
   grader lives outside that directory on purpose.

3. Paste [`PROMPT.txt`](PROMPT.txt) verbatim. Then say nothing. No hints, no
   answers to questions, no corrections when it looks like it's going the wrong
   way. That last part is harder than it sounds.

4. Grade it:

   ```
   node grading/grade.mjs
   ```

5. Save the patch and the agent's session transcript before resetting for the
   next one:

   ```
   cd campus-events && git diff > ../diff-<agent>.patch
   ```

Repeat for each agent.

## The two tests

With "today" pinned to Thursday 17 September 2026:

| | What it checks | Who passes |
|---|---|---|
| **Test A** | An event on Sunday the 20th appears in *This week* | any plausible fix |
| **Test B** | An event on the 30th appears in *Upcoming this month* | only a fix to the shared logic |

Test B is the whole experiment. Nobody asked for it, and it is the only thing
separating an agent that understood the bug from one that made the symptom go
away.

## Why the grader is not in the test suite

`campus-events/test/filters.test.js` covers the **weekly filter only**. Test B
lives in `grading/`, outside the directory you point the agent at.

This matters more than it sounds. If Test B ships inside the project, the first
agent to run `npm test` is handed the answer, and there is nothing left to
compare. Keep it out.

## Where the transcripts live

Each harness writes its own session file to disk as it works. Rough locations:

| Harness | Path |
|---|---|
| Claude Code | `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` |
| Copilot CLI | `~/.copilot/session-state/<uuid>/events.jsonl` |
| Cursor | `~/.cursor/projects/<project>/agent-transcripts/<id>/<id>.jsonl` |

They are all JSON and they all disagree about the details — what a tool call is
named, where its arguments live, whether reasoning is recorded at all. Reading
three of them side by side is the point of the exercise.

## Note

The three transcripts are not included here. Run your own — the interesting part
is the comparison, and results will differ.
