# Fixed human-trained statistical references — version1

This development specification was written after inspecting the human archive
and main results, before fitting these references. It is not preregistration or
an untouched human test. The model-generation hold and locked primary target,
J_FN/J_FI and their primary/secondary status are unchanged.

The executable specification is `configs/human_statistical_references_v1.json`.
No reference is selected for a favourable main moderation or prediction score.
All three are retained. This is a practical reference under labelled-data access,
not a new method or an equal-information contest against zero-shot LLMs.

## Data and predictors

Use the complete four-profile high/low-income source pool, excluding every person
in the existing main candidate cohort and pilot. That leaves877 people with3508
human allocation labels. The target is the existing556 high/low main people and
their2224 tasks. Validate source and linkage SHA256 against the specification.
Report person overlap, design rank and both cohort hashes. Keep four rows of
each person together throughout. Person ID and task number are not predictors.

| Reference | Fixed predictors | Fitted coefficients |
| --- | --- | ---: |
| B_mean | Training-label grand mean only | 1 |
| B_recipient_OLS | Intercept plus eight recipient factors, canonical reference coding | 18 |
| B_income_interacted_OLS | The same recipient basis fully interacted with low versus high respondent income | 36 |

These simple references do not use respondent job risk or parenthood. State that
feature difference next to their labelled-human access; they are not replacements
for N/F/F-I nor a clean test of those three prompt arms. SVD least squares uses
no regularization, feature selection or hyperparameter optimization. If a design
is rank deficient, stop rather than dropping columns, resampling or silently
changing the model. This restriction does not establish contrast nonestimability.

Predictions are conditional means. Clip them to0–4000 by a rule fixed here,
report raw ranges and counts outside the range, and do not round or sample.
This declared statistical prediction rule is distinct from the prohibition on
clamping invalid respondent-model outputs. Never turn these predictions into
fabricated LLM responses, valid-call logs or individual human trajectories.

## Validation and evaluation

Within the training pool only, use five person-level folds, shuffled within
income strata by seed20261030. Report out-of-fold RMSE and MAE for every fixed
reference. Cross-validation does not select a winner or feed a main-outcome
tuning step. Fit each fixed reference to all877 training people afterward.

The prediction function must require only training labels and target predictors.
Changing main labels or ID values must not change fitted predictions. Reject
person overlap. Main labels enter only the separate fixed-design evaluator.
The researchers' prior inspection of those labels remains a limitation even
when computational leakage checks pass. Public-source pretraining exposure of
future LLMs cannot be excluded.

Evaluate continuous predictions on the same locked main rows and36-column X.
Report RMSE, MAE, both groups'30k-minus120k contrasts, their low-minus-high
difference, and existing mean/distribution diagnostics. A known finite score gets
no sampling CI. Conditional-mean prediction error or distribution compression is
not individual-trajectory fidelity. Good moderation alone is insufficient if
both component contrasts are wrong. This is a substantive reporting condition,
not a new pass threshold, composite score or selected primary endpoint.

Keep this output separately labelled human-trained reference analysis. It is
not a software oracle, a new human survey, a respondent-model experiment or
evidence that LLMs improve or worsen anything. No model calls are required.
