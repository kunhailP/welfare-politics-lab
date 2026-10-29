# Author response and implementation record — round01

Two independent internal AI reviews were obtained with separate contexts and
without author history or the other review. Both judged REVISE before main data
collection. Neither review is a venue decision. We accept the need for revision.

The current protocol is version3. The main evaluation is now the exact selected
high/low cohort, fixed X, one recorded rollout. We removed ordinary respondent
bootstrap CIs and categorical fidelity/equivalence claims from the primary
specification. Archive/general-population or expected-decoding inference remains
an unresolved extension, not a silently assumed benefit of a bootstrap.

| Issue | Response | Verification / remaining condition |
| --- | --- | --- |
| A1 novelty | Narrowed; open empirical issue | RELATED_WORK.md distinguishes the specific contrast and intervention; actual diagnostic value is unproved |
| A2 human mechanism | Claim restricted | CURRENT_PROTOCOL excludes causal self-interest/solidarity interpretations and generated rationales as mechanism evidence |
| A3 projection composition | Implemented diagnostic; empirical robustness open | Two synthetic tests reproduce nonzero group-blind gamma and remove it on common profiles; common_task_plan generates96 crossed model-only requests |
| A4 reconstructed instrument | Partial | Renderer preserves declared levels, separate amounts and recorded fact semantics; original language/pairs remain unknown; rendering sensitivity is still required |
| A5 loss/meaningfulness | Continuous losses implemented; margins open | J_FN/J_FI and signed errors are explicit; categorical acceptable/meaningful claims disabled rather than choosing convenient thresholds |
| A6 sample/uncertainty | Target restricted; repeat/precision planning open | Actual primary cohort556/2224, rank36, condition52.07; no finite-cohort sampling CI claimed |
| A7 practical comparator | Scope restricted; comparator deferred | No predictive-superiority claim; any trained baseline needs disjoint humans and declared labels/cost |
| A8 simulation scope | Claim restricted | Survey-response component validation; no interaction, emergent politics or persistent digital-twin claim |
| A9 cohort mismatch | Implemented | primary_design.py builds one exact cohort, checks all4 profiles and outcomes, hashes X/rows/contrast; copied-reference check returns zero discrepancy |
| A10 bounds utility | Partly implemented; empirical value open | Missing leverage, completion width and conservative nonlinear error-change bounds; actual failures/results remain absent |
| B1 inferential target | Target restricted | Finite selected cohort and recorded rollout, not finite archive expectation or superpopulation; inferential extensions remain gated |
| B2 exclusion mismatch | Implemented | Primary rejects a missing profile rather than silently deleting it; supplementary raw-row audit remains explicitly separate |
| B3 improvement/precision | Partly implemented; substantive criteria open | Continuous loss and signed errors implemented; no unvalidated pass/fail or equivalence claims |
| B4 failure ambiguity | Implemented diagnostic; collection feasibility open | Actual-X preflight tests random/high-leverage failed pairs; even1% can give broad ranges; no claim more N cures ambiguity |
| B5 uncertainty implementation | Unsupported primary promise removed | No ordinary bootstrap CI in fixed-cohort main analysis; model repeats and any inferential method still need implementation and validation |
| B6 group-blind counterexample | Implemented and interpreted |600CAD nonlinear example, common-design zero example, common-task counterfactual plan; gamma_N need not be zero |
| B7 operational intervention | Core planning implemented; live runner open | Whitelisted renderer, exact F/F-I income-sentence difference, no arm labels in messages, seeded interleaving, strict whole-pair parser; actual model logs/native runner remain absent |
| B8 selection | Scope restricted | Income-dependent eligibility retained in all claims; no weighting/imputation recovery asserted |
| B9 identification flag | Fixed and tested | Zero-weight missing rows can be point identified within declared tolerance; SVD weights and condition guard; new adversarial tests |

## Offline verification

31 unit tests pass. `scripts/reproduce.py --output runs/revised_02` completes
human reanalysis, design/selection audit, per-arm inputs, matched primary design,
planned requests and design-only failure ambiguity. Primary3336 planned requests
are not actual calls. The96 common-task audit requests are counterfactual model
inputs with no observed human reference.

The actual-X failure preflight shows that12 invalid pairs(about1.08%) imply a
193.45CAD completion width in the seeded random pattern and420.05CAD when
concentrated on largest contrast weights. This is a design calculation, not an
observed model failure rate. A95% valid-output pilot alone is therefore not a
scientific readiness criterion.

No reviewer issue requiring empirical fidelity, practical usefulness, presentation
robustness, model-repeat inference or novelty is marked resolved by these tests.
