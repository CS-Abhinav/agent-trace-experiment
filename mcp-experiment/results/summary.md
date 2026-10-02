# Results: one MCP tool, three agents, two descriptions

18 runs on 24 September 2026, 17:08–17:12 UTC (22:38–22:42 IST). Raw evidence is in
[`raw/`](raw/). Every number below was extracted from those files by
[`../runner/extract.py`](../runner/extract.py) (output: [`extracted.json`](extracted.json)) and
checked against the raw outputs by hand.

**Prediction:** none was recorded; when asked before any run, the experimenter chose
"No prediction" ([`prediction.md`](prediction.md)).

## Setup, briefly

- **Prompt**, identical in every run:
  *"What events are happening between Monday 14 September and Sunday 20 September 2026? Please list all of them."*
- **Server:** one tool, `get_events_in_range(start, end)`, calling the app's unchanged
  exclusive-end helper. Round A description: *"Returns events between two dates."*
  Round B: *"Returns events from start up to, but NOT including, end. To include a day,
  pass the following day as end."* Nothing else differed. Checksums of the prompt,
  server, helper and data files were identical before and after all runs
  ([`raw/checksums-before-runs.txt`](raw/checksums-before-runs.txt),
  [`raw/checksums-after-runs.txt`](raw/checksums-after-runs.txt)).
- **Empty workspaces.** Each run started in its own new, empty folder,
  `/private/tmp/mcp-exp/<run>/`, outside the repo and outside the home directory (which is
  itself a git repo). The event data could only be reached through the MCP tool.
  Cursor's workspace contained one file, `.cursor/cli.json` (permissions only, no paths);
  see [Cursor caveat](#cursor-caveat).
- **Tool restrictions**, via each CLI's own mechanism (flags checked against `--help`):
  - Claude Code: `--mcp-config … --strict-mcp-config --tools "" --allowedTools mcp__campus-events__get_events_in_range`. No built-in tools at all.
  - Copilot CLI: `--additional-mcp-config … --disable-builtin-mcps --available-tools=campus-events-get_events_in_range --allow-tool=campus-events(get_events_in_range)`. The model saw only this tool.
  - Cursor CLI: global `~/.cursor/mcp.json` written for the run and deleted after; project
    `.cursor/cli.json` allowing `Mcp(campus-events:get_events_in_range)` and denying
    `Shell(*)`, `Read(**)`, `Write(**)`, `WebFetch(*)`. Cursor cannot hide its built-in tools,
    only deny them.
- **Headless, fresh sessions, clean environment** (only `HOME`, `USER`, `PATH` and similar).
  Default models, no model flag. Runs were interleaved (Claude, Copilot, Cursor, repeat)
  within each round.
- **No failed runs, no retries.** All 18 exited 0 on the first attempt.

¹ Cursor reports only `Auto`. Each Cursor run's local chat store
(`~/.cursor/chats/…/store.db`) contains the strings `cursor-grok-4.5-high` and `grok-4.5`,
but the CLI does not state which model answered, so this is **unverified**.

² Captured in Observal only after manual repair of its local outbox; see [Observal capture](#observal-capture).

## Every run

| Run | Agent | # | Round | CLI version | Model | Tool calls (agent / server log) | `start` → `end` sent | Server returned | Robotics Club Social in answer? | Boundary mentioned to user? | Observal session ID | Captured in Observal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `run-A-claude-1` | Claude Code | 1 | A | 2.1.220 | `claude-sonnet-5` | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `8d96d340-5efa-458d-b7af-685c1e32b1a7` | Yes² |
| `run-A-claude-2` | Claude Code | 2 | A | 2.1.220 | `claude-sonnet-5` | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `74d5c296-5c10-4ade-8bb8-7315ba579424` | Yes² |
| `run-A-claude-3` | Claude Code | 3 | A | 2.1.220 | `claude-sonnet-5` | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `4591fe06-8b57-4a3f-9e17-a6a81441a93c` | Yes² |
| `run-A-copilot-1` | Copilot CLI | 1 | A | 1.0.83 | auto → `gpt-5.6-luna` | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `4c9c84f9-3666-4635-93c0-ba4554c9c461` | Yes² |
| `run-A-copilot-2` | Copilot CLI | 2 | A | 1.0.83 | auto → `gpt-5.6-luna` | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `b675b052-50a1-4aef-a91f-67c86945c3a1` | Yes² |
| `run-A-copilot-3` | Copilot CLI | 3 | A | 1.0.83 | auto → `gpt-5.6-luna` | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `6cd965cc-7219-4806-bbb9-65e6558cce34` | Yes² |
| `run-A-cursor-1` | Cursor CLI | 1 | A | 2026.09.10-fd3934a | `Auto`¹ | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `88ee6eb0-d333-4895-8be4-f59c7ca23318` | Yes² |
| `run-A-cursor-2` | Cursor CLI | 2 | A | 2026.09.10-fd3934a | `Auto`¹ | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `da0d39b6-7516-4ab9-a48f-f4963f894fc5` | Yes² |
| `run-A-cursor-3` | Cursor CLI | 3 | A | 2026.09.10-fd3934a | `Auto`¹ | 1 / 1 | `2026-09-14` → `2026-09-20` | 2: Robotics Club Build Night, Debate Society Open Floor | **No** | No | `0382a1e0-3631-4995-a8bc-f95b4a6266e3` | Yes² |
| `run-B-claude-1` | Claude Code | 1 | B | 2.1.220 | `claude-sonnet-5` | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `9fb289ba-2a00-4a1c-9229-e8883421b0a8` | Yes² |
| `run-B-claude-2` | Claude Code | 2 | B | 2.1.220 | `claude-sonnet-5` | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `8a3b3dfa-aee0-4056-92b9-2340a4d0601c` | Yes² |
| `run-B-claude-3` | Claude Code | 3 | B | 2.1.220 | `claude-sonnet-5` | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `bbbc8c4b-7f17-49fb-855c-ce25d4352f0f` | Yes² |
| `run-B-copilot-1` | Copilot CLI | 1 | B | 1.0.83 | auto → `gpt-5.6-luna` | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `e31f7d0b-f055-4e19-a4d5-e3893897d562` | Yes² |
| `run-B-copilot-2` | Copilot CLI | 2 | B | 1.0.83 | auto → `gpt-5.6-luna` | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `6ee36066-4f43-43d4-8373-b48a74143c7c` | Yes² |
| `run-B-copilot-3` | Copilot CLI | 3 | B | 1.0.83 | auto → `gpt-5.6-luna` | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `f5f931e6-2ac6-49b7-8860-0f9f6e0b6808` | Yes² |
| `run-B-cursor-1` | Cursor CLI | 1 | B | 2026.09.10-fd3934a | `Auto`¹ | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `c2e53f8a-6960-46c6-aa75-11d2a3a6d364` | Yes² |
| `run-B-cursor-2` | Cursor CLI | 2 | B | 2026.09.10-fd3934a | `Auto`¹ | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `d3967083-2ed9-4429-a4d1-96d81c58aaf7` | Yes² |
| `run-B-cursor-3` | Cursor CLI | 3 | B | 2026.09.10-fd3934a | `Auto`¹ | 1 / 1 | `2026-09-14` → `2026-09-21` | 3: Robotics Club Build Night, Debate Society Open Floor, Robotics Club Social | Yes | No | `807a6212-e612-4896-96a9-e331fe069de3` | Yes² |

"Tool calls (agent / server log)" counts calls to `get_events_in_range` in the agent's own
output and `call` records in [`raw/server-log.jsonl`](raw/server-log.jsonl); they agree in
every run. Cursor additionally made one `GetDynamicTools` lookup of the tool's schema
before each call. That is Cursor's tool discovery, not a data call, and the server logged
nothing for it. No agent made any other tool call.

"Boundary mentioned to user?" was checked by reading all 18 final answers
(`final_answer` in [`extracted.json`](extracted.json)). None mentions an inclusive or
exclusive end, the 21st, or a possibly missing day.

### Session registry

Kept so experiment sessions cannot be confused with the orchestrating Claude Code
session (`23708334-3f45-49d9-9656-4d6a7d466d88`, working directory `~`), which is
excluded from all results.

| Run | Session ID | Started (UTC) | Finished (UTC) | Workspace | Exit |
|---|---|---|---|---|---|
| `run-A-claude-1` | `8d96d340-5efa-458d-b7af-685c1e32b1a7` | 2026-09-24 17:08:26 | 17:08:32 | `/private/tmp/mcp-exp/run-A-claude-1` | 0 |
| `run-A-claude-2` | `74d5c296-5c10-4ade-8bb8-7315ba579424` | 2026-09-24 17:08:56 | 17:09:02 | `/private/tmp/mcp-exp/run-A-claude-2` | 0 |
| `run-A-claude-3` | `4591fe06-8b57-4a3f-9e17-a6a81441a93c` | 2026-09-24 17:09:25 | 17:09:32 | `/private/tmp/mcp-exp/run-A-claude-3` | 0 |
| `run-A-copilot-1` | `4c9c84f9-3666-4635-93c0-ba4554c9c461` | 2026-09-24 17:08:32 | 17:08:43 | `/private/tmp/mcp-exp/run-A-copilot-1` | 0 |
| `run-A-copilot-2` | `b675b052-50a1-4aef-a91f-67c86945c3a1` | 2026-09-24 17:09:02 | 17:09:12 | `/private/tmp/mcp-exp/run-A-copilot-2` | 0 |
| `run-A-copilot-3` | `6cd965cc-7219-4806-bbb9-65e6558cce34` | 2026-09-24 17:09:32 | 17:09:42 | `/private/tmp/mcp-exp/run-A-copilot-3` | 0 |
| `run-A-cursor-1` | `88ee6eb0-d333-4895-8be4-f59c7ca23318` | 2026-09-24 17:08:43 | 17:08:56 | `/private/tmp/mcp-exp/run-A-cursor-1` | 0 |
| `run-A-cursor-2` | `da0d39b6-7516-4ab9-a48f-f4963f894fc5` | 2026-09-24 17:09:12 | 17:09:25 | `/private/tmp/mcp-exp/run-A-cursor-2` | 0 |
| `run-A-cursor-3` | `0382a1e0-3631-4995-a8bc-f95b4a6266e3` | 2026-09-24 17:09:42 | 17:09:56 | `/private/tmp/mcp-exp/run-A-cursor-3` | 0 |
| `run-B-claude-1` | `9fb289ba-2a00-4a1c-9229-e8883421b0a8` | 2026-09-24 17:09:57 | 17:10:04 | `/private/tmp/mcp-exp/run-B-claude-1` | 0 |
| `run-B-claude-2` | `8a3b3dfa-aee0-4056-92b9-2340a4d0601c` | 2026-09-24 17:10:30 | 17:10:35 | `/private/tmp/mcp-exp/run-B-claude-2` | 0 |
| `run-B-claude-3` | `bbbc8c4b-7f17-49fb-855c-ce25d4352f0f` | 2026-09-24 17:11:02 | 17:11:12 | `/private/tmp/mcp-exp/run-B-claude-3` | 0 |
| `run-B-copilot-1` | `e31f7d0b-f055-4e19-a4d5-e3893897d562` | 2026-09-24 17:10:04 | 17:10:15 | `/private/tmp/mcp-exp/run-B-copilot-1` | 0 |
| `run-B-copilot-2` | `6ee36066-4f43-43d4-8373-b48a74143c7c` | 2026-09-24 17:10:36 | 17:10:49 | `/private/tmp/mcp-exp/run-B-copilot-2` | 0 |
| `run-B-copilot-3` | `f5f931e6-2ac6-49b7-8860-0f9f6e0b6808` | 2026-09-24 17:11:13 | 17:11:24 | `/private/tmp/mcp-exp/run-B-copilot-3` | 0 |
| `run-B-cursor-1` | `c2e53f8a-6960-46c6-aa75-11d2a3a6d364` | 2026-09-24 17:10:15 | 17:10:29 | `/private/tmp/mcp-exp/run-B-cursor-1` | 0 |
| `run-B-cursor-2` | `d3967083-2ed9-4429-a4d1-96d81c58aaf7` | 2026-09-24 17:10:49 | 17:11:02 | `/private/tmp/mcp-exp/run-B-cursor-2` | 0 |
| `run-B-cursor-3` | `807a6212-e612-4896-96a9-e331fe069de3` | 2026-09-24 17:11:24 | 17:11:46 | `/private/tmp/mcp-exp/run-B-cursor-3` | 0 |

## Round A vs round B

| | Round A (vague) | Round B (clear) |
|---|---|---|
| Runs that called the tool | 9 / 9 | 9 / 9 |
| `end` sent | `2026-09-20` in 9 / 9 | `2026-09-21` in 9 / 9 |
| Events returned | 2 in 9 / 9 | 3 in 9 / 9 |
| Answer includes Robotics Club Social (Sun 20 Sep) | 0 / 9 | 9 / 9 |
| Answer mentions the end-date boundary | 0 / 9 | 0 / 9 |

The description alone decided the outcome. With the vague description, every agent read
"Sunday 20 September" as `end = 2026-09-20`, and the exclusive comparison silently dropped
Sunday. With the clear description, every agent sent the following day.

## Agent vs agent

There was **no difference between agents in what they sent**: all three sent identical
arguments within each round, in all 3 repeats. The differences are in what they
recorded and said:

- **Visible reasoning.**
  - Claude Code's thinking blocks are empty in the output and transcript (a signature
    only), so its reasoning cannot be inspected.
  - Copilot's reasoning summaries in round A mention ISO date format but not
    inclusivity (run 2 has no reasoning event). In round B all three mention the end
    date: run 1 "the end date doesn't count, which is September 21"; run 2 "ensure that
    the date range is inclusive. The end date should be the 21st"; run 3 "from September
    14, 2026, to September 21, 2026 … inclusive".
  - Cursor's thinking in round B says, in all three runs, that the tool excludes the end
    date and so the end should be the 21st. In round A it never considers the boundary.
- **Confidence in wrong answers.** In round A, all three Cursor answers state a count
  ("there are **2** events"). Claude's and Copilot's round A answers list the two events
  without a count. None of them hedges.
- **Silent correction in round B.** Every round B answer lists the three events and none
  tells the user that the tool's end date is exclusive or that it passed the 21st.
  Cursor B-3 ends with "That's all three events in that range."

## Server log vs what the user was told

Same run, two views. The left column is everything the server can see.

| Run | Server log ([`raw/server-log.jsonl`](raw/server-log.jsonl)) | Final answer to the user |
|---|---|---|
| `run-A-claude-1` | `start=2026-09-14 end=2026-09-20`, count 2: Robotics Club Build Night, Debate Society Open Floor | "Events between Monday, September 14 and Sunday, September 20, 2026:" then the same two events |
| `run-A-copilot-1` | `start=2026-09-14 end=2026-09-20`, count 2: same two | The two events as bullets, no heading, no count |
| `run-A-cursor-1` | `start=2026-09-14 end=2026-09-20`, count 2: same two | "There are **2** events between Monday 14 September and Sunday 20 September 2026" |
| `run-B-cursor-3` | `start=2026-09-14 end=2026-09-21`, count 3: adds Robotics Club Social | Three events, "That's all three events in that range." |

**Can the server alone tell whether the tool was used correctly? From this log, no.**
The log shows exactly what was asked and what was returned. `end=2026-09-20` returning
nothing on the 20th is correct behaviour for the tool's contract. Whether it was *wrong*
depends on the user's intent ("through Sunday"), which never reaches the server. The
server sees neither the prompt nor the final answer. A request for "the week before the
20th" and a request for "up to and including Sunday the 20th" produce the same log line.
What the server *can* do is flag a pattern: in round A, 9 of 9 calls used an `end` that is
a Sunday and returned nothing for that day. Even then it cannot tell whether any user was
misled.

## Observal capture

All 18 experiment sessions are in Observal ([`raw/observal/traces-after-drain.json`](raw/observal/traces-after-drain.json)),
and `observal reconcile --dry-run` afterwards reports every one `up_to_date`
([`raw/observal/reconcile-dryrun-after-drain.json`](raw/observal/reconcile-dryrun-after-drain.json)).
**None arrived on its own.** What happened:

1. The hooks fired for every run: `~/.observal/sync.log` shows "durable records pending"
   for each session ([`raw/observal/sync-log-experiment.txt`](raw/observal/sync-log-experiment.txt)), and the local outbox grew from 21 pending batches (before the setup checks) to 69 (after the runs).
   Immediately after the runs, `observal ops traces` listed **0** of the 18
   ([`raw/observal/traces-before-reconcile.json`](raw/observal/traces-before-reconcile.json)).
2. `observal reconcile` found all 18 but only queued them (`outbox_drained: false`,
   [`raw/observal/reconcile.json`](raw/observal/reconcile.json)).
3. Two causes. First, the server's ingest endpoint is limited to 60 requests per minute
   (`observal-server/api/routes/ingest.py`), and the backlog plus reconcile hit it (14 × HTTP 429 in the load balancer log, [`raw/observal/lb-ingest-requests.log`](raw/observal/lb-ingest-requests.log);
   that log starts at 17:03:33 because Docker's log rotation dropped earlier lines. Its 6 × HTTP 422
   are Observal quarantining old batches from 17 and 20 September, not experiment data). Second, the outbox is delivered strictly oldest-first
   and stops at the first batch the server does not fully acknowledge. Its head was a batch
   from an **unrelated session of 20 September** (`82e6588f…`, lines 505–506). The server
   held that session only through line 308, and the batch carrying lines 309–808 was queued
   *behind* it. The head batch could never be acknowledged, so nothing behind it, including
   all 18 experiment sessions, was sent.
4. With the experimenter's approval, the 7 blocking batches (ids 118–137) were backed up
   and deleted from `~/.observal/telemetry_buffer.db`. Their lines were all contained in
   later batches 200/201, so nothing was lost. Two reconcile passes 65 s apart then
   drained the outbox to 0 (17:17–17:19 UTC).

So "captured" here means **captured after manual repair**, not live.

What Observal holds differs by agent ([`raw/observal/experiment-sessions-spans.json`](raw/observal/experiment-sessions-spans.json)):

| Agent | Tool arguments (`start`/`end`) | Tool result | Model field | Notes |
|---|---|---|---|---|
| Claude Code | Yes (`hook_posttooluse.tool_input`) | Yes | `claude-sonnet-5` | Complete for this question |
| Copilot CLI | **No**: `copilot_cli_tool_execution_start` has empty attributes, and `hook_toolresult.tool_name` is `""` | Yes | empty | Observal cannot show which arguments produced the result |
| Cursor CLI | Yes (inside `CallDynamicTool.tool_input.arguments`) | **No** (`tool_result_count` 0) | empty | Event timestamps are ingest time (17:17), not run time (17:08–17:11) |

So for the question "what did the agent send, and what came back", Observal alone answered
it fully only for Claude Code in this setup. The server log answered it for all 18.

### Setup-check sessions (not results)

Seven sessions came from setup checks run before the experiment, with different prompts
(listing tools, or deliberately trying to read files). They are in
[`raw/setup-checks/`](raw/setup-checks/) and in Observal: Claude `7fa9822b…`,
Copilot `8e6f14c3…`, Cursor `7d8602c1…`, `44cbd377…` (plus its subagent `4b4f2cca…`),
`a3b6a153…`, `e3c2a4ab…`. They are excluded from the results.

## Surprising or contrary to expectation

- **Zero variance.** Repeats were run because LLM output varies, but the 9 runs in each
  round sent byte-identical arguments, and the outcome was the same for every agent in
  every repeat.
- **No agent mentioned the boundary, in either round.** In round A none suspected the
  last day was missing. In round B they all handled it correctly and silently, so the
  user is never told the tool has an exclusive end.
- <a id="cursor-caveat"></a>**Cursor's `Read()` deny rules do not cover its Grep tool.** In
  setup check `check-A-cursor-2` (prompt: read `.cursor/mcp.json` and the server file),
  `Read` and `Shell` were denied, but Cursor used Grep to read the workspace
  `.cursor/mcp.json`, found the absolute server path, grepped the first lines of
  `server.mjs` outside the workspace, and also started a subagent to retry. For this reason
  the MCP config was moved to the global `~/.cursor/mcp.json` before the real runs. The
  re-test (`check-A-cursor-4`) found no path to the server. In the 6 real Cursor runs no
  Grep, Glob, Read or Shell call was made.
- **Copilot's default model is "auto"**, resolved per session to `gpt-5.6-luna`, which was
  the only candidate available on this account (`session.auto_mode_resolved`).
- **The embedded Observal server could not be installed.** `observal server install` fails
  because its checksum file returns 404 upstream. The existing Docker deployment in
  `~/observal` was used instead.

## Deviations from the plan, logged

- `checksums-before-runs.txt` was not written when intended (a shell `||` branch that
  never ran). The hashes were printed to the console before the first run and copied into
  the file afterwards; the file says so. They match the after-run hashes.
- Setup checks were added before the experiment (7 sessions, separate prompts, separate log
  [`raw/setup-checks-server-log.jsonl`](raw/setup-checks-server-log.jsonl)) to catch config
  errors without spending experiment runs. The Cursor configuration changed once as a
  result (see above), before any real run.
- `observal ops traces` exports were filtered to experiment sessions before being
  committed. All personal paths and IDs were redacted; see
  [`raw/REDACTIONS.md`](raw/REDACTIONS.md).

## Observal sessions worth screenshotting

Open these in the Observal web UI (`http://localhost:3000`):

1. **`run-A-cursor-1`: `88ee6eb0-d333-4895-8be4-f59c7ca23318`.** The clearest wrong answer:
   `CallDynamicTool` with `end: 2026-09-20`, then "There are **2** events". It also shows
   Observal's Cursor gap, with arguments but no tool result.
2. **`run-B-cursor-3`: `807a6212-e612-4896-96a9-e331fe069de3`.** Same agent, clear
   description: `end: 2026-09-21`, three events, "That's all three events in that range."
   Side by side with #1 it shows the description is the only variable.
3. **`run-A-claude-1`: `8d96d340-5efa-458d-b7af-685c1e32b1a7`.** The most complete trace:
   `hook_posttooluse` shows arguments *and* the two-event result, so the missing Sunday is
   visible inside Observal itself. Pair it with the server-log line for the same run.
4. **`run-A-copilot-1`: `4c9c84f9-3666-4635-93c0-ba4554c9c461`.** Observal has the tool
   result but an empty tool name and no arguments, so from this trace alone you cannot tell
   which date range was requested. Only the server log shows `end=2026-09-20`.
5. **`check-A-cursor-2`: `44cbd377-6ecd-441f-baed-632eeeb9d396`** (setup check, not a
   result). Cursor, denied `Read`, falls back to Grep and a subagent to read files outside
   its workspace. Useful if the article discusses sandboxing an agent's tool access.
