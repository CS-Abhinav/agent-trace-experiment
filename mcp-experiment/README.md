# One tool, three agents

The same date-range bug from [the parent experiment](../README.md), now exposed
as a tool through an MCP server. Nothing is fixed. The question is different:
when three coding agents are handed this tool, how do they *use* it, and can
the server, looking only at its own log, tell whether they used it correctly?

## The server

[`server.mjs`](server.mjs) exposes one tool, `get_events_in_range(start, end)`.
It imports the app's own helper and data, unchanged:

```js
// ../campus-events/src/lib/dateRange.js
export function getEventsInRange(events, start, end) {
  return events.filter((event) => event.date >= start && event.date < end);
}
```

`end` is exclusive. Dates are `YYYY-MM-DD` strings compared as strings: no
`Date` parsing, so the caller's time zone cannot shift anything. Arguments are
passed through as received, not validated, so if an agent sends
`2026-09-20T23:59:59`, that exact string is compared and logged.

The tool description has two versions, chosen by an environment variable:

| `EVENTS_TOOL_DESCRIPTION` | Description the agent sees |
|---|---|
| `A` (default) | Returns events between two dates. |
| `B` | Returns events from start up to, but NOT including, end. To include a day, pass the following day as end. |

Nothing else changes between A and B.

## The log

stdout carries MCP messages, so the server never writes to it. Every call is
appended to a JSONL file instead:

```json
{"ts":"…","run":"run-A-claude-1","description":"A","event":"call","args":{"start":"2026-09-14","end":"2026-09-20"},"count":2,"returned":["Robotics Club Build Night","Debate Society Open Floor"]}
```

A `server_start` record is written when an agent launches the server. It
separates "the agent never started the server" from "the server started, but
the tool was never called".

| Variable | Default | Purpose |
|---|---|---|
| `MCP_RUN_LABEL` | `unlabelled` | Which agent/run this is |
| `MCP_LOG_FILE` | `logs/calls.jsonl` | Where the log goes |

Read it with `jq`:

```bash
jq -c 'select(.event=="call") | {run, args, count, returned}' logs/calls.jsonl
```

## Try it yourself

```bash
cd mcp-experiment && npm install
```

Then make an **empty** folder somewhere outside this repo and start each agent
there. The empty folder matters: if the agent can see `campus-events/`, it can
read the data directly and never needs the tool.

Paste this prompt verbatim and say nothing else:

> What events are happening between Monday 14 September and Sunday 20 September 2026? Please list all of them.

Replace `/ABS/PATH` below with the absolute path to this folder. To use version
B, change `"A"` to `"B"`.

### Claude Code

```bash
claude mcp add campus-events -s user \
  -e EVENTS_TOOL_DESCRIPTION=A -e MCP_RUN_LABEL=claude-try \
  -- node /ABS/PATH/mcp-experiment/server.mjs
```

Or, headless and without touching your config (as in the experiment):

```bash
claude -p "$(cat /ABS/PATH/mcp-experiment/PROMPT.txt)" \
  --mcp-config configs/claude.mcp.json --strict-mcp-config \
  --tools "" --allowedTools mcp__campus-events__get_events_in_range
```

`--tools ""` removes Claude Code's built-in tools, so the MCP tool is the only
one left.

### GitHub Copilot CLI

Add the server to `~/.copilot/mcp-config.json` (see
[`configs/copilot.mcp-config.json`](configs/copilot.mcp-config.json)), or pass
it for one session:

```bash
copilot -p "$(cat /ABS/PATH/mcp-experiment/PROMPT.txt)" \
  --additional-mcp-config @/ABS/PATH/mcp-experiment/configs/copilot.mcp-config.json \
  --disable-builtin-mcps \
  --available-tools=campus-events-get_events_in_range \
  --allow-tool='campus-events(get_events_in_range)'
```

`--available-tools` hides every other tool from the model; `--allow-tool`
pre-approves the one that is left.

### Cursor CLI

Cursor has no per-session MCP flag. Put the server in `~/.cursor/mcp.json`
(see [`configs/cursor.mcp.json`](configs/cursor.mcp.json)), and permissions in
`<workspace>/.cursor/cli.json`
(see [`configs/cursor.cli.json`](configs/cursor.cli.json)), then:

```bash
cursor-agent -p "$(cat /ABS/PATH/mcp-experiment/PROMPT.txt)" --approve-mcps --trust
```

Two things we found while setting this up:

- Cursor's CLI cannot hide its built-in tools; it can only deny them.
- Its `Read(...)` deny rules do **not** cover its Grep tool. In a setup check
  (see [`results/raw/setup-checks/check-A-cursor-2`](results/raw/setup-checks/check-A-cursor-2)),
  Cursor was denied `Read`, used Grep on a workspace `.cursor/mcp.json`,
  found the server path, and grepped `server.mjs` outside the workspace. That
  is why the MCP config goes in the global `~/.cursor/mcp.json`, not the
  workspace, so nothing in the workspace points at the data.

## How the experiment was run

[`runner/run.py`](runner/run.py) runs one session at a time:

```bash
python3 runner/run.py <claude|copilot|cursor> <A|B> <n>
```

Each run gets a fresh session, a fresh empty workspace under `/private/tmp/mcp-exp/<label>/`
and a clean environment (only `HOME`, `USER`, `PATH` and similar). The runner
saves the agent's stdout/stderr unchanged, plus a `meta.json` with the exact
command, CLI version, timestamps and exit code. It refuses to overwrite an
existing run.

Results are in [`results/`](results/): the summary, the prediction, and every
raw output, server log and session transcript.
