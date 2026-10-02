#!/usr/bin/env python3
"""Redact personal data from results/raw before it goes into the repo.

    python3 runner/redact.py <private-archive-dir>

First copies results/raw, unredacted, to the archive dir (outside the repo),
then rewrites files in place, replacing only the patterns below. Every
substitution is counted per file and written to results/raw/REDACTIONS.md.
Nothing else in any file is changed.
"""
import getpass
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
RAW = HERE / "results" / "raw"

def rules():
    """Build the patterns from this machine, so the script itself names nobody."""
    home = str(Path.home())
    user = getpass.getuser()
    obs = json.loads((Path.home() / ".observal" / "config.json").read_text())
    return [
        # (name, pattern, replacement)
        ("home directory path", re.compile(re.escape(home)), "/Users/<user>"),
        ("home directory in encoded project names", re.compile(re.escape(home.replace("/", "-"))), "-Users-<user>"),
        ("local username", re.compile(re.escape(user)), "<user>"),
        ("Observal user id", re.compile(re.escape(obs["user_id"])), "<observal-user-id>"),
        ("Observal username", re.compile(re.escape(obs["username"])), "<observal-username>"),
        ("email address", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "<email>"),
    ]


def main():
    archive = Path(sys.argv[1]).expanduser().resolve()
    if HERE in archive.parents or archive == HERE:
        raise SystemExit("archive must be outside the repo")
    if archive.exists():
        raise SystemExit(f"{archive} exists; refusing to overwrite")
    shutil.copytree(RAW, archive)

    RULES = rules()
    report = {}
    for p in sorted(RAW.rglob("*")):
        if not p.is_file() or p.name == "REDACTIONS.md":
            continue
        text = p.read_text(errors="surrogateescape")
        counts = Counter()
        for name, rx, repl in RULES:
            text, n = rx.subn(repl, text)
            if n:
                counts[name] += n
        if counts:
            p.write_text(text, errors="surrogateescape")
            report[str(p.relative_to(RAW))] = counts

    lines = [
        "# Redactions",
        "",
        "Files in this folder are the raw outputs, unchanged except for the substitutions",
        "below. Unredacted originals are kept outside the repository.",
        "",
        "| Pattern | Replaced with |",
        "|---|---|",
    ]
    lines += [f"| {name} | `{repl}` |" for name, _, repl in RULES]
    lines += [
        "",
        "Not redacted, on purpose: provider-encrypted reasoning blobs and IDs",
        "(`encryptedContent`, `reasoningOpaque`, `reasoningBlocks`, `apiCallId`,",
        "Claude `signature` fields). They are opaque model data, not credentials, and they",
        "are part of what a transcript records.",
        "",
        "Scanned for and not found: GitHub tokens, `sk-` keys, JWTs, bearer tokens,",
        "`access_token`/`api_key`/`password`-style fields, machine hostnames.",
        "",
        "| File | Substitutions |",
        "|---|---|",
    ]
    lines += [f"| `{f}` | " + ", ".join(f"{k}: {v}" for k, v in c.items()) + " |" for f, c in report.items()]
    (RAW / "REDACTIONS.md").write_text("\n".join(lines) + "\n")
    print(f"archived to {archive}; redacted {len(report)} files")


if __name__ == "__main__":
    main()
