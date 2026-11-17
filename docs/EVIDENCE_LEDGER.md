# Historical evidence ledger

This ledger points to source-document summaries, not to raw event records. SHA-256 values identify the exact documentation text used for this draft; they do not identify a runtime, source revision, or raw dataset. None of the historical figures below were independently recomputed from private logs for this publication.

| Public claim | Source-relative locator | Source document SHA-256 | Evidence status |
|---|---|---|---|
| Main push comparison 17% HELPED / 59% NOISE; sub-agent comparison 24% / 47%; pull final 45% / 23% | `docs/pull-quality-measurement.md`, §§5.6–5.7 and final channel comparison, dated 2026-08-10, lines 156–160, 179–204 | `a650c4065918c2d7b19357b4740b60aa7feac36bc3131b44285b753b215e33d1` | DOCUMENTED; arithmetic not independently reproduced |
| Sub-agent broad cohort n=628, 44 sessions, HELPED 16.2%, NOISE 64.5% | `docs/verdict-10-subagent-2026-08-27.md`, §§1–2, dated 2026-08-27, lines 1–21 | `03f1dcce2dbf0938f35b4c7f2fb561215573a58f927f85fceccc21a64f20b9be` | DOCUMENTED; historical logs unavailable here |
| Selected whitelist follow-up n=84, 54 HELPED, 11 NOISE; 16 parent sessions; one session accounts for 27/54 HELPED | `docs/verdict-10-subagent-2026-08-27.md`, follow-up §11.2–11.3, dated 2026-09-22, lines 485–521 | `03f1dcce2dbf0938f35b4c7f2fb561215573a58f927f85fceccc21a64f20b9be` | DOCUMENTED; selected, shortened-window observation |
| The 2026-09-22 window was moved early and the result is sensitive to session concentration | `docs/verdict-10-subagent-2026-08-27.md`, follow-up §§11.1–11.5, dated 2026-09-22, lines 475–505, 590–604 | `03f1dcce2dbf0938f35b4c7f2fb561215573a58f927f85fceccc21a64f20b9be` | DOCUMENTED; broad efficacy INCONCLUSIVE |
| Pull carry-over 41/53 versus 24/53 control, lift 32.1pp; 20-judgment initial result and 53-judgment expanded result | `docs/pull-quality-measurement.md`, §§5.5–5.7, dated 2026-08-10, lines 90–204 | `a650c4065918c2d7b19357b4740b60aa7feac36bc3131b44285b753b215e33d1` | DOCUMENTED; lexical lift is not utility |
| Holdout 14 judgments, 13 NOT_REDERIVED, one UNCLEAR, zero REDERIVED; nine sessions | `docs/l3-utility-measurement.md`, §8, dated 2026-10-02, lines 91–110 | `ec9aa63d2eaec88d3a3b953a92c9ec33365cd8958738b19081f991e5957b9d72` | DOCUMENTED; source itself classifies as insufficient-sample / inconclusive |
| Promotion before/after counts: clipboard topic 10/285 to 5/366; peer-review topic 10/285 to 13/366; skill calls differ from utterance counts | `docs/midreview-2026-09-30.md`, §§1–1.2, dated 2026-09-30, lines 8–34; `TODO.md`, § “2026-10-17 KWVP wiki curation wave,” lines 217–223 | `docs/midreview-2026-09-30.md`: `06abbf8253fd6ccd5de4ed243b49c048a4faa4da24d700f5e1e555cea129fa78`; `TODO.md`: `0667ea8db2c473c6b26d7d5ea1f721f1abccd5f6130d8ca522f198b125f76b54` | DOCUMENTED; observational counts; causal conclusion INCONCLUSIVE |
| Blind relabel: 14 earlier HELPED judgments, one reflected, 13 unrelated, zero unknown; agreement 10/14 with prior relabel | `TODO.md`, “2026-10-17 KWVP wiki curation wave,” WC2 first step, lines 217–220 | `0667ea8db2c473c6b26d7d5ea1f721f1abccd5f6130d8ca522f198b125f76b54` | DOCUMENTED summary; selected and single-reviewer; no population inference |

## Interpretation rule

“DOCUMENTED” means a claim appears in the cited historical project documentation. It does not mean the underlying logs are included, the result was independently reproduced, or the design establishes causality. “INCONCLUSIVE” describes the strength of the inference where sample, selection, control, or reviewer limitations prevent a broad conclusion.
