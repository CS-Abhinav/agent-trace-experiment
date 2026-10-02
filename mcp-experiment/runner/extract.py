#!/usr/bin/env python3
"""Pull the facts out of each run's raw output. Reads only; writes results/extracted.json.

For every run: CLI version, model as reported by the agent, every call to the
MCP tool with its exact arguments, every other tool call, the final answer
text, and the matching server-log records. Nothing is scored here except one
mechanical check (does the final answer contain "Robotics Club Social"), which
summary.md then confirms by reading the answer.
"""
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
RAW = HERE / "results" / "raw"
TOOL = "get_events_in_range"


def jsonl(path):
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            out.append({"_unparsed": line})
    return out


def claude(events):
    r = {"models": set(), "session_ids": set(), "tool_calls": [], "other_tool_calls": [], "final": None, "texts": []}
    for e in events:
        if "session_id" in e:
            r["session_ids"].add(e["session_id"])
        t = e.get("type")
        if t == "system" and e.get("subtype") == "init":
            r["models"].add(e.get("model"))
        elif t == "assistant":
            for c in e["message"]["content"]:
                if c.get("type") == "tool_use":
                    target = r["tool_calls"] if c["name"].endswith(TOOL) else r["other_tool_calls"]
                    target.append({"name": c["name"], "args": c.get("input")})
                elif c.get("type") == "text":
                    r["texts"].append(c["text"])
        elif t == "result":
            r["final"] = e.get("result")
            r["is_error"] = e.get("is_error")
            r["model_usage"] = sorted((e.get("modelUsage") or {}).keys())
    return r


def copilot(events):
    r = {"models": set(), "session_ids": set(), "tool_calls": [], "other_tool_calls": [], "final": None, "texts": []}
    for e in events:
        t, d = e.get("type"), e.get("data") or {}
        if e.get("sessionId"):
            r["session_ids"].add(e["sessionId"])
        if d.get("model"):
            r["models"].add(d["model"])
        if t == "session.auto_mode_resolved":
            r["auto_mode_resolved"] = d
        if t == "tool.execution_start":
            target = r["tool_calls"] if d.get("mcpToolName") == TOOL else r["other_tool_calls"]
            target.append({"name": d.get("toolName"), "args": d.get("arguments")})
        if t == "assistant.message" and d.get("content"):
            r["texts"].append(d["content"])
        if t == "result":
            r["exit_code_reported"] = e.get("exitCode")
    r["final"] = r["texts"][-1] if r["texts"] else None
    return r


def cursor(events):
    r = {"models": set(), "session_ids": set(), "tool_calls": [], "other_tool_calls": [], "final": None, "texts": []}
    for e in events:
        if e.get("session_id"):
            r["session_ids"].add(e["session_id"])
        t = e.get("type")
        if t == "system":
            r["models"].add(e.get("model"))
        elif t == "tool_call" and e.get("subtype") == "started":
            tc = e["tool_call"]
            kind = next(iter(tc))
            args = tc[kind].get("args", {})
            if kind == "mcpToolCall" and TOOL in json.dumps(args):
                r["tool_calls"].append({"name": kind, "args": args})
            else:
                r["other_tool_calls"].append({"name": kind, "args": args})
        elif t == "assistant":
            for c in e["message"]["content"]:
                if c.get("type") == "text":
                    r["texts"].append(c["text"])
        elif t == "result":
            r["final"] = e.get("result")
            r["is_error"] = e.get("is_error")
    return r


PARSERS = {"claude": claude, "copilot": copilot, "cursor": cursor}


def main():
    log = defaultdict(list)
    for rec in jsonl(RAW / "server-log.jsonl"):
        log[rec.get("run")].append(rec)

    runs = []
    for d in sorted((RAW / "runs").iterdir()):
        meta = json.loads((d / "meta.json").read_text())
        r = PARSERS[meta["agent"]](jsonl(d / "stdout.txt"))
        server = log.get(meta["label"], [])
        final = r["final"] or ""
        runs.append({
            "label": meta["label"], "agent": meta["agent"], "round": meta["round"], "repeat": meta["repeat"],
            "cli_version": meta["cli_version"].splitlines()[0], "exit_code": meta["exit_code"],
            "started": meta["started"], "finished": meta["finished"], "workspace": meta["workspace"],
            "session_ids": sorted(r["session_ids"]), "models": sorted(m for m in r["models"] if m),
            **{k: r[k] for k in ("model_usage", "auto_mode_resolved", "is_error") if k in r},
            "tool_calls_seen_by_agent": r["tool_calls"], "other_tool_calls": r["other_tool_calls"],
            "server_started": any(x["event"] == "server_start" for x in server),
            "server_calls": [{"args": x["args"], "count": x["count"], "returned": x["returned"]}
                             for x in server if x["event"] == "call"],
            "final_answer": final,
            "final_mentions_robotics_club_social": "Robotics Club Social" in final,
            "stderr_bytes": (d / "stderr.txt").stat().st_size,
        })
    (HERE / "results" / "extracted.json").write_text(json.dumps(runs, indent=2, ensure_ascii=False) + "\n")
    for r in runs:
        print(f"{r['label']:18} models={r['models']} calls={[(c['args']['start'], c['args']['end']) for c in r['server_calls']]} "
              f"counts={[c['count'] for c in r['server_calls']]} other={len(r['other_tool_calls'])} RCS_in_answer={r['final_mentions_robotics_club_social']} exit={r['exit_code']}")


if __name__ == "__main__":
    main()
