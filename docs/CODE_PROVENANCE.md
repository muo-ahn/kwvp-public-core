# Code provenance

The candidate extracts small deterministic mechanisms from the source repository, not its transcripts or configuration:

- `harness/scripts/knowledge-refine.py:1091-1106`: character-bigram Jaccard, source Git blob `bf6f967985a096c7d4646c2fefdb6cfa01df83c3`.
- `harness/hooks/lib/wiki_index.py:28-35,133-149`: stop words and weighted page score, source Git blob `2ac23beae56e754223286413b9ff0bc063aecdcc`.
- `harness/hooks/lib/verdict_prior.py:228-298`: union of zero-help and proportional suppression rules, source Git blob `cdc5803796b7afcd1827819c56e653b4cff3d6db`. Adaptation uses explicit counts and thresholds, validates inputs, and removes random retesting and environment defaults.

Other pipeline code and synthetic fixtures are new. The candidate is released under the MIT License in the repository root. Source attribution above is retained.
