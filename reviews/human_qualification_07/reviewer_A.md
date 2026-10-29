# Reviewer A — human-reference qualification 07

**Internal AI-assisted limited re-review with my earlier context retained; not a fresh blind review or external peer review.** I read the authorized question, aggregate report, audit script and its packet-local design dependency. No raw data, parent repository, authoring conversation or other review was read. **All source aggregates below are author-calculated and were not independently verified from raw data.** I did not use test counts as evidence of scientific readiness.

After the frozen packet was supplied, the coordinator explicitly authorized one additional primary source: arXiv:2609.33055. I inspected its current arXiv abstract, whose metadata identifies v2 dated 18 October 2026. Version-specific PDF retrieval failed, and the unversioned PDF returned inconsistent older title/page-count information; I therefore do not claim full-text verification of the new v2 experiments. This additional literature exposure is part of this re-review.

**Judgement: the human audit improves interpretation and weakens a tempting headline; it does not establish the remaining methods contribution. A narrow, nontrivial empirical question remains possible, but the overlap threat is now stronger.** Keep the locked finite-cohort score, but revise the claim and freeze the income-specific comparison, component diagnostics and practical comparator before collecting model outcomes. Do not turn a small sign reversal into a political discovery.

## A19 — Major: the closest new literature substantially reduces the distinctiveness of income omission and manipulation

The added primary-source abstract already combines human socioeconomic structure, counterfactual income changes and income omission, with omission checks in three models. It reports substantial dispersion compression alongside preserved income structure and distinguishes changes in predicted means from changes in dispersion. Thus neither “does explicit income drive socioeconomic structure?” nor the combination of human matching, counterfactual labels and removal is a strong novelty claim here. [Powdthavee, current arXiv abstract, v2 metadata](https://arxiv.org/abs/2609.33055).

The welfare proposal still differs in its target: respondent-income moderation of a recipient-income allocation contrast on recorded conjoint tasks, rather than an income gradient in well-being dispersion. That distinction is real, but changing outcome/domain and coefficient does not by itself constitute a substantial methods advance. Prior persona/subgroup and relational-fidelity work remains overlapping as already acknowledged.

**What remains potentially nontrivial:** Whether explicit socioeconomic conditioning preserves or distorts *who differentiates between lower- and higher-income aid recipients, and by how much*, relative to matched human judgements; and whether task composition, presentation or invalid actions materially change that assessment. This can be a focused welfare-politics component-validation study. To become more than a domain application, actual results must reveal a consequential, well-diagnosed limitation or use case. The new human audit does not supply that result. Full-text comparison with the new paper should precede any precise “not previously tested” claim.

## A20 — Major: the income-specific question and the named primary loss change still differ

**Evidence:** `question.txt` asks about explicit own-household-income conditioning but identifies J_FN as the primary loss change. N to F adds income, job risk and parenthood together. Only F versus F-I isolates omission of the explicit income sentence, conditional on the other facts. Correlated remaining facts can still convey income information.

**Consequence:** J_FN < 0 would support a closer score after adding the three-fact bundle, not an income-specific benefit. J_FN > 0 would not establish that income caused the deterioration. This is an interpretation gap even if every software operation is correct.

**Minimum correction:** Keep the locked primary score and state its bundle-level question accurately. Explicitly place J_FI = |gamma_F−gamma_H|−|gamma_F-I−gamma_H| and the signed F-minus-F-I contrast alongside it as the prespecified income-specific analysis, maintaining their existing secondary/companion status rather than silently replacing the primary. Name which conclusion each comparison can support. None identifies a human psychological mechanism.

## A21 — Major qualification: the audit varies the reference, not just its moderation sign

**Evidence:** `aggregate_report.json::main/disjoint_remainder/matched_draw_distributions` and `audit_human_reference_stability.py::main/summarize`.

The author-reported main group-specific recipient-income contrasts are about **136 CAD for high-income and 191 CAD for low-income respondents**, versus **249 and 370 CAD** in the disjoint remainder. Moderation is about **55 versus 121 CAD**. The main high-group slope is below the reported draw q05, and its low-group slope is close to the reported draw minimum. Those comparisons are descriptive locations in the specified sensitivity exercise, not rejection tests. They show that the qualification concerns absolute group responsiveness as well as the sign of their difference.

Both group-specific contrasts are positive in all 500 reported draws, whereas moderation is negative in 34. This supports distinguishing a comparatively persistent *descriptive recipient-income ordering in these sampled subsets* from a less stable moderation direction. It does not show that the main sample is invalid, biased or selected for its outcome. The locked finite target remains mathematically legitimate.

**Limits that matter for the claim:**

- The 500 sets reuse one remainder archive. They are not 500 new human datasets or independent empirical replications. More draws refine the specified subset-sensitivity distribution; they do not create new human information.
- The main target is excluded from the draw pool. The reported quantiles are not a confidence interval around its gamma, nor a coverage statement for its score. The 466/34 count is not a population sign probability or evidence that the population moderation differs from zero.
- Changing people changes their four tasks and the projection design. Fixing high/low counts does not fix recipient distributions, other respondent facts or leverage. The exercise cannot separate human heterogeneity from task-composition changes or identify the source of the difference.
- The full pool contains the main cohort, and the disjoint remainder was already inspected during development. Neither is an external or untouched validation sample. Source selection, missing profiles, procedural reconstruction and population limits persist.

**Minimum correction:** Report the two group-specific contrasts next to gamma for every actual model arm as a diagnostic decomposition of the existing endpoint, not a new selected primary endpoint. A model can obtain gamma approximately right by getting both group slopes wrong in the same direction. Likewise, erasing moderation can look competitive against a small main gamma without reproducing the larger within-group recipient-income preferences. Keep source-cohort sensitivity separate from main-model scoring; do not rescore the same main-model coefficient against remainder gamma as if it were the same X/target. Do not subtract the model-only common-task DID as a decomposition of either human projection.

## Results that would still be insufficient

The following technically correct findings would not establish the proposed scientific increment:

- A model reverses the small positive main gamma, described as overturning class solidarity, self-interest or human welfare politics. The mechanisms are unidentified, and the new audit directly cautions against a sign-based story.
- All model groups favour 30k over 120k recipients, or adding personas changes gamma. Those are coarse directional/response checks, not a substantial advance over existing work.
- A small negative J_FN on one rollout, described as a benefit of explicit income, reliable respondent simulation or policy-relevant improvement. The comparison changes multiple facts, the target is local, and there is no importance or stability criterion.
- F-I retains a group pattern, presented as a new discovery that explicit income is unnecessary. The added literature already studies that possibility, and this archive also permits composition-induced group differences.
- The human 500-draw sensitivity exercise, the permutation oracle or stronger same-output diagnostics presented as actual generator validation. They qualify interpretation and verify evaluation properties; they do not supply model evidence.
- Good aggregate or conditional-distribution scores standing alone. The eventual judgement must also inspect the prespecified contrast, its component slopes, direct error changes and any invalid-action ranges on the same outputs.

## A22 — Useful comparator proposal, not yet an evidentiary answer

Training a simple statistical predictor on the 877 disjoint people could make the practical case more assessable. Freeze its permitted features, model class, internal person-level validation, hyperparameter-selection criterion and evaluation procedure before actual main-model outcomes. No main outcomes should select them. Keep all four rows of a person together in validation, and state that the reference was available to the researchers during design.

Use the same main tasks and metrics, including the two group slopes and gamma, for the trained predictor and model arms. Disclose its human-label access and cost. A zero-shot LLM is not guaranteed never to have encountered this public source in pretraining; describe project-level training access accurately rather than claiming proven absence of human-data exposure. This comparator can establish a practical reference under different information regimes, not an equal-resource contest or independent human replication.

## Minimum next revision and decision

The next change should be a short prospective empirical claim-and-analysis specification, not another control or another round of resampling:

1. Identify bundle-level versus explicit-income comparisons and preserve the locked primary target. Name the concrete inference about recipient-income preferences that is being audited; retain continuous CAD reporting and mechanism/population restrictions.
2. Add high/low component contrasts to the fixed reporting table; retain the source-sensitivity qualification without choosing a more favourable human subset or seed.
3. Freeze the simple disjoint-human comparator and its data-access accounting. Finalize repeat and presentation designs, model/settings/cost, and isolated native execution/log adapters before lifting the declared generation hold.
4. State in advance how actual common-task, presentation and invalid-action evidence will qualify the model result. A useful result may show benefit, distortion, mixed performance or non-identification. A generic persona effect or sign reversal is insufficient.

**Proceed only as a narrowly positioned prospective welfare-allocation audit after those remaining gates are resolved; the present packet does not establish an empirical methods advance.** If the eventual finding amounts only to “the income sentence changes an error score on this cohort,” without meaningful diagnostic or practical context, the remaining contribution is a limited domain replication. The new human audit is valuable precisely because it prevents overinterpretation; it should not be converted into evidence that the larger contribution has already been secured.
