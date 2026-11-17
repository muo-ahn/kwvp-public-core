# Extraction assessment

## Recommendation

Extracting a narrow deterministic core is useful as a research artifact because its assumptions can be inspected and tested without private logs or a model service. It does not establish that automated knowledge extraction improves work. The candidate is a synthetic, review-gated demonstration.

## Current architecture and ownership boundary

The documented workflow spans event capture/judgment, episodic knowledge, wiki drafts and confirmed pages, then human-authored reusable procedures. Its current boundary is split: some hooks exist only in the user-global harness; repository and global copies of `judge_agent.py` and `knowledge-refine.py` were byte-identical at inspection; `wiki_suggest.py` was absent from both locations. The standalone candidate is a separate implementation and does not reproduce that runtime.

| Source component | Observed owner/status | Dependency or data boundary | Reusable mechanism | Testability / cost / risk | Extraction decision |
|---|---|---|---|---|---|
| `post_tool_judge.py`, `session_end_judge.py` | User-global only; absent from repository | Session hooks, local state, judge path | No pure function selected | Hard to isolate from host lifecycle; may process private session data | Excluded; document boundary only |
| `judge_agent.py` | Repository and user-global copies byte-identical at inspection | Local CLI LLM fallback and knowledge writes | No model judgment extracted | Cost/latency depend on CLI and session volume; private content risk | Excluded from runtime candidate |
| `knowledge-refine.py` | Repository and user-global copies byte-identical at inspection | Local CLI refinement and wiki/knowledge content | Character-bigram similarity helper; source uses it for link candidates, candidate reuses it for draft deduplication | Pure similarity portion is deterministic; full workflow has model and private-data dependencies | Extract only the character-bigram similarity helper (used for link candidates in source; reused for candidate draft deduplication) |
| `wiki_suggest.py` | Absent from repository and checked live boundary | Older documentation refers to it; not a current integration point | None | Cannot claim current behavior from historical references | Excluded; avoid stale integration claims |
| `wiki_index.py` / page scoring | Repository library; current path not identified as a live hook | Reads page title/tags and a prompt | Weighted keyword score | Deterministic and unit-testable; lexical false positives remain | Extract scoring function |
| `verdict_prior.py` | Repository library; current active wiring not assumed | Historical verdict counts | Zero-help and proportional suppression rules | Pure count logic is testable; small-sample and label risks remain | Extract as standalone utility, not active recall gate |
| `quality_eval.py` / `quality_integration.py` | Repository evaluation tooling | Structured manifests, evidence references, evaluation files and integration contracts | Typed validation, scorecards, provenance and integration checks | Deterministic portions are testable; vault/provider-contract wiring expands scope and data boundary | Excluded from initial candidate; separately assess if the project expands |
| Human wiki-to-procedure graduation | Human-owned step in documented ladder | Requires contextual review and authorship | Review boundary | Human decision is not reducible to a synthetic score | Preserve manual gate; no automatic skill generation |

The ownership and duplicate-copy observations are a point-in-time boundary check, not a guarantee about later deployments. Source locator: `docs/knowledge-ladder.md`, “L1 pipeline details” and “Layer definitions,” dated 2026-10-13; repository inventory and direct live-boundary inspection performed during this extraction.

## Extraction candidates and scope

The implementation adapts three pure mechanisms: the character-bigram similarity helper used for link candidates in the source, weighted keyword scoring, and prior-based suppression. The candidate reuses the similarity helper for its own deterministic draft deduplication. It adds new typed synthetic event validation, hash-bound manual promotion, approved-only retrieval, and synthetic evaluation. The suppression utility is not connected to recall.

Included scope:

- local synthetic event JSONL and explicit `state.json`;
- kind-matched deduplication using character-bigram Jaccard ≥0.9;
- deterministic title/tag scoring for approved records;
- a human promotion command that accepts a current draft SHA-256;
- a separate descriptive evaluator for synthetic judgment fixtures.

Excluded scope:

- global hooks and live transcript ingestion;
- local CLI or hosted model calls;
- provider-contract and vault-integrated quality evaluation;
- automatic procedure/skill generation;
- production persistence, multi-process coordination, and claims of time saved.

## Dependency, cost, and security profile

| Option | Dependencies / cost | Data exposure | Assessment |
|---|---|---|---|
| Synthetic deterministic candidate | Python standard library; local CPU; no API calls | Synthetic fixtures only | Appropriate for reproducible mechanics |
| Historical CLI-assisted judging/refinement | Local CLI tools and configuration; variable latency and quota | Session-derived text may be processed | Not included; historical results cannot be rerun from this release |
| Hosted model integration | Provider, credentials, network and recurring cost | Data crosses a service boundary | Out of scope; requires separate privacy/cost review |

## Known limitations

- Character-bigram similarity detects string resemblance, not semantic equivalence.
- Keyword scores can reward topic overlap, stale content, and lexical bias.
- The approval hash detects content drift after review; it does not validate the review itself.
- The JSON state is local application state, not encrypted storage or a multi-process database.
- Historical aggregate claims are documented, not independently reproduced from source logs.
- Synthetic fixture results validate mechanics only, not usefulness or productivity.

## Alternatives and reasons

1. **Publish the full operational runtime and data.** Excluded because the live boundary includes user-global hooks and private session data; a clean extraction better protects privacy and is independently runnable.
2. **Rebuild the model-backed workflow.** Excluded because source records are unavailable for reproduction, outcomes are mixed, and nondeterminism/cost would not resolve utility uncertainty.
3. **Automatically generate reusable procedures.** Excluded because wiki-to-procedure graduation was human-authored and existing evidence does not justify removing that gate.
4. **Include the newer quality evaluator and integration layer.** Deferred because its manifest/evidence contract and vault/provider integration materially expand the initial scope; it should be reviewed as a separate extraction, not silently represented by this simpler evaluator.
5. **Publish only a narrative.** Rejected because a small fixture-backed implementation permits direct inspection of deterministic mechanics while keeping evidence claims separate.

## Decision

Proceed with the small deterministic candidate, synthetic fixtures, and evidence-backed case study. Keep the human gate. Do not infer productivity gains or generalize selected historical cohorts. Any live integration, model adapter, or broader evaluator requires a new scope decision and separate data, security, cost, and utility evaluation.
