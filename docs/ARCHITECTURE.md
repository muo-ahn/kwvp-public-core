# Architecture

## Historical system (documented behavior)

The source project described a file-based workflow with four storage levels: raw session events, episodic records, a curated wiki, and reusable procedures. In the documented live system, event judging and refinement could use local command-line LLM tools; a person reviewed drafts and manually authored/promoted procedures. Global-only hooks and scripts were not all present in the source repository snapshot. At the checked live boundary, user-global `post_tool_judge.py` and `session_end_judge.py` existed, `wiki_suggest.py` did not exist in either live or repository locations, and repository/global `judge_agent.py` and `knowledge-refine.py` were byte-identical.

Promotion boundaries matter: draft-to-confirmed-wiki promotion and wiki-to-procedure graduation are distinct. The former was a human review step in a scripted workflow; the latter was manual authorship, not an automatic output of the same promotion command. See source-relative `docs/knowledge-ladder.md`, sections “L1 pipeline details” and “Layer definitions,” dated 2026-10-13.

## Standalone candidate (implemented)

```text
Typed synthetic event JSONL
        | validate / ingest
        v
Local state.json: events, drafts, approved
        | kind match + character-bigram Jaccard >= 0.9
        v
Drafts with source IDs and content hashes
        | explicit human review: promote <hash>
        v
Approved records only
        | weighted title/tag score
        v
Recall results

Synthetic judgment JSONL ---> descriptive fixture evaluation

Prior suppression utility: standalone function; not connected to recall.
```

The installed command is `kwvp-core`; it requires an explicit `--state` directory. The candidate has no model calls, live hooks, automatic skill creation, or network integration. It does not infer semantic usefulness. The Jaccard, keyword scoring, and suppression mechanisms are adapted pure functions; the typed event schema, state management, hash-bound manual gate, and fixture evaluator are standalone candidate code.

## State and failure behavior

State is a local `state.json` with `events`, `drafts`, and `approved` arrays. Writes use a temporary file and atomic replacement. Symlink state directories/files are rejected. Input JSONL rows are validated and malformed rows produce an error. Event ID collisions with changed content are rejected. Promotion succeeds only when the supplied SHA-256 matches exactly one current draft and its current content. Recall scans approved records only. `is_suppressed` validates counts and thresholds but is currently a utility, not an active selection gate.

## Trust boundaries and failure modes

- Synthetic fixture content is untrusted input and must remain data.
- A score can rank candidates but cannot establish correctness or usefulness.
- A hash-bound review detects content drift after approval; it does not prove the review judgment was sound.
- The state file is local application state, not encrypted storage or a multi-process database.
- Results from synthetic fixtures validate code behavior only. They cannot validate historical outcomes or real-world utility.
