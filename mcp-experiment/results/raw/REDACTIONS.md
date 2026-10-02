# Redactions

Files in this folder are the raw outputs, unchanged except for the substitutions
below. Unredacted originals are kept outside the repository.

| Pattern | Replaced with |
|---|---|
| home directory path | `/Users/<user>` |
| home directory in encoded project names | `-Users-<user>` |
| local username | `<user>` |
| Observal user id | `<observal-user-id>` |
| Observal username | `<observal-username>` |
| email address | `<email>` |

Not redacted, on purpose: provider-encrypted reasoning blobs and IDs
(`encryptedContent`, `reasoningOpaque`, `reasoningBlocks`, `apiCallId`,
Claude `signature` fields). They are opaque model data, not credentials, and they
are part of what a transcript records.

Scanned for and not found: GitHub tokens, `sk-` keys, JWTs, bearer tokens,
`access_token`/`api_key`/`password`-style fields, machine hostnames.

| File | Substitutions |
|---|---|
| `observal/experiment-sessions-spans.json` | Observal user id: 18 |
| `observal/traces-after-drain.json` | Observal user id: 25 |
| `runs/run-A-claude-1/meta.json` | home directory path: 3 |
| `runs/run-A-claude-1/stdout.txt` | home directory path: 1 |
| `runs/run-A-claude-2/meta.json` | home directory path: 3 |
| `runs/run-A-claude-2/stdout.txt` | home directory path: 1 |
| `runs/run-A-claude-3/meta.json` | home directory path: 3 |
| `runs/run-A-claude-3/stdout.txt` | home directory path: 1 |
| `runs/run-A-copilot-1/meta.json` | home directory path: 3 |
| `runs/run-A-copilot-2/meta.json` | home directory path: 3 |
| `runs/run-A-copilot-3/meta.json` | home directory path: 3 |
| `runs/run-A-cursor-1/meta.json` | home directory path: 3 |
| `runs/run-A-cursor-2/meta.json` | home directory path: 3 |
| `runs/run-A-cursor-3/meta.json` | home directory path: 3 |
| `runs/run-B-claude-1/meta.json` | home directory path: 3 |
| `runs/run-B-claude-1/stdout.txt` | home directory path: 1 |
| `runs/run-B-claude-2/meta.json` | home directory path: 3 |
| `runs/run-B-claude-2/stdout.txt` | home directory path: 1 |
| `runs/run-B-claude-3/meta.json` | home directory path: 3 |
| `runs/run-B-claude-3/stdout.txt` | home directory path: 1 |
| `runs/run-B-copilot-1/meta.json` | home directory path: 3 |
| `runs/run-B-copilot-2/meta.json` | home directory path: 3 |
| `runs/run-B-copilot-3/meta.json` | home directory path: 3 |
| `runs/run-B-cursor-1/meta.json` | home directory path: 3 |
| `runs/run-B-cursor-2/meta.json` | home directory path: 3 |
| `runs/run-B-cursor-3/meta.json` | home directory path: 3 |
| `setup-checks/check-A-claude-1/meta.json` | home directory path: 3 |
| `setup-checks/check-A-claude-1/stdout.txt` | home directory path: 1 |
| `setup-checks/check-A-copilot-1/meta.json` | home directory path: 3 |
| `setup-checks/check-A-cursor-2/stdout.txt` | home directory path: 15 |
| `setup-checks/check-A-cursor-3/meta.json` | home directory path: 3 |
| `setup-checks/check-A-cursor-4/meta.json` | home directory path: 3 |
| `transcripts/check-A-claude-1__claude__7fa9822b-1e5e-446b-8dd5-6ca8824cd6cb.jsonl` | home directory path: 1 |
| `transcripts/check-A-copilot-1__copilot__8e6f14c3-451a-4f70-b338-46500ce51ebe.jsonl` | home directory path: 1, email address: 1 |
| `transcripts/check-A-cursor-2__cursor__44cbd377-6ecd-441f-baed-632eeeb9d396.jsonl` | home directory path: 4 |
| `transcripts/check-A-cursor-2__cursor__4b4f2cca-be62-470d-9ff6-dfc82c980819.jsonl` | home directory path: 5 |
| `transcripts/run-A-claude-1__claude__8d96d340-5efa-458d-b7af-685c1e32b1a7.jsonl` | home directory path: 1 |
| `transcripts/run-A-claude-2__claude__74d5c296-5c10-4ade-8bb8-7315ba579424.jsonl` | home directory path: 1 |
| `transcripts/run-A-claude-3__claude__4591fe06-8b57-4a3f-9e17-a6a81441a93c.jsonl` | home directory path: 1 |
| `transcripts/run-A-copilot-1__copilot__4c9c84f9-3666-4635-93c0-ba4554c9c461.jsonl` | home directory path: 1, email address: 1 |
| `transcripts/run-A-copilot-2__copilot__b675b052-50a1-4aef-a91f-67c86945c3a1.jsonl` | home directory path: 1, email address: 1 |
| `transcripts/run-A-copilot-3__copilot__6cd965cc-7219-4806-bbb9-65e6558cce34.jsonl` | home directory path: 1, email address: 1 |
| `transcripts/run-B-claude-1__claude__9fb289ba-2a00-4a1c-9229-e8883421b0a8.jsonl` | home directory path: 1 |
| `transcripts/run-B-claude-2__claude__8a3b3dfa-aee0-4056-92b9-2340a4d0601c.jsonl` | home directory path: 1 |
| `transcripts/run-B-claude-3__claude__bbbc8c4b-7f17-49fb-855c-ce25d4352f0f.jsonl` | home directory path: 1 |
| `transcripts/run-B-copilot-1__copilot__e31f7d0b-f055-4e19-a4d5-e3893897d562.jsonl` | home directory path: 1, email address: 1 |
| `transcripts/run-B-copilot-2__copilot__6ee36066-4f43-43d4-8373-b48a74143c7c.jsonl` | home directory path: 1, email address: 1 |
| `transcripts/run-B-copilot-3__copilot__f5f931e6-2ac6-49b7-8860-0f9f6e0b6808.jsonl` | home directory path: 1, email address: 1 |

## Rows removed (not redacted)

- `observal/traces-before-reconcile.json` and `observal/traces-after-drain.json` are
  `observal ops traces -o json` exports filtered to the 18 experiment runs and the 7
  setup-check sessions. Removed rows were the experimenter's unrelated sessions and the
  orchestrating Claude Code session (`23708334-…`), which is excluded from the results.
  Each file carries a `_filter_note` with the before/after row counts.
- `observal/experiment-sessions-spans.json` is `observal ops traces --span -o json`
  filtered the same way, to the 18 experiment runs only.
