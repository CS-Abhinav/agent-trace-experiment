#!/usr/bin/env python3
"""Run one experiment session: one agent, one round, one repeat.

    python3 runner/run.py <claude|copilot|cursor> <A|B> <n> [--check]

Each run gets a fresh, empty workspace outside the repo, a fresh session and a
clean environment (only HOME/USER/PATH and friends), so nothing from the
orchestrating shell leaks in. The prompt is read from PROMPT.txt and sent
verbatim. The agent's stdout and stderr are saved unchanged, next to a small
meta.json recording the command, CLI version, timestamps and exit code.

--check runs a setup check instead: same config, a neutral prompt that asks the
agent to list its tools without calling any, and a separate log. It exists only
to catch configuration errors before the real runs, and is never a result.
"""
import json
import os
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # mcp-experiment/
SERVER = HERE / "server.mjs"
PROMPT = (HERE / "PROMPT.txt").read_text().rstrip("\n")
CHECK_PROMPT = os.environ.get("CHECK_PROMPT", "List the names of the tools you have available. Do not call any tools.")
WS_ROOT = Path("/private/tmp/mcp-exp")                   # outside the repo and outside ~
NODE = shutil.which("node")
SERVER_NAME = "campus-events"
TOOL = "get_events_in_range"
CURSOR_GLOBAL_MCP = Path.home() / ".cursor" / "mcp.json"
CLEAN_ENV_KEYS = ["HOME", "USER", "LOGNAME", "PATH", "SHELL", "TMPDIR", "LANG", "TERM"]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def mcp_server_entry(label, version, log_file):
    return {
        "command": NODE,
        "args": [str(SERVER)],
        "env": {
            "EVENTS_TOOL_DESCRIPTION": version,
            "MCP_RUN_LABEL": label,
            "MCP_LOG_FILE": str(log_file),
        },
    }


def build(agent, ws, label, version, log_file, prompt, session_id):
    """Return the argv for one headless run. Flags checked against each CLI's --help."""
    entry = mcp_server_entry(label, version, log_file)
    if agent == "claude":
        cfg = json.dumps({"mcpServers": {SERVER_NAME: {"type": "stdio", **entry}}})
        return [
            "claude", "-p", prompt,
            "--mcp-config", cfg, "--strict-mcp-config",       # only our server
            "--tools", "",                                      # no built-in tools
            "--allowedTools", f"mcp__{SERVER_NAME}__{TOOL}",    # pre-approve the one tool
            "--output-format", "stream-json", "--verbose",
            "--session-id", session_id,
        ]
    if agent == "copilot":
        cfg = json.dumps({"mcpServers": {SERVER_NAME: {"type": "local", "tools": ["*"], **entry}}})
        return [
            "copilot", "-p", prompt,
            "--additional-mcp-config", cfg,
            "--disable-builtin-mcps",                           # no GitHub MCP server
            f"--available-tools={SERVER_NAME}-{TOOL}",          # model sees only our tool
            f"--allow-tool={SERVER_NAME}({TOOL})",              # pre-approve it
            "--no-ask-user", "--disallow-temp-dir",
            "--no-remote-export", "--no-auto-update",
            "--output-format", "json",
            "--session-id", session_id,
        ]
    if agent == "cursor":
        # Cursor has no per-run MCP flag. It reads MCP servers from mcp.json and
        # permissions from cli.json. The MCP config goes in the GLOBAL
        # ~/.cursor/mcp.json for the duration of the run (see main), not in the
        # workspace: a setup check showed Cursor's Grep tool ignores Read() deny
        # rules, read a workspace mcp.json and followed it to the server source.
        # The workspace keeps only the permission file, which names no paths.
        CURSOR_GLOBAL_MCP.write_text(json.dumps({"mcpServers": {SERVER_NAME: entry}}, indent=2))
        cdir = ws / ".cursor"
        cdir.mkdir()
        (cdir / "cli.json").write_text(json.dumps({
            "permissions": {
                "allow": [f"Mcp({SERVER_NAME}:{TOOL})"],
                "deny": ["Shell(*)", "Read(**)", "Read(/**)", "Write(**)", "Write(/**)", "WebFetch(*)"],
            }
        }, indent=2))
        return [
            "cursor-agent", "-p", prompt,
            "--output-format", "stream-json",
            "--approve-mcps", "--trust",
            "--workspace", str(ws),
        ]
    raise SystemExit(f"unknown agent {agent}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    agent, version, n = args[0], args[1].upper(), int(args[2])
    kind = "check" if check else "run"
    label = f"{kind}-{version}-{agent}-{n}"

    out = HERE / "results" / "raw" / ("setup-checks" if check else "runs") / label
    if out.exists():
        raise SystemExit(f"{out} already exists; refusing to overwrite a recorded run")
    out.mkdir(parents=True)
    log_file = HERE / "results" / "raw" / ("setup-checks-server-log.jsonl" if check else "server-log.jsonl")

    ws = WS_ROOT / label
    if ws.exists():
        raise SystemExit(f"workspace {ws} already exists")
    ws.mkdir(parents=True)

    if CURSOR_GLOBAL_MCP.exists():
        raise SystemExit(f"{CURSOR_GLOBAL_MCP} exists; refusing to overwrite the user's Cursor MCP config")

    env = {k: os.environ[k] for k in CLEAN_ENV_KEYS if k in os.environ}
    session_id = str(uuid.uuid4())
    argv = build(agent, ws, label, version, log_file, CHECK_PROMPT if check else PROMPT, session_id)
    exe = argv[0]
    cli_version = subprocess.run([exe, "--version"], env=env, capture_output=True, text=True).stdout.strip()

    meta = {
        "label": label, "agent": agent, "round": version, "repeat": n, "setup_check": check,
        "cli_version": cli_version, "workspace": str(ws),
        "requested_session_id": session_id if agent != "cursor" else None,
        "prompt": argv[2], "argv": argv, "started": now(),
    }
    print(f"[{meta['started']}] {label}: {cli_version} in {ws}", flush=True)
    with open(out / "stdout.txt", "wb") as so, open(out / "stderr.txt", "wb") as se:
        try:
            p = subprocess.run(argv, cwd=ws, env=env, stdout=so, stderr=se, stdin=subprocess.DEVNULL, timeout=600)
            meta["exit_code"] = p.returncode
        except subprocess.TimeoutExpired:
            meta["exit_code"] = "timeout after 600s"
        finally:
            if agent == "cursor":
                meta["cursor_global_mcp_json"] = json.loads(CURSOR_GLOBAL_MCP.read_text())
                CURSOR_GLOBAL_MCP.unlink()
    meta["finished"] = now()
    meta["workspace_after"] = sorted(str(p.relative_to(ws)) for p in ws.rglob("*"))
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"[{meta['finished']}] {label}: exit {meta['exit_code']}", flush=True)


if __name__ == "__main__":
    main()
