# Prospective analysis plan — inherited version6, protocol7 wording addendum

Protocol7 retains the estimands and proposed audits below. Its shared system
instruction explicitly attributes supplied facts to the participant in all arms.
Prompt hashes change before generation; human design does not. The sealed
core-receipt check binds scorer files only; complete live campaign binding
remains unfinished. See `CURRENT_PROTOCOL.md` and `RESPONSE_LOG_FORMAT.md`.

Written after observing the human reference and before any new respondent-model
output. This is not an untouched preregistration of the human study or permission
to generate. Primary cohort and J_FN/J_FI remain in `CURRENT_PROTOCOL.md`.

## Exact inference and same-output comparisons

On the matched welfare tasks, does explicit household-income conditioning make
the recorded respondent-income moderation contrast closer to the human reference,
and can task composition, invalidity or stimulus operationalization change that
interpretation? Report all arms, signed errors and both loss changes; no choice
of trait, prefix, model or rollout based on favorable confirmation outcomes.

Apply these checks to the **same actual outputs**:

| Check | Object and interpretation |
| --- | --- |
| Grand mean | Overall generosity error |
| Respondent-group means | High/low generosity errors; not group-conditioned recipient effects |
| Complete recipient-profile means | Pooled profile errors, weighting cells by fixed row counts; not respondent-by-profile fidelity |
| Primary interacted contrast | Same36-column X; gamma discrepancy, J_FN and J_FI |
| Stronger conditional check | Group-by-profile errors or interactions; can detect the oracle too |

The public keyed evaluator now reports group/profile weighted mean-error bounds
and empirical-distribution W1 ranges on the same fixed rows. A stronger
group-by-profile check is included. This is not an
exact reproduction of every SSDataBench metric. Keep invalid actions in fixed
denominators with completion ranges; selective complete-case summaries cannot
establish the unconditional claim. No arbitrary “good fidelity” threshold.

The software panel now includes a distribution-preserving permutation control:
it preserves the overall, income-group and pooled complete-profile allocation
multisets, and the fixed additive projection/R2, but not group-by-profile
conditional outcomes or individual trajectories. The earlier mean-only control
is retained as historical/supporting evidence. Neither demonstrates that real
models pass restricted checks while failing stronger ones.
The archive gamma and common-task DID have different tasks and weights:
**do not subtract them as a mechanical decomposition**. Common-task label effects
are model input sensitivity without observed human counterfactual biographies.

## Pilot and resource preflight

The frozen32-person engineering pilot has25 high/low people and100 primary
rows. Its36-column design has rank34. The specific primary contrast is nevertheless
algebraically estimable: its distance from the row space is about9.5e-16. The
current evaluator deliberately requires full rank and rejects this pilot matrix;
that implementation limit is not proof the contrast itself is unidentified.
The pilot is operational in this plan and cannot certify the main score's
stability. A pilot-contrast extension would need an explicit estimable-contrast
implementation, rather than silently substituting another regression.

Outcome-independent prefixes of the main candidate cohort give:

| Candidate people | Primary people | Rows | Rank/columns | Pair requests/rollout |
| --- | --- | --- | --- | --- |
| 256 | 186 | 744 | 36/36 | 1116 |
| 512 | 372 | 1488 | 36/36 | 2232 |
| 768 | 556 | 2224 | 36/36 | 3336 |

Reproduce with `scripts/design_readiness.py`. Full rank establishes feasibility,
not power, practical importance or generator stability. Prefixes change the
finite target; choose resources before confirmation outputs, not by their signs.

## Proposed stronger repeat/presentation campaign

Plan three full recorded rollouts on the chosen main cohort, all arms, with the
same frozen model/settings/tasks. R0 is primary; R1/R2 are predeclared replications.
Report each score and completion range and the finite observed range across
rollouts. Do not choose the best run or call three runs an expected-response CI.
The full768-candidate option uses10008 primary pair requests before audits/retries.
If resources permit only one, restrict the claim prospectively to its recorded
finite score. Model/settings/budget and per-rollout live adapters remain open.

Before generation, select64 main high/low people,32 per group, by seed20261030
from sorted IDs without outcomes. Use identical people/rows for:

1. Baseline pairs1/2 and3/4 with canonical English white names.
2. Alternate pairs1/3 and2/4, all other wording fixed.
3. Baseline pairs with French white names; other ethnicity mappings fixed.
4. Baseline pairs with A/B reversed, preserving source profile IDs.

Each additional variant uses64×3×2=384 requests; three add1152/model. The common-
task audit adds96, and an all-income32-person operational pilot adds192. With
three main rollouts this proposed full campaign totals11448 requests before
retries/second model. This is a call count, not a dollar quote or executable
frozen manifest. Pricing/platform support must be verified before generation.

On these64 people, report rowwise allocation changes and contributions under the
**full main design's weights**. Do not refit36 columns on a small subset and call
it a main-contrast replication. These local contributions do not bound all
untested tasks or establish nationwide/whole-generator robustness.

The live manifest must bind variant and rollout even when messages coincide:
identical prompts do not justify merging fresh-generation replicates. This
audit/campaign adapter is not implemented. Freeze repeat/presentation choices
before outputs; never choose a variant because it strengthens the preferred sign.

## Contribution test and failure reporting

Report actual invalidity and missing contrast weight by arm/group/recipient
attributes. Label any complete-case comparison and show its fixed-design
completion ranges. Inconclusive ranges remain a result; no invalid substitution
or semantic-refusal retries to obtain a preferred outcome.

Scientific value requires an actual welfare-specific inference or consequential
validity limit after these diagnostics. Injected failures and oracle controls
verify analysis but cannot establish an empirical consequence. Human mechanisms,
population inference, predictive superiority and persistent-society claims remain
outside this design. Null, improved, mixed or inconclusive outputs are admissible.
