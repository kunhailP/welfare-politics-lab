# Response to round04 — author revision

Both reviewers retained prior context: critical internal AI re-review, not a new
blind round or external peer review. The packet stays unchanged. Both ran45 tests;
reviewer B additionally checked400 controls on200 unbalanced/boundary-heavy
synthetic tables. Neither independently reproduced the source-data control receipt.

| Issue | Response and evidence | Status |
| --- | --- | --- |
| A14: oracle is not observed failure | Software panel only; distributions/variances/conditional outcomes not preserved. Primary target unchanged. | Scope fixed; empirical consequence open |
| A1/A15: increment weak/unproved | Accepted unresolved judgement. `ANALYSIS_PLAN.md` states the exact question, same-output comparisons and limits of relating archive/common-task quantities. | Actual evidence required |
| A4: source table locator | Changed instrumentTable2 toTable1. Annual/individual recipient-income expansion remains removed. | Locator fixed; reviewer supported the wording correction |
| A16/B15: preservation ambiguity | Receipt specifies pooled means/additive-regression sufficient statistics. Fixture verifies equal additive coefficients and changed conditional main coefficient. | Regression passes |
| B14: unchanged table called counterexample | `has_changed_contrast_control` and conditional interpretation; all-zero/all-cap/no-shared-profile cases. | Regression passes |
| B16: no optimization certification | `sharp_extremum_certified=False`; no general sharpness/non-sharpness claim. | Semantics fixed |

Current author-revised tests total49 and pass; this does not alter the reviewers'
45-test snapshot or imply a fresh blind review. During development, a directional
fixture exposed an initial double-sign reversal, fixed before the source-data
run and frozen packet. Later test insertion placement required correction before
the current passing run. Neither is empirical model evidence.

Additional preflight found the32-person pilot matrix has rank34/36, while the
particular contrast is algebraically estimable (row-space residual about9.5e-16).
An initial author draft conflated full-rank rejection with contrast identification;
the row-space self-audit corrected it before release. `design_readiness.py`
records both properties separately, alongside full-rank
186/372/556-person primary tiers. `ANALYSIS_PLAN.md` keeps the pilot operational,
specifies a proposed full-cohort repeat and targeted presentation plan, and
marks adapters/model/cost as open. Rank and call counts do not establish power.

Generation stays disabled. Strong workshop-paper quality is the target, and
competition remains the objective; no readiness score or award probability is
manufactured from software checks.
