#!/usr/bin/env node
/**
 * campus-events MCP server: one tool, get_events_in_range(start, end).
 *
 * The tool calls the app's own shared helper, unchanged, so the end date is
 * still EXCLUSIVE. The bug is the point of the experiment; do not fix it here.
 *
 * stdout carries MCP messages, so nothing else may be written to it.
 * Every call is appended to a JSONL log file instead.
 *
 * Environment:
 *   EVENTS_TOOL_DESCRIPTION  "A" (vague, default) or "B" (clear)
 *   MCP_RUN_LABEL            free-text label for the run, written to the log
 *   MCP_LOG_FILE             log path (default: ./logs/calls.jsonl next to this file)
 */
import { appendFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { getEventsInRange } from "../campus-events/src/lib/dateRange.js";
import { events } from "../campus-events/src/data/events.js";

const here = dirname(fileURLToPath(import.meta.url));

const DESCRIPTIONS = {
  A: "Returns events between two dates.",
  B: "Returns events from start up to, but NOT including, end. To include a day, pass the following day as end.",
};

const version = (process.env.EVENTS_TOOL_DESCRIPTION || "A").toUpperCase();
if (!(version in DESCRIPTIONS)) {
  process.stderr.write(`EVENTS_TOOL_DESCRIPTION must be A or B, got "${version}"\n`);
  process.exit(1);
}
const runLabel = process.env.MCP_RUN_LABEL || "unlabelled";
const logFile = process.env.MCP_LOG_FILE || join(here, "logs", "calls.jsonl");

function log(record) {
  mkdirSync(dirname(logFile), { recursive: true });
  appendFileSync(
    logFile,
    JSON.stringify({ ts: new Date().toISOString(), run: runLabel, description: version, ...record }) + "\n"
  );
}

const server = new McpServer({ name: "campus-events", version: "1.0.0" });

server.registerTool(
  "get_events_in_range",
  {
    description: DESCRIPTIONS[version],
    // Dates are plain "YYYY-MM-DD" strings compared as strings, exactly as the
    // app does. No Date parsing, so the caller's time zone cannot matter.
    inputSchema: { start: z.string(), end: z.string() },
  },
  async ({ start, end }) => {
    const result = getEventsInRange(events, start, end);
    log({
      event: "call",
      args: { start, end },
      count: result.length,
      returned: result.map((e) => e.title),
    });
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

// A start record shows the agent at least launched the server, which separates
// "server never started" from "server started, tool never called".
log({ event: "server_start", pid: process.pid });

await server.connect(new StdioServerTransport());
