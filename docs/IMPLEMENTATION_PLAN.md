# Implementation plan

## Scope

Deliver a small, runnable research reference implementation and a transparent account of historical evidence. This plan describes the candidate artifact, not a production rollout.

## Phases and acceptance criteria

1. **Source boundary and provenance**
   - Record the three adapted pure algorithms and source-relative locators.
   - Exclude private logs, credentials, company identifiers, internal page names, and local paths.
   - Make no claim of ownership or license clearance without an authorized decision.

2. **Deterministic candidate**
   - Define typed synthetic events and a deterministic refinement pipeline.
   - Implement character-bigram Jaccard similarity, keyword scoring, and prior suppression without external services.
   - Require a hash-bound manual approval record before an item is retrievable.
   - Keep model adapters, automatic procedure generation, and live hooks out of scope.

3. **Reproducible demonstration**
   - Provide a fixed synthetic fixture and documented CLI commands.
   - Tests demonstrate deterministic behavior, rejection of stale or unapproved items, and fixture evaluation.
   - Clearly label all outputs as synthetic mechanics checks.

4. **Evidence-backed case study**
   - Give every experiment the same reporting structure: hypothesis, setup, measurement, sample, baseline/control, results, limitations, decision, reproduction instructions, and evidence classification.
   - Separate historical documentation from reproduced results.
   - Preserve failures and conflicting follow-up samples rather than pooling them.

5. **Release review**
   - Check links, commands, fixture provenance, and public-risk review.
   - Decide license only after ownership and relicensing authority are confirmed.

## Deferred work

No live hook integration, model provider, production retention, automatic skill generation, or claim of time savings is included. Reconsider only with a preregistered evaluation, privacy review, cost estimate, and explicit rollback plan.
