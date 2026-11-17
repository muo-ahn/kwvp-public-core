# Security and data handling

This repository is a local, synthetic case study. Its reference implementation is not a production security boundary and is not approved for processing confidential session logs.

## Data boundary

- Fixtures must contain fabricated examples only.
- Do not add credentials, session transcripts, user identifiers, private wiki text, internal hostnames, or organization-specific URLs.
- Historical findings are reported as aggregates with source-relative section/date locators. They are not accompanied by raw logs.
- The candidate has no network integration or model-provider client. If that changes, document what data leaves the machine and obtain a separate review before use.

## Threat considerations

Input text is untrusted. Treat it as inert data; do not execute fixture content or interpret it as shell commands. Keep file reads scoped to explicitly selected fixtures. Do not use this code to infer personal behavior or rank people. Similarity and keyword scores are heuristics, not truth or authorization signals.

## Reporting a concern

Until a project maintainer and private reporting channel are designated, do not send sensitive reports through public issue trackers. For a local research copy, remove sensitive data and stop processing before sharing a minimal, non-sensitive reproduction.

## Publication scan scope

The heuristic publication scanner skips `.git`, caches, bytecode, virtual environments, build directories, distribution directories, and `*.egg-info`. A clean scan is not a security guarantee. Publish a source-only tree; do not include build, distribution, or egg-info artifacts unless those artifacts receive a separate scan.

## Deployment status

No live hooks, schedulers, network services, or production deployment are part of this candidate. Any future integration requires a reviewed data-flow diagram, retention policy, access controls, and a safe rollback plan.
