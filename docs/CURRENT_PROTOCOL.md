# Current protocol: version 7, reviewed handoff and explicit participant background

Version7 inherits the version6 cohort, estimands and primary/secondary hierarchy.
Before any respondent generation, the shared system instruction makes F/F-I
facts explicitly the participant's own background, identically across arms.
All prompt hashes intentionally change; human design
and endpoints do not. Version6 is archived in
`archive/PROTOCOL_V6_PRE_FINAL_REVIEW.md`. The CLI checks design/request files
against a pre-generation core receipt with an externally recorded digest. This
binds input files, not a complete live campaign or provider authenticity.
The final09 review used two fresh contexts and a separate private source
supplement for independent numerical checks. Post-review fixes and their author
verification are in `../reviews/final_09/response.md`; actual model generation
and the unresolved empirical/execution conditions remain unchanged.

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
Income groups mean observed household-income bands, not class identity, assets,
occupational class or actual voting. Report directions, CAD magnitudes and errors
within observed/completion-possible outcomes; no binary global fidelity label.

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
income is a respondent field, separate from recipient pre-pandemic income. The
printed recipient instrument does not explicitly state its time unit; the
renderer does not add an annual-unit assertion. F-I can still allow
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

Canonical names can repeat within a pair. All prompts now explicitly state A
and B are distinct hypothetical people even if names match. The frozen primary
plan has143 such pairs among1112 pair tasks per arm (429 of3336 requests).
This discloses and mitigates ambiguity; it does not establish harmlessness.
The presentation audit must test the chosen handling before robustness claims.

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

Design-only failure diagnostics consider one seeded random-failure scenario,
the analytic expected width under a uniform subset, and highest-leverage paired
failures at0.5/1/2/5/10%. A95% validity pilot is only a basic format check, not
evidence of useful ambiguity. Larger N need not shrink bounds at a fixed rate.

## Baselines, model replication and context extension

N/F/F-I are the real generation comparisons. A human-mean constant is an oracle
software diagnostic: it matches the mean by construction and has zero recipient
effects. The three fixed human-trained references use877 disjoint people with explicit
label access and continuous-mean interpretation. Neither these references nor
the oracle is a zero-information forecaster.

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

Freeze common-task summaries before any responses: for each base b and label
l, D_bl=Y_bl,30k-Y_bl,120k for the focal recipient. Report equal-base means of
D_low, D_high, D_omitted, plus mean(D_low-D_high) as the principal common-task
diagnostic; low-minus-omitted and high-minus-omitted are secondary diagnostics.
Each base has weight1/16. Zero-based even bases put the focal recipient in A;
odd bases put it in B, identically across all six cells. Base contexts can
share a source person and are not independent human observations. Missing cells
stay explicit unknown actions in0–4000; calculate linear completion bounds
without deleting incomplete bases. A missing log is an accounting error.
One recorded rollout is planned for this descriptive diagnostic; expected-model
or stochastic-stability claims are disabled until a repeat plan is frozen and
executed. `common_task.py` verifies additive/interaction fixtures and missing
cells. Version0.3's `common_task_responses.py` verifies keyed offline attempt
logs against the sealed original plan before summarizing. Actual web-platform
call/export integration is still required before execution. Its stable audit
IDs and explicit currency/credit accounting do not change these estimands.

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

Loaded arm files are now checked for duplicate people, identical populations,
empty N facts, and F-I exactly equal to F minus income. Frozen requests bind
arm, respondent, profile-to-A/B mapping, rollout and prompt hash to a request
ID. The offline `recorded_responses` entry point requires explicit keyed
attempt logs and rejoins them to frozen row IDs. It rejects contradictory,
duplicate, missing or unexpected logs and changed returned-model IDs; only
transport errors may be retried, up to three total attempts. An invalid reply
ends that request and leaves both actions unknown. Exhaustion requires all
three transport attempts to be recorded. Human, design and contrast hashes
are stored. These consistency checks do not authenticate a provider or replace
generation isolation. The array-only numerical API is a labelled evaluation helper,
not the public path for model logs. End-to-end copied-human replay is explicitly
software-only evidence, never a model result.

Before generation: resolve or disclose reconstruction assumptions; qualify the
target population; freeze primary contrasts, failure handling, model, size and
budget; verify reference outcomes cannot enter the request path. Papers will
report null or mixed evidence, not tune the prompt until a desirable result.

The proposed method is an applied validation procedure. Its substantive value,
increment beyond existing benchmarks, and transferability require actual results
and independent critical review; packaging alone does not establish novelty.

## Evaluation-only development addendum: marginal-preserving controls

The primary N/F/F-I estimands and cohort are inherited from version4; version5
removes the unsupported annual/individual expansion in recipient income wording
and records its source crosswalk. A new evaluation
diagnostic constructs integer outcome-informed tables with identical means for
each income group and each complete recipient profile but changed group-by-
recipient contrasts. `marginal_control.py` verifies exact conservation and action
bounds. These are oracle software checks, not predictions or empirical model
findings. They preserve neither individual trajectories nor conditional
group-by-profile outcomes. A correctly targeted interaction audit detects them.
The construction is not sharp optimization or a new theorem; its role is to
make the insufficiency of the specified marginal checks concrete. It may read
human outcomes in evaluation only. Do not expose its outputs to generation.

Generation, including the engineering pilot, is on a research-development hold.
Source reconstruction, repeat/presentation design and native execution remain
pre-collection requirements. A new evaluation control does not resolve them.

## Unresolved collection gates

Model identity/settings, native isolated runner/logging, campaign cap, justified
scientific decision/precision criteria, repeated-generation allocation and
presentation sensitivity remain incomplete. Actual respondent calls are0.
Software validation resolves implementation issues; empirical importance and
generalization still require evidence. A revised plan is not a completed study.

## Same-output diagnostics and stronger software control

Version6 retains the primary cohort, prompts, contrast and loss definitions.
For every arm, the keyed evaluator adds empirical W1 distances for the full
allocation distribution, income-group distributions, pooled complete-recipient-
profile distributions and group-by-profile distributions. Conditional distances
and absolute cell-mean errors use fixed row-count weights. Report cell counts
and singleton counts: these are finite sample comparisons, not estimates of
conditional population distributions or individual psychological fidelity.
No pass/equivalence threshold is introduced. The additive recipient-basis-plus-
group projection reports coefficients/fitted-value differences and R2 only if
all actions are observed; constant-outcome R2 is undefined, not perfect.

For missing actions, all cells/denominators remain fixed. A computational
midpoint anchor gives conservative W1 completion ranges by the triangle
inequality: radius2000*m/n for m unknown actions in a cell of n fixed rows.
The midpoint is not an observed/imputed answer. These are not sharp bounds or
confidence intervals; exact complete-data distances are separately identified.
No full-cohort R2 is calculated from complete cases or anchor-filled outcomes.

The new outcome-informed permutation control swaps existing amounts in disjoint
four-row checkerboards. It preserves the overall allocation multiset, each
income-group multiset and each pooled complete-profile multiset. Therefore the
corresponding distributions/means/variances and fixed additive projection/R2
stay equal, while income-by-recipient interactions can change. This is a known
higher-order association issue made concrete on this design, not a new theorem.
The stronger group-by-profile check detects the changed control and is included
in the comparison, rather than presenting the target contrast as uniquely able
to detect it. Other respondent traits, trajectories and conditional joint tables
need not be preserved. No real model failure, benchmark-wide failure or novel
empirical discovery is inferred from a constructed table. Additional respondent
model calls required for these evaluation checks: zero.

## Evaluation addendum: fixed statistical references and group components

The original version6 primary target and primary/secondary loss definitions are
unchanged. `EMPIRICAL_CLAIM_SPEC_V1.md` specifies the narrowed prospective claim
and reporting table after human analysis, before any respondent generation.
The public evaluator now reports both group-specific components of the primary
interaction contrast, signed reference errors and exact completion bounds.
Under this fully interacted design the components use disjoint groups; their
continuous-completion joint feasible set is rectangular. Other restricted or
partially interacted designs need not share that property. Gamma still uses its
own direct contrast weights. Components are diagnostics, not selected endpoints
or a new composite success score.

`HUMAN_STATISTICAL_REFERENCES.md` and its version1 config fix three simple
conditional-mean references before fitting: training mean, recipient-only OLS
and income-interacted OLS. They use877 people outside all existing main/pilot
candidates and person-level5-fold training diagnostics, retaining all models.
Main labels enter evaluation only. Prior research inspection of those labels is
disclosed. Their human-label access and continuous-mean predictions differ from
the LLM arms; they are neither zero-information forecasters nor simulated
trajectories. Fixed statistical predictions may be clipped under their declared
rule; invalid LLM replies may not. The remaining generation gates persist.
