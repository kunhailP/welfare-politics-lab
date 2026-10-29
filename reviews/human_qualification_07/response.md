# Human-reference qualification07: response and limits

This is a targeted internal AI re-review, with each reviewer's own earlier
context retained. It is not a new context-blind review or external peer review.
The frozen packet contains aggregate source results but no raw observations.
Both reviewers distinguish author-computed source results from independent
synthetic/script checks. Neither received the other report during review.

After packet freezing, both reviewers received an additional primary-source
link, arXiv:2609.33055, and a synopsis of its current v2 abstract. Reviewer A
independently inspected that abstract and recorded the PDF version discrepancy;
reviewer B records synopsis exposure only. The frozen packet was not overwritten.

| Issue | Response | Remaining limitation |
| --- | --- | --- |
| A19: new literature substantially overlaps income manipulation/omission | `EMPIRICAL_VALUE_PLAN_KO.md` now cites that source and FairFund-Bench, and withdraws any implication that these operations establish novelty | A substantial welfare-specific empirical increment remains unproved; v2 full text was not verified |
| A20: explicit-income question differs from bundle-level primary J_FN | Memo distinguishes primary F-versus-N three-fact bundle from secondary F-versus-F-I/J_FI and direct signed income comparison | No silent primary switch or human-income causal interpretation |
| A21: component slopes also vary across source cohorts | Memo reports high/low slopes next to moderation and explicitly limits sign/magnitude interpretation | People and recipient tasks change together; this does not estimate uncertainty for the locked main score |
| A21: gamma can look right with both group slopes wrong | Prospective reporting now requires both component contrasts alongside the existing endpoint | Live public evaluator reporting of those component bounds is still to be implemented before generation; no empirical model comparison exists |
| A22/B comparator: disjoint training alone does not settle data access or validation | Memo labels the comparator proposed/unimplemented and specifies person-level internal validation, no main-label tuning and unequal label access | Exact model, features, tuning and output rules are not frozen; no superiority result |
| B18: numerical roundoff at zero is counted as positive/negative | Author script now uses explicit1e-8 CAD numerical-zero tolerance, retains all raw signed values, and adds a roundoff regression test | This is not a substantive/equivalence margin. Reviewers did not independently verify the post-review patch |
| B full-rank restriction | Retain fail-fast behavior, with no redraw-until-full-rank | This is a script support restriction, not proof a particular contrast is unidentifiable; broader reuse would need additional diagnostics |

## Author verification after the numerical fix

`runs/human_stability_02` uses the patched script. All500 source draws have rank36;
the summaries and466/34 moderation sign count are identical to the earlier run.
An independent invocation in a fresh output directory produces byte-identical
report, draw-estimate and membership files. The main contrast agrees with the
locked `human_reference_design.npz` within1e-8 CAD, and the raw source SHA256 is
unchanged. All59 repository tests pass in the existing tested environment.
This is not a new clean dependency installation. The aggregate receipt is
`docs/HUMAN_STABILITY_VALIDATION.json`.

These are author checks, not independent review of the source aggregates or of
the final patch. Reviewer B independently exercised the frozen script with
synthetic CLI data and diagnosed the zero-count defect. Reviewer A's central
judgement remains: the audit improves interpretation but does not establish a
methods or empirical contribution. Both reports retain that limitation.

## Next scientific action

Freeze a short bundle-level/explicit-income empirical specification and a
disjoint-human practical comparator, with the closest literature included.
Preserve the locked finite target, source-sensitivity qualification and proposal
status of unimplemented components. If the comparison yields no substantive
increment beyond known persona effects, reconsider the central question rather
than adding further oracle examples. Model execution/settings/cost and actual
evidence remain unresolved; generation stays on hold.
