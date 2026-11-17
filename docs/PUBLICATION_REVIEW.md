# Publication Review

## Implementation

This is a source-only, standalone candidate and a documentation-based case study. The candidate repository contains deterministic event validation and refinement, hash-bound manual promotion, approved-only recall, a separate synthetic judgment evaluator, sample fixtures, tests, and public documentation. No live hook, production integration, model adapter, automatic skill generation, or historical raw log is included.

The public report keeps historical observations separate from candidate behavior. The included synthetic expected output is a deterministic fixture snapshot, not a reconstruction of historical results. The source project's ownership, current global hook boundary, and extraction exclusions are described in [ARCHITECTURE.md](ARCHITECTURE.md) and [EXTRACTION_ASSESSMENT.md](EXTRACTION_ASSESSMENT.md).

On 2026-11-16, the user confirmed rights to publish this candidate, selected the MIT License, and authorized public repository creation and push. The standard license is now in the repository root. This documents the user's authorization; it is not an independent legal opinion or separate verification of third-party rights.

## Verification

## Prepublication verification snapshot (2026-11-16, before authorization)

The final verification run reported the following. This task made no writes to the original source checkout or global configurations. While packaging was pending, the shared source checkout advanced to a later merge commit; a subsequent full file-tree comparison found no content differences from the initial snapshot. The cause of that history movement is not attributed. The public candidate is a separate repository with no source history inherited:

- `docker run --network none ... python -m unittest discover -s tests -v`, Python 3.12: 10 tests passed.
- `python -m pip --disable-pip-version-check wheel --no-index --no-deps --no-build-isolation --wheel-dir /tmp/wheels /tmp/package` using locally available setuptools 79 and wheel 0.46.3, followed by `python -m pip --disable-pip-version-check install --no-index --find-links /tmp/wheels kwvp-core` into a fresh Python 3.11 virtual environment: 10 tests passed.
- Installed CLI exercised outside the checkout for demo and fixture evaluation; the test suite also verified recall returns no result before approval and returns the approved item after promotion.
- Ruff with cache disabled: passed.
- Differential comparison against isolated AST-extracted source functions passed for 200 random Jaccard pairs, 200 keyword-score cases, and all 1,771 valid suppression count combinations through total 20 with retesting disabled. This validates those pure mechanisms only, not operational pipeline utility.
- Publication scanner: zero findings. A separate manual sweep found no company/internal domains, home paths, email addresses, or UUIDs in staged source files.
- Python 3.9 in-memory checks: 5 passed; complete run was blocked by temporary-directory cleanup `EPERM`. A host Python 3.13 run had the same cleanup issue.

One initial Docker run copied an ignored stale build artifact and failed one test. The source-only clean copy was rerun and passed. An earlier local wheel-build attempt also encountered environment cleanup `EPERM`; the clean offline wheel and fresh-environment installation passed afterward. These attempts are recorded as environment/artifact failures, not hidden as successful runs.

## Evidence

Historical measurements are supported by source-relative documentation locators and SHA-256 digests in [EVIDENCE_LEDGER.md](EVIDENCE_LEDGER.md). Raw records were not included or reprocessed. Historical claims are therefore classified DOCUMENTED, not REPRODUCED. Conclusions remain INCONCLUSIVE where selection, sample size, reviewer agreement, controls, or counterfactual design do not support a general claim.

Synthetic CLI and test outputs are REPRODUCED for the candidate only. They show deterministic mechanics and do not establish historical accuracy, usefulness, or productivity effects.

## Security

The candidate makes no model or network calls at runtime. Fixtures are fabricated. The scan found no identifying data, but absence of findings is not proof of complete de-identification or rights clearance. The publication scanner is heuristic and skips `.git`, caches, bytecode, virtual environments, build directories, distribution directories, and `*.egg-info`; a clean scan is not proof of safety. Publication must use a source-only tree unless excluded artifacts receive a separate scan.

No credentials, transcripts, private wiki content, personal paths, or internal identifiers are included in the staged public files. The application is not a production security boundary and has no production deployment. The scan does not independently establish rights; user rights confirmation and MIT selection are recorded above and in `LICENSE_REVIEW.md`.

## PublicationReadiness snapshot

The table below preserves the prepublication acceptance snapshot recorded before the user authorized license selection and public release. AC12 therefore describes that historical cutoff, not the current authorization state.

| AC | Acceptance criterion | Status | Evidence / note |
|---|---|---|---|
| AC01 | Original private repo/global harness unchanged | BLOCKED | This task made no source/global writes and the file tree compares identically to the initial snapshot, but the shared source checkout history advanced during packaging. Therefore the strict repository/history invariant cannot be certified. No actor is attributed. |
| AC02 | Separate dir/new Git history | PASS | Candidate is in a separate directory with a freshly initialized repository, unborn `main`, zero commits, and no remote. No source history or author metadata was imported. |
| AC03 | Minimal synthetic knowledge pipeline E2E | PASS | Typed fixture event ingest, deterministic refinement, draft hash, manual promotion, approved-only recall, and synthetic evaluation were exercised. |
| AC04 | Offline tests no LLM/API | PASS | Docker tests ran with network disabled; runtime and tests make no LLM or API calls. |
| AC05 | Major evaluation logic testable/reproduction documented | PASS | Synthetic evaluation has pinned expected output and tests; 200 Jaccard pairs, 200 keyword-score cases, and 1,771 suppression combinations were differentially checked against isolated source functions. Historical reproduction limits are documented. |
| AC06 | Actual results vs limitations distinguished | PASS | EVALUATION and EVIDENCE_LEDGER separate documented historical aggregates, reproduced synthetic behavior, and inference limits. |
| AC07 | Success/failure/inconclusive included | PASS | Broad push failures, selected whitelist follow-up, pull results and control, holdout, promotion outcomes, and reliability audit include positive, negative, mixed, and inconclusive findings. |
| AC08 | Company/personal sensitive data and real transcripts excluded | PASS | No private records or identifying artifacts are included. Scanner and manual staged-file sweep reported zero findings; a clean scan is not proof of complete de-identification. |
| AC09 | Empty environment install/demo/tests | PASS | A source-only offline wheel was installed into a fresh Python 3.11 environment and passed 10/10 tests; Docker Python 3.12 passed 10/10. Python 3.9 subset checks passed 5 cases, but a full run was blocked by cleanup `EPERM`. |
| AC10 | README Architecture Evaluation Retrospective written | PASS | README, `docs/ARCHITECTURE.md`, `EVALUATION.md`, and `docs/ENGINEERING_RETROSPECTIVE.md` are present. |
| AC11 | Source comparison/exclusions documented | PASS | `docs/CODE_PROVENANCE.md`, `docs/ARCHITECTURE.md`, and `docs/EXTRACTION_ASSESSMENT.md` document extracted mechanisms, source-relative locators, ownership boundary, and exclusions. |
| AC12 | No external publication; final approval pending | PASS | No remote, push, release, or external transmission had occurred at the prepublication snapshot. |

**Prepublication snapshot status: BLOCKED pending rights/license authorization and owner approval.**

## Current release status (2026-11-17)

The approved release is published at [https://github.com/muo-ahn/kwvp-public-core](https://github.com/muo-ahn/kwvp-public-core), whose default public branch is `public-core`. Publication completed through the connected GitHub API after the direct CLI push did not succeed; no TLS verification was disabled and no secrets were read. No protected-branch write or merge was performed. All 24 remote files were independently fetched and matched the local release manifest exactly. The repository is licensed under MIT via the root `LICENSE`, as authorized by the user on 2026-11-16. This records the user's rights confirmation and release authorization, not an independent legal opinion.

The AC01 BLOCKED result remains as a historical prepublication finding: the shared source checkout's history advanced during packaging, though its file tree matched the initial snapshot. AC12 also remains a prepublication snapshot only; it is not a statement about the current release. CI status is not asserted here.
