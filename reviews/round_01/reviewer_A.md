# Reviewer A — internal independent AI review

**Status:** Internal AI-assisted review, not external peer review. **Judgement: REVISE before main collection.** Proceed only with a narrower, prospectively frozen benchmark audit. Stop the present design as a vehicle for discovering human welfare mechanisms or validating a general agent-based social simulation. There is no demonstrated fatal defect in the paired information-arm experiment itself; there are fatal limits on those broader interpretations and major unresolved questions about contribution and measurement.

## Review scope and central assessment

I read only `packet.md`, `packet_manifest.json`, and the four enclosed Python files. I did not inspect other project files, author context, prior reviews, or another reviewer's output. I consulted primary-source literature identified below. This is a design review: no model outcomes exist in the packet, and I infer neither their signs nor their likely publication value. Code was inspected, not executed; no human data or generated artifacts were independently verified.

The question is substantively intelligible: can a synthetic survey reproduce how respondent economic position moderates allocation judgements, and does providing explicit economic information improve that reproduction? The proposed contrast is more consequential than merely matching average generosity. The controlled F versus F-I comparison also isolates a real intervention on the information supplied to a model. Neither point establishes novelty or fidelity by itself.

The smallest defensible contribution would be an estimand-specific validation result: on a declared human reference design, explicit income information changes a model's low-versus-high respondent income difference in the recipient-income allocation contrast, and changes its error relative to the human contrast by a practically meaningful amount. This would be a synthetic-survey methods case study. The packet presently lacks enough criteria and robustness evidence to know whether it will become more than a domain application of established concerns.

## Ranked issues

### A1 — Major; fatal to the broad novelty claim: the motivating failure mode is already established nearby

**Evidence/location:** `packet.md`, Research question, lines 11–13, and nearest work, lines 113–117. Taday Morocho et al. explicitly compare matched persona and no-persona survey responses and report that conditioning can redistribute errors across subgroups without clear aggregate improvement. FairFund-Bench already studies welfare-deservingness-inspired allocations and sensitivity to audit format. These overlap with the packet's motivation, not merely its background. [Taday Morocho et al., 2026](https://arxiv.org/html/2602.18462v1), [FairFund-Bench, v2](https://arxiv.org/abs/2607.28934v2).

**Consequence:** Finding that factual personas distort subgroup fidelity in another allocation task is insufficient as a general methods advance. Three arms, a larger cohort, and an evaluation wrapper do not resolve this novelty problem. A second model would test model dependence, not supply an independent substantive benchmark.

**Proposed fix:** Define the incremental claim before outcomes: human-referenced respondent-by-randomized-recipient contrast fidelity, explicit-income ablation, and whether a substantive inference changes despite acceptable aggregate fit. Supply a short comparison table of targets, interventions, human references, and failure treatment against the nearest studies. Position a single-dataset result as a case study unless it yields a reusable diagnostic whose importance is demonstrated.

**Verification criterion:** A reader can state what inference this design validates or invalidates that the nearest persona audit and allocation benchmark do not already test. The empirical result must establish that distinction, rather than simply reproduce their general warning. This review does not certify an exhaustive novelty search.

### A2 — Major; fatal to a human-mechanism claim: income moderation is not material self-interest

**Evidence/location:** `packet.md`, lines 35, 55–57 and 69–79. The primary outcome is a difference between two respondent groups' recipient-income allocation contrasts. Household income categories and recipient individual income are different measures. Neither actual respondent benefit eligibility nor a material payoff from the allocation is manipulated. The source article itself distinguishes social affinity and material interest and describes their separation as difficult. [Bridgman et al., 2021/2022, theory section](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/CA90FB810E4B2E401395F4BEA0987087/S2052263021000105a.pdf/all_in_this_together_a_preregistered_report_on_deservingness_of_government_aid_during_the_covid19_pandemic.pdf).

**Consequence:** A positive or negative gamma does not uniquely indicate self-interest, similarity, class solidarity, or their absence. A change in gamma after adding income identifies a response to model input, not a psychological mechanism. This is a limit of the design, not something larger N or model explanations can repair.

**Proposed fix:** Use “respondent-income moderation of recipient-income allocation contrasts.” Treat self-interest and affinity as competing substantive motivations for examining that statistic, not tested explanations. Do not use generated rationales as mechanism evidence. A separate mechanism project would require a design that distinguishes own material stakes from recipient similarity and deservingness.

**Verification criterion:** All primary hypotheses, result labels, and eventual conclusions remain true under alternative explanations such as learned income stereotypes, inequality preferences, or prompt demand. The present packet mostly respects this restriction; it must survive into the paper.

### A3 — Major: a fixed-design projection has a narrower interpretation than a common behavioural response surface

**Evidence/location:** `packet.md`, lines 29–35 and 69–76; `study1_interest_audit.py`, `contrast()`. X contains additive recipient attributes fully interacted with respondent group. Recipient tasks differ across actual low- and high-income respondents. Common X across outcome sources holds those differences fixed, but does not make the two groups' recipient distributions identical or make the additive specification saturated over recipient combinations.

**Consequence:** The archive-specific gamma is well defined without verifying original randomization; that is a legitimate prediction target. However, if outcomes include recipient-by-recipient interactions or pair-context effects, group-specific projection coefficients can differ partly because groups see different designs. Even a group-blind N arm can then exhibit a nonzero projected gamma. F minus F-I is an input effect on this particular projected statistic, not automatically a general effect of income labels on a common recipient-income preference. Unequal source margins alone are not proof of invalid randomization.

**Proposed fix:** Retain the fixed-design primary target and explicitly report gamma_N as a diagnostic. Add one small, common-recipient-design audit: render the same recipient tasks with high versus low income labels, holding the other supplied facts fixed. This deliberately counterfactual label intervention must be identified as such, not presented as observed respondent biographies. Alternatively, restrict interpretation entirely to the released design and avoid general response-surface claims.

**Verification criterion:** Report archive-projection and common-task label contrasts separately. A general claim about income conditioning requires the effect to survive the common-task audit; otherwise the claim must name the archive design. Show design overlap and contrast leverage, not just full rank.

### A4 — Major: disclosure of reconstruction does not establish human–model measurement comparability

**Evidence/location:** `packet.md`, lines 37–42 and 58–61. Pair membership, name assignment, and language are unavailable; pairs are reconstructed and names canonicalized. Pair answers are collected jointly in JSON and the next pair receives no previous answer. FairFund-Bench makes format sensitivity a direct empirical issue, although it does not establish the size of that sensitivity for this specific task. [FairFund-Bench, v2](https://arxiv.org/abs/2607.28934v2).

**Consequence:** A human–model discrepancy combines model behaviour with unknown presentation differences. Keeping presentation constant across arms protects the internal input comparison conditional on that presentation; it does not show that fidelity improvements transfer to the original human instrument. A recipient-income result is not exempt: comparison context and canonical names may interact with income information.

**Proposed fix:** Freeze and publish exact prompts and an original-to-reconstructed instrument crosswalk. Before expanding the sample, run a limited robustness audit using a second plausible pairing or single-profile rendering and a second balanced name mapping. Resolve original wording, time reference, health meaning, income category definitions, and independent versus shared amounts from primary materials where possible. If an aspect remains unknowable, state the resulting target as a reconstructed instrument.

**Verification criterion:** The practical conclusion about the information intervention survives these predeclared renderings, or is explicitly reported as rendering-dependent. Do not infer exact replication from valid JSON or from plausibility of the average allocation.

### A5 — Major: “improvement,” “distortion,” and “plausible aggregates” need numerical decision rules

**Evidence/location:** `packet.md`, lines 75–83. The packet correctly rejects more heterogeneity as success and nonsignificance as equivalence, but gives no substantive error margins and no explicit primary F-versus-N error-improvement estimand. Gamma_F − gamma_H and gamma_F − gamma_F-I alone do not answer whether factual conditioning improves fidelity relative to N.

**Consequence:** A significant input effect can improve or worsen fidelity, or have negligible practical importance. A human contrast estimated imprecisely near zero cannot support the claim that a model manufactures a human-absent distinction just because its own contrast is significant. “Aggregates look plausible” could become an outcome-dependent description.

**Proposed fix:** Predeclare signed discrepancy D_a = gamma_a − gamma_H, primary error change J_FN = |D_F| − |D_N|, and an income-ablation error change J_FFI = |D_F| − |D_F-I|. Choose and justify CAD margins for acceptable subgroup discrepancy, meaningful error change, and acceptable aggregate fit. Preserve signed estimates because absolute errors hide direction. Declare precisely which statistic and family are primary.

**Verification criterion:** A “harm despite aggregate fidelity” result meets a predeclared aggregate equivalence criterion and exceeds the subgroup discrepancy/error-increase criterion with uncertainty that supports that conclusion. If margins remain unresolved, report continuous estimates and uncertainty without categorical success/failure language.

### A6 — Major: sample size and uncertainty are not yet linked to the scientific decision

**Evidence/location:** `packet.md`, lines 46–48, 65, 73 and 81–83. Only 556 of 768 candidate main respondents contribute to the main low-versus-high contrast. The second-model sample has 256 respondents before subgroup division. Four judgements per person do not create four independent respondent records. The target is described both as the retained archive and through matching X on selected respondents.

**Consequence:** Resource prefixes can be outcome independent yet too imprecise to distinguish useful from harmful conditioning. A second model with an inconclusive estimate is not replication. The bootstrap's target is ambiguous if the estimand is an exact finite selected cohort rather than a broader sampling population. Conditional intervals also omit model generation variation, as the packet acknowledges.

**Proposed fix:** Declare whether gamma_H refers to the identical selected cohort or the full retained archive, and what population the respondent bootstrap approximates. Use human/design-based variance or clearly labelled synthetic planning scenarios to estimate attainable precision at each permitted budget. Choose the smallest fixed size able to adjudicate the margins in A5. Allocate a small repeat-query sample to quantify conditional generation variation if generation is stochastic; otherwise state that the estimand concerns the frozen deterministic protocol. Freeze model identity, prompt, settings, timing, and stopping rules before outputs.

**Verification criterion:** A prospective precision table connects each permitted N and subgroup count to the chosen decision margins, and the selected N is fixed for resource reasons before model outcomes. Report model versions separately; do not pool them into an implied population of models.

### A7 — Major for a reusable methods claim: the current comparator set cannot establish practical advantage

**Evidence/location:** `packet.md`, lines 96–100. There is an oracle mean-matching diagnostic but no implemented human-trained statistical comparator. The information intervention itself can be studied without one; the claim that this is a useful synthetic-survey evaluation or simulation method is harder to assess without a realistic alternative.

**Consequence:** An LLM can outperform a constant mean and still add no predictive value over a simple model of recipient factors and respondent groups. Conversely, improvement from supplying income can be real even if neither arm approaches the fidelity of a cheap statistical predictor. These are separate questions. Recent persona work also distinguishes information and training-data regimes, so comparisons require matched access accounting. [Lee et al., 2026](https://arxiv.org/abs/2610.05828).

**Proposed fix:** Keep the constant as a labelled sanity check. For any practical prediction claim, add one simple prespecified regression or regularized regression trained on disjoint human respondents, including a recipient-only and respondent-interaction version if feasible. Report access to labels, sample size, compute, and uncertainty. Human-trained and zero-target-label methods need not have equal access, but the difference must be explicit. If no baseline is added, narrow the contribution to an intervention audit, not predictive superiority.

**Verification criterion:** Held-out predictions and subgroup-contrast error are reported under declared data-access regimes. No training labels or model-selection decisions use evaluation respondents. Complexity is justified only by improved held-out fidelity or diagnostic value.

### A8 — Major to scope: these are stateless survey emulations, not evidence of a social system simulation

**Evidence/location:** `packet.md`, lines 50–61. Fresh contexts are used, previous pair answers are withheld, agents do not interact, and there is no shared resource budget, institutional feedback, or evolving state.

**Consequence:** The experiment tests a response generator's survey fidelity. It does not validate persistent respondent identities, population interaction, collective redistribution, policy feedback, or emergent politics. Calling 768 records “agents” does not add evidence about those properties. The reusable evaluator may be useful for future simulations but does not confer their validity.

**Proposed fix:** Frame the paper as validation of an information-conditioned survey response component used in some agent simulations. State that passing this test is at most evidence for the tested component and context. Do not add interactions simply to make the work appear more ambitious; that would expand the validation burden without fixing A1.

**Verification criterion:** The title, abstract, and claims describe survey emulation/component validation. Any future system-level claim comes with corresponding human or empirical system-level validation.

### A9 — Moderate, with a major reproducibility implication: the inspected audit code does not yet instantiate the final human target

**Evidence/location:** `study1_interest_audit.py`, `main()` and `contrast()`, reads the raw table and drops incomplete individual rows within the two respondent groups. `prepare_design.py` instead selects respondents with all four recipient profiles complete. `packet.md`, lines 23–26 and 69–73, declares the latter design for the benchmark. The audit's own warning describes a supplementary reanalysis, so this is not proof of a wrong main estimate.

**Consequence:** A raw-table supplementary gamma could accidentally be reused as gamma_H for a different complete-person cohort or design. Main evaluation, prompt rendering, inference, and the trained comparator remain planned rather than evidenced implementations. Assertions and a bound example do not validate the final data path.

**Proposed fix:** Give every human contrast an explicit cohort identifier, design hash, outcome scale, category mapping, and row count. Build human and model contrasts from the same frozen evaluation table. Keep the supplementary full-release/task-complete audit clearly separate. Verify income and employment definitions from the reference documentation rather than using category labels as sufficient semantics.

**Verification criterion:** A dry run with fabricated model outcomes equal to the corresponding human allocations returns exactly zero paired discrepancy on the intended cohort. Cohort and X hashes agree across arms, and the reported human gamma is demonstrably computed on those rows. This verifies implementation, not scientific novelty.

### A10 — Moderate: exact invalid-action bounds are useful hygiene until demonstrated consequential

**Evidence/location:** `packet.md`, lines 87–100; `contrast_validity.py`, `contrast_bounds()` and `verify_with_exhaustive_completions()`. The software example checks endpoint extrema of a linear contrast in a small artificial full-rank design. No actual invalid model responses exist yet.

**Consequence:** Correct completion bounds do not establish a new inference method or a meaningful empirical problem. With no invalids, they add no empirical insight; with influential invalids, they may leave the central claim unidentified. Separate bounds for each gamma are also not automatically a completed analysis of nonlinear error-improvement or equivalence decisions.

**Proposed fix:** Treat the utility as a transparent secondary contribution. Report invalidity rates and their contrast-weight leverage. If invalids occur, propagate allowed completions through the actual decision quantities from A5, distinguishing identification uncertainty from sampling uncertainty. Report inconclusiveness where bounds do not adjudicate the claim. Do not coerce or selectively discard answers to obtain a result.

**Verification criterion:** The substantive conclusion remains true over every allowed invalid completion, with the declared sampling analysis, or the paper reports exactly which conclusion is not identified. A bounds contribution requires a real example where conventional complete-case analysis would support a materially different conclusion.

## Recommended smallest core design

1. **One study, one primary contrast, a frozen protocol.** Use Study1 and the low-versus-high respondent-income moderation target. Retain N, F, and F-I; they answer distinct total-conditioning and explicit-income questions. Employment and parenthood can remain prespecified secondary endpoints. Use a fixed cohort chosen by precision rather than treating 768 as intrinsically convincing. Medium/missing-income respondents can support secondary analyses, but do not count them as primary-contrast information.
2. **One common-design sensitivity audit and one presentation audit.** A small, crossed high/low income-label audit clarifies what the model's input sensitivity means. A small predeclared alternative task rendering checks whether the fidelity conclusion rests on reconstruction. These are more informative than a large context extension.
3. **One simple comparator if claiming practical prediction value.** Train on separate retained respondents and evaluate on the frozen cohort. An intervention-only case study may omit this comparator if it also omits predictive-advantage claims.
4. **A second frozen model before another context.** Allocate enough observations to assess the same practical criterion; 256 is a budget proposal, not an evidentiary guarantee. Preserve model-specific conclusions if results differ. Defer Study2: it cannot test respondent-income fidelity with absent respondent demographics, changes instrument and outcome support, and does not distinguish pure crisis framing from program descriptions.
5. **Register prospectively what remains prospective.** Human outcomes and this dataset's substantive pattern have already been inspected. Label that provenance openly. Freeze model hypotheses, inputs, margins, sample sizes, invalid handling, and reporting before model outcomes. This can be a legitimate prospective model evaluation without pretending the human benchmark or choice of question was untouched.

## Smallest empirical result that would materially change this judgement

I would move from “revise” to “proceed as a focused methods case study” if a frozen primary-model evaluation shows a practically meaningful change in J_FN or J_FFI relative to the human contrast, with uncertainty capable of distinguishing it from trivial change; the interpretation survives the small common-task and presentation audits; and invalid completions do not overturn it. A harm claim should specifically establish acceptable aggregate fit and a materially wrong subgroup contrast under the predeclared criteria. A benefit claim should establish reduced subgroup error, not merely a larger model interaction. An adequately precise null or equivalence result is also scientifically interpretable; it supports a bounded statement about this protocol rather than an anticipated failure story.

A second model with the same qualitative, practically meaningful conclusion would strengthen the case. A genuinely independent human benchmark would be needed for a broader claim about the reliability of persona conditioning across settings. No result on this design alone would warrant claims about discovering self-interest, the psychology of crisis solidarity, national welfare preferences, or emergent political behaviour.
