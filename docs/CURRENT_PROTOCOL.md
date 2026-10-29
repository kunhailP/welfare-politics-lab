# Current protocol: version 3, after first independent internal review

This is a prospective plan for model data, developed after viewing the human
reference data. It is not a preregistered or untouched human replication.
`archive/RESEARCH_PROTOCOL_V1.txt` records the previous plan; this document
supersedes its broad causal-AMCE interpretation, population scope and ordinary
bootstrap confidence interpretation. Round01 was independent and context
separated; round02 is a re-review with each reviewer's own prior report visible.

## Question and theoretical target

Does observed socioeconomic conditioning improve synthetic welfare support,
or distort the group structure of that support while preserving plausible
aggregate allocations? Distinguish overall generosity, recipient-attribute
contrasts and differences in those contrasts across respondent groups.
Income-group moderation is descriptive; it does not identify the causal effect
of household income, self-interest, solidarity or a psychological mechanism.

## Reference population and selection

The released Study 1 has 2,295 people and 9,180 judgments. Complete four-profile
records exist for 2,003 people. Completion rates differ by household income:
799/854 high, 659/813 low, 384/438 medium, 161/190 missing income. The eligible
pool is this retained archive. The primary target is the exact selected high/low
cohort and its recorded tasks conditional on fixed X, not Canadian citizens in
general. Diagnose selection and compare available-case human contrasts as a
sensitivity analysis; weighting alone cannot recover unrecorded profile facts.

Published statements about random profiles do not reveal the full assignment
probabilities in the released table. Study 1 citizenship and employment margins
are strongly nonuniform. This is a source-verification question, not proof the
original trial was invalid. Until resolved, call the primary statistic a
**fixed-design regression contrast**, not a new causal AMCE.

## Population and input intervention

Seed 20261029 draws 32 pilot people and a disjoint 768-person main candidate
cohort. Main household-income counts are high304/low252/medium140/missing72.
Only556 people enter the primary contrast; the other212 are not counted as
primary information or required primary requests. Three arms therefore require
3336 primary pair requests before retries.
Resource-only prefixes256/512/768 may be chosen before model generation. Do not
select the size by p-values or model performance.

Use identical respondent IDs and recipient tasks in three fresh-context arms:

| Arm | Observed socioeconomic facts |
| --- | --- |
| N | None |
| F | Household income category, employment risk, parenthood |
| F-I | Employment risk and parenthood; income sentence omitted |

No ideology, age, personality, human outcomes, hypothesized result, paper title
or authoring chat is supplied. Missing income is omitted consistently. Household
income is different from recipient individual income. F-I can still allow
inference about income through correlated facts; it removes explicit income
information only. Request order is randomized inside respondent blocks.

## Stimulus operationalization

Study 1 uses two reconstructed profile pairs with separate monthly allocations
0–4000CAD per recipient; there is no shared4000 budget. Two requests generate
four judgments per person and arm. Prior model answers are not fed into the next
pair. Stable observed facts do not constitute an individual digital twin.

Published Appendix D supplies levels and name pools. Original name assignment,
language and pair IDs are absent. Pairing1/2 and3/4 is an assumption. Canonical
names preserve recorded gender/ethnicity; English/French white-name sensitivity
must be recorded. Health means a pre-existing complication-risk condition in
Study1; it must not be replaced by generic poor health from Study2. JSON is an
adaptation of the original slider. Claims concern this operationalization.

## Estimands and models

Let X include all recorded recipient factor dummies, an indicator for low versus
high household income and its interactions with all recipient factors. Medium
and missing household income are outside the primary contrast, but remain in
descriptive reports and applicable secondary comparisons. Fit the same X to
human and each arm's allocations.

Let gamma be the low-minus-high respondent difference in the recipient income
contrast30k versus120k. The main fidelity discrepancy is gamma_F - gamma_H.
The explicit-input intervention is gamma_F - gamma_F-I. Improvement requires
directly comparing the human-reference errors, not merely more heterogeneity.
Never infer a difference from one significant and one nonsignificant estimate.

Primary continuous loss change: J_FN=|gamma_F-gamma_H|-|gamma_N-gamma_H|.
Negative means closer on this finite benchmark. Secondary income-ablation loss
change: J_FI=|gamma_F-gamma_H|-|gamma_F-I-gamma_H|. Preserve signed errors.
No policy-relevance margin is justified yet: categorical claims of acceptable
fidelity, equivalence, meaningful harm or success are disabled. Raw CAD effects
and a50/100/200CAD sensitivity grid are descriptive, not validated substantive
thresholds. An exact finite score does not establish scientific importance.

A group-blind nonlinear rule can have nonzero gamma_N under unequal profile
distributions. Tests reproduce a600CAD example and its zero contrast under
common profiles. Do not infer hidden income knowledge or stereotypes from
gamma_N alone. Report joint support, conditioning and contrast leverage.

Secondary contrasts: respondent employment risk by recipient pandemic-related
job loss; parenthood by recipient young children. Report all specified contrasts.
These are secondary descriptive endpoints. No p-values are planned for the
finite-cohort main analysis. A future inferential extension must separately
define its population, multiplicity family and validated procedure.

## Uncertainty and invalid actions

Gamma_H is known on the exact observed cohort. Report descriptive discrepancies
and loss changes for a recorded rollout, without an ordinary respondent-bootstrap
CI for the fixed-cohort score. This is not an expected-decoding-response target.
Repeated generations on a predeclared subset can diagnose model stochasticity;
they are not new humans. Any respondent reweighting is a task-composition stress
test, not a95% interval for the finite cohort or national population. Archive
sampling or model-expectation inference remains an unresolved extension needing
an estimator and coverage/precision validation. No nonsignificance is equivalence.

Strict JSON integer actions in0–4000 are required. Never clamp, infer numbers
from explanations, or substitute rule outputs for refusals. Retry transport
failures at most twice; log every attempt and cost. Report failures by arm,
respondent group and recipient attribute.

For a fixed full-rank X, an OLS contrast is w'y. With invalid entries represented
as unknown actions in0–4000, compute its exact min/max over all completions.
This does not assume random failure or turn refusal into an observed amount.
Completion bounds and human sampling uncertainty are different objects. Missing
regressors cannot be repaired by bounds for missing outcomes.

Report missing absolute contrast weight and exact linear completion width
4000*sum(abs(w_missing)). Subtract arm intervals for linear input-effect bounds;
conservatively propagate absolute-error ranges to J_FN/J_FI. Interval-hull ranges
need not be sharp for integer actions and are not confidence intervals. Point
identification uses a documented1e-8CAD numerical tolerance; irrelevant zero-weight
missing rows do not destroy it. SVD weights replace normal equations.

Design-only failure diagnostics consider random and highest-leverage paired
failures at0.5/1/2/5/10%. A95% validity pilot is only a basic format check, not
evidence of useful ambiguity. Larger N need not shrink bounds at a fixed rate.

## Baselines, model replication and context extension

N/F/F-I are the real generation comparisons. A human-mean constant is an oracle
software diagnostic: it matches the mean by construction and has zero recipient
effects. A human-trained regression, if added, requires disjoint training people
and explicit label/computation budgets. Neither comparator is mislabelled a
zero-information forecaster.

Verify the chosen model and total cost using the pilot, freeze them before main
generation, then prioritize a second model on256 of the same main people. Do
not choose the second model because its results strengthen a preferred claim.

Before a context extension, prioritize a16-base common-task audit crossing
counterfactual low/high/omitted respondent income with focal recipient30k/120k,
holding all other facts and the companion profile fixed:96 requests/model.
These are model-only counterfactual labels, not observed biographies or new
human validation. A small predeclared alternate-pairing/name audit remains
required for presentation-robust claims; source reconstruction cannot be repaired
by assuming good average allocations imply exact replication.

Study2 is a lower-priority context extension with128 people per original frame,
four single profiles each, no invented respondent persona. Exact minority-name
and outcome-order assignment is unavailable. It changes institution description
with context, and has an unbounded dollar response. Do not impose the Study1
cap, call this a pure crisis effect, or merge studies into a longitudinal panel.
Report raw and normalized effects separately.

## Execution and claim gate

No paid runner exists in this version. The offline pipeline generates source
diagnostics, human reanalysis and whitelisted inputs only. A future native
SocioVerse study must log actual transmitted prompts, responses, returned model
IDs, failures and costs; saved-output replay must be separated from new calls.

Before generation: resolve or disclose reconstruction assumptions; qualify the
target population; freeze primary contrasts, failure handling, model, size and
budget; verify reference outcomes cannot enter the request path. Papers will
report null or mixed evidence, not tune the prompt until a desirable result.

The proposed method is an applied validation procedure. Its substantive value,
increment beyond existing benchmarks, and transferability require actual results
and independent critical review; packaging alone does not establish novelty.

## Unresolved collection gates

Model identity/settings, native isolated runner/logging, campaign cap, justified
scientific decision/precision criteria, repeated-generation allocation and
presentation sensitivity remain incomplete. Actual respondent calls are0.
Software validation resolves implementation issues; empirical importance and
generalization still require evidence. A revised plan is not a completed study.
