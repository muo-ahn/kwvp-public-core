# Engineering retrospective

## Why the workflow was introduced

**Historical design premise:** preserve useful decisions and resolutions from prior work so later sessions can reuse them instead of rediscovering the same information. This was a hypothesis about reducing repeated search and explanation, not an observed productivity outcome.

## Documented observations

The strongest engineering lesson is that measurement definitions and controls matter more than an attractive aggregate. Lexical carry-over looked high until an unread-page control showed a 45.3% baseline. A direct judged sample landed exactly on the NOISE threshold, and the larger follow-up moved above it. Reporting the samples separately preserves that distinction.

A selected whitelist follow-up crossed its thresholds, but the window was early and the result depended heavily on one session. The small holdout saw no re-derivation but could not establish the counterfactual. Promotion counts moved in different directions by topic. A blind relabeling found only one of 14 earlier HELPED judgments reflected and agreed 10/14 with the previous relabeling. These are documented observations, not independent reruns of private records.

## Interpretation (inferred)

The broad push failure appears to be a candidate-selection problem as much as a content-value question: the historical report found high noise and strong differences between material that was used and material that was not. The inference is that broad dispatch was sending low-relevance material. That does not show all retrieval or memory methods fail.

A second inference is that a positive selected slice does not erase a failed broad cohort. Selection, early timing, and session concentration prevent a general resumption claim.

A third lesson is that automation boundaries are product decisions. In the documented workflow, a person could promote drafts and manually author reusable procedures. The public candidate preserves an explicit review gate instead of treating similarity or synthetic test success as a substitute for judgment.

## What did not work

- Broad ambient push missed its preregistered HELPED and NOISE thresholds.
- A lexical proxy had a large negative-control baseline and could not stand in for usefulness.
- A small, selected whitelist follow-up produced a promising signal but not a robust general result.
- A small holdout observed no re-derivation, but the sample could not establish the counterfactual.
- One blind relabeling pass disagreed with prior labels often enough to make the label process itself a concern.

## What we changed in this public artifact

The artifact uses synthetic events and deterministic algorithms, keeps model calls and live hooks out, binds manual approvals to content hashes, and retrieves only approved items. Historical observations are clearly labeled as documented rather than independently reproduced. The source project's runtime and private logs are not bundled.

## Next prospective test

If live utility is studied again, preregister a held-out set of sessions, use one stable rubric, have multiple reviewers label outcomes blind to condition, and measure concrete rework or re-derivation rather than lexical carry-over alone. Include a concurrent comparison condition and report reviewer agreement and uncertainty. Do not pool it with the historical cohorts.

## What remains unknown

We do not know whether this extraction reduces time, improves answer quality, generalizes across teams, or performs better than no memory. We also do not have an independent reanalysis of the historical event records in this public package. Resolving those questions requires prospective data collection, a defensible control, multiple reviewers, and separately approved data handling.
