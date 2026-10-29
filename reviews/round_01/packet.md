# Anonymous research proposal: independent review packet

Review the proposal and enclosed code critically. This packet intentionally
omits author identity, affiliations, project-hosting URL, prior conversations,
previous reviews and intended competitive outcomes. No empirical model data
have been collected. Human results have already been inspected by the authors.
This is an internal AI-assisted review, not external venue peer review.

## Research question

Does conditioning synthetic survey respondents on observed socioeconomic facts
improve reproduction of welfare support, or distort group-specific recipient
allocation contrasts even when aggregate allocations look plausible?

## Human reference and limitations

The reference is Bridgman et al., doi:10.1017/XPS.2021.10, replication archive
doi:10.7910/DVN/LPHMB7. Study1 has2,295 people with4 judgments each. Respondent
household income, employment risk and parenthood are recorded. Recipient income,
employment, citizenship, gender, ethnicity, health, marital status and children
are supplied as conjoint factors.

Recipient employment is missing in438 of9,180 released rows. Keeping people with
four fully recorded recipient profiles leaves2,003 people. Income-group retention
is high799/854, low659/813, medium384/438, missing161/190. The benchmark target
is the retained complete-profile archive, not a representative national sample.
No released survey weights are available.

The paper describes randomized profiles, but released Study1 margins include
citizenship counts7344 born citizens/1218 noncitizens/618 other citizens and
employment counts2746 pandemic-unemployed/2274 other unemployed/1897 full-time/
1825 reduced income/438 missing. Their assignment and preprocessing provenance
is not fully established. No uniform assignment is assumed. The primary human
statistic is a fixed-design projection contrast, not an asserted new causal AMCE.
Respondent income and mechanisms such as self-interest are observational.

Original pair IDs, individual name assignment and language are not distributed.
The proposal reconstructs pairs1/2 and3/4 and uses canonical names consistent
with recorded gender/ethnicity. The published Appendix D supplies levels and
name sets. Its Study1 poor-health factor means pre-existing COVID complication
risk, unlike generic poor health in Study2. JSON replies adapt a slider task.
The operationalization is disclosed as reconstructed, not exact procedural replay.

## Controlled model experiment

Seeded selection of32 pilot people and a disjoint768-person candidate main
cohort. Main household income groups: high304/low252/medium140/missing72.
Resource-only prefixes256/512/768 can be fixed before observing model outcomes.

All selected people receive the same recipient tasks in three arms:
N: no observed socioeconomic facts.
F: household income category, employment risk, parenthood.
F-I: F without explicit household income.

No invented ideology, age or personality. Missing income remains unprovided.
The intervention concerns explicit input information, not all income knowledge.
Household and recipient individual incomes are different units. Fresh contexts
across arms; prior pair answers not fed to the next pair. Same canonical names,
pairing, response format and model settings across arms. Request order is
randomized within respondent blocks. Two pair requests each return separate
0–4000CAD amounts per recipient; there is no shared budget.

The pilot is for protocol validity, identity/cost and storage, not fit to human
outcomes. No model, campaign spend, or main output has been collected. The design
plans a second model on256 of the same people before a context extension.

## Estimands

Fit the same full-rank design X to the human and each model-arm outcomes.
For the main contrast X includes all recipient-factor dummies, a low-versus-high
household-income indicator, and all their interactions. Gamma is the difference
between low- and high-household-income respondents in the recipient30k-versus120k
allocation contrast. Other household income groups are outside this contrast.

Fidelity discrepancy: gamma_F - gamma_H.
Explicit-input effect: gamma_F - gamma_F-I.
Improvement requires comparing errors relative to gamma_H. More heterogeneity
alone is not success. Compare contrasts directly rather than separate p-values.
Secondary endpoints: employment-risk by pandemic job-loss contrast, parenthood
by recipient young-child contrast. Report all; define families and Holm-adjust
any inferential p-values. Bootstrap whole respondents with all four judgments,
human outcomes and model arms paired,1000 draws. Model-version/general decoding
uncertainty is outside those intervals. No significance is not equivalence.

## Failure handling and reusable component

Strict JSON integers0–4000. No clamping, semantic answer repair or rule-based
fallback. At most two transport retries with full logs. Report invalids by group,
arm and profile factor. In fixed X, an OLS contrast is w'y. Assign invalid records
unknown allowed actions in0–4000 and compute exact lower/upper contrast bounds.
No random-failure assumption. Bounds do not identify a refusal's actual intended
allocation or solve missing regressors; human sampling intervals remain separate.
Enclosed contrast_validity.py verifies the formula against32 exhaustive endpoint
completions in a synthetic software case; it is not actual model evidence.

The component will accept human reference and model trajectories, report mean,
recipient and group-effect fidelity, information-arm differences and invalid-action
completion bounds. The mean-matching constant is explicitly an oracle diagnostic;
a trained statistical comparator, if added, needs disjoint training respondents
and declared labels/cost. No human-trained baseline is currently implemented.

## Extension and scope

Study2 provides2,501 different people assigned either general GST rebate or
crisis relief, four single profiles each. Its respondent demographic fields are
absent, and name minority subgroups and outcome-order IDs are unavailable.
A256-person extension with128/frame is lower priority and supplies no invented
demographics. Responses are unbounded dollars, so the finite-action bounds do
not transfer. Program descriptions and context change together. Do not identify
pure crisis effects, use normalized contrasts alone to infer solidarity, or
combine studies into an individual longitudinal panel.

Current nearest work includes FairFund-Bench(arXiv:2607.28934v2), persona versus
no-persona survey reliability(doi:10.1145/3774905.3795477; arXiv:2602.18462),
data-derived personas(arXiv:2610.05828) and multi-experiment treatment-effect
prediction(Nature s41586-026-10742-x). The authors do not claim first persona
ablation, first synthetic survey, or novelty for the linear bound formula alone.

## Questions for the reviewer

Identify fatal validity/novelty issues, overclaims, untestable mechanisms,
assumptions requiring verification, statistical failure modes, and better minimal
alternatives. Rank issues by severity; distinguish scientific gaps from missing
implementation. For each provide evidence/location, consequence, concrete fix
and a verification criterion. Do not reward complexity or assume the intended
result. Give a clear proceed/revise/stop judgement for the present design and
the smallest convincing empirical result that would materially change it.
