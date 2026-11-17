# Knowledge Workflow Validation Pipeline

A small, reproducible case study in measuring whether remembered knowledge helps future work. This public edition separates historical observations from a standalone synthetic reference implementation. It does not claim that retrieval, automation, or an AI assistant increases productivity.

## Problem

Knowledge systems often measure retrieval, injection counts, or lexical overlap while leaving the real question unanswered: did stored knowledge reduce rework, or did it add noise? This case study documents both failed and ambiguous measurements instead of treating activity as productivity.

## Why

The historical project needed a defensible decision about knowledge capture and recall. Its results show why controls, holdouts, stable denominators, and human review matter. They do not establish a productivity benefit.

## What this is

The original project instrumented a file-based knowledge workflow: session events could be judged, refined into wiki drafts, reviewed by a person, and promoted into reusable procedures. Its most useful contribution for this case study is methodological: define outcomes before looking at results, include negative controls, preserve failed experiments, and label evidence by what it can support.

The standalone candidate extracts a few deterministic selection and suppression ideas into a typed, synthetic event pipeline. It is intentionally smaller than the original operational system. It has no live hooks, model calls, automatic skill creation, or access to private session records.

## Architecture

The original documented flow was event capture and judgment → episodic knowledge → wiki draft and human review → manually authored procedure. Some live hooks were user-global; they are not represented as current repository components. The standalone candidate instead validates synthetic events, merges same-kind near-duplicates using character-bigram similarity, writes drafts to local JSON state, requires a person to approve the current content hash, and retrieves only approved drafts. Fixture evaluation is separate from retrieval. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for ownership and failure boundaries.

## QuickStart

Requirements: Python 3.9+; no third-party runtime dependencies. Run from the repository root with an explicit state directory:

```sh
PYTHONPATH=src python -m kwvp_core.cli --help
PYTHONPATH=src python -m kwvp_core.cli --state /tmp/kwvp-demo demo
PYTHONPATH=src python -m kwvp_core.cli --state /tmp/kwvp-demo list
# Paste the hash printed by demo if your code differs from this revision.
PYTHONPATH=src python -m kwvp_core.cli --state /tmp/kwvp-demo promote b5608b6cc78b20c14a85c0d8dff53db900959b6c5551e819592e961ce51ce610
PYTHONPATH=src python -m kwvp_core.cli --state /tmp/kwvp-demo recall "staged rollout releases"
PYTHONPATH=src python -m kwvp_core.cli --state /tmp/kwvp-demo evaluate examples/judgments.jsonl
PYTHONPATH=src python -m unittest discover -s tests -v
```

The demo creates one synthetic event and a draft. Promotion is an explicit manual step. Evaluation reads synthetic judgments without creating or changing the state directory. No model or network calls are made by the runtime or tests.

To use the installed `kwvp-core` command instead, build/install from a prepared environment with setuptools 61 or newer and wheel available locally: `python -m pip install --no-build-isolation --no-deps .`. Default pip build isolation may download build tools, so use the source-only commands above for a guaranteed offline run.
## Case study

The historical evidence includes mixed and inconclusive findings:

- An initial push-channel comparison reported 17% helped and 59% noise for the main channel; a later sub-agent cohort reported 16.2% helped and 64.5% noise. Both missed the preregistered thresholds.
- A selected whitelist follow-up reported 54/84 helped (64.3%) and 11/84 noise (13.1%) across 16 parent sessions. This was early, selected, and concentrated: half of helped judgments came from one session. It does not establish general channel efficacy.
- A holdout contained 14 judgments across 9 sessions: 13 NOT_REDERIVED, one UNCLEAR, and zero REDERIVED. This is too small to establish that recall prevented re-derivation.
- Pull carry-over was 41/53 (77.4%), but a negative control was 24/53 (45.3%). The 32.1 percentage-point difference is a descriptive lift; lexical carry-over is not equivalent to usefulness.
- A blind relabeling of 14 earlier HELPED judgments found one reflected, 13 unrelated, and none unknown; agreement with the previous relabel was 10/14. One reviewer and the limited audit prevent population claims.

Promotion showed mixed topic-level results: one topic declined from 10/285 sessions to 5/366, while another rose from 10/285 to 13/366; the measure could not distinguish invoking a skill from restating its procedure. See [EVALUATION.md](EVALUATION.md) for the complete A–D case study and [docs/EVIDENCE_LEDGER.md](docs/EVIDENCE_LEDGER.md) for source-relative evidence locators.

## Evaluation highlights

The broad push cohorts missed the preregistered thresholds. A selected whitelist follow-up passed descriptively but was early and concentrated in one session. Pull carry-over exceeded its control, yet the control itself was high and the expanded judged sample exceeded the noise limit. A small holdout observed zero re-derivations but was inconclusive. Promotion results differed by topic: one skill-associated repetition declined, while another did not.

## What failed

The historical push implementation produced high noise; a lexical proxy could not separate topic overlap from utility; the whitelist follow-up was too selected and fragile to justify generalization; and the holdout was underpowered. A blind relabeling also challenged prior helped judgments.

## Limitations

Historical aggregates come from project documentation, not raw records in this release. They were not rerun here. Samples are small or selected in several analyses, judgments are imperfect, and the reported measurements do not provide a reliable causal estimate of productivity. Synthetic examples validate only deterministic mechanics.

## Repository map

- `src/kwvp_core/`: standalone reference implementation
- `examples/`: synthetic, deterministic input data
- `tests/`: local behavior checks
- `docs/`: architecture, evaluation, evidence ledger, extraction assessment, plan, and [engineering retrospective](docs/ENGINEERING_RETROSPECTIVE.md)
- `docs/CODE_PROVENANCE.md`: source-relative attribution and transformation notes

## Provenance and dependency scope

The implementation adapts three pure algorithmic ideas from a private, file-based project: character-bigram Jaccard similarity, keyword scoring, and prior-based suppression. Historical values in this case study are transcribed from project documentation and are not recomputed from private logs. The candidate uses only synthetic fixtures and has no runtime dependency on the original project, its accounts, services, or data. See [docs/CODE_PROVENANCE.md](docs/CODE_PROVENANCE.md).

## Cost and public-risk profile

| Component | Runtime cost | Data / risk boundary |
|---|---:|---|
| Synthetic demo and evaluation | Local CPU; no API calls | Generated fixture data only |
| Historical case study | No execution | Aggregate numbers only; no private identifiers or source transcripts |
| Future live integration | Not included | Would require separate privacy, security, and evaluation review |

## Repository scope

This repository contains the deterministic candidate, synthetic examples, tests, and historical documentation-based case study. It excludes the original operational harness, private session records, and production integration.

## Security and privacy

See [SECURITY.md](SECURITY.md). Do not place real session transcripts or credentials in the fixtures. The reference pipeline is not designed for production deployment.

## Example output

Running the source-only demo creates a draft. Its deterministic example output is:

```json
{
  "hash": "b5608b6cc78b20c14a85c0d8dff53db900959b6c5551e819592e961ce51ce610",
  "kind": "Decision",
  "source_ids": ["example1"],
  "tags": ["rollout"],
  "text": "Use staged rollout for releases"
}
```

The initial state has no approved items, so retrieval returns no candidates until a person promotes the current draft hash. Fixture evaluation produces the stable snapshot in [examples/evaluation-expected.json](examples/evaluation-expected.json).

## Future work

A prospective, controlled evaluation with multiple reviewers could resolve whether these mechanisms reduce rework. Any live integration would need a separate data-handling and security review. No productivity claim follows from the current evidence.

## License status

This candidate is released under the MIT License; see [LICENSE](LICENSE). The authorization and attribution decision is recorded in [LICENSE_REVIEW.md](LICENSE_REVIEW.md). See [docs/PUBLICATION_REVIEW.md](docs/PUBLICATION_REVIEW.md) for verification and publication readiness.
