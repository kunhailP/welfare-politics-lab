# Contribution and execution decisions — 2026-10-29 KST

The objective remains a competition entry of strong workshop-paper quality.
Workshop quality is the standard for rigor, originality and depth; it is not a
request to wait for a journal decision. No submission-date detour replaces that
objective. This document is the author's research assessment, not a blind review.
Respondent generation remains disabled, including the pilot.

## The political-science object

The object is the **class structure of deservingness judgments**, rather than
automated eligibility administration. Which recipient income differences matter
to higher- and lower-income respondents? Does adding socioeconomic information
preserve those observed differences, impose much stronger differences, or erase
them? Welfare opinion is not adequately summarized by average generosity.
Household-income categories are observed group markers, not randomized causes.
The source cannot identify psychological self-interest or solidarity mechanisms.

Keep three objects distinct:

1. Recipient-profile generosity: how much each complete recipient profile receives.
2. Respondent-group generosity: how much each income group allocates on average.
3. Group-conditioned allocation: how recipient-income contrasts differ by group.

The new oracle control preserves objects1 and2 exactly while changing object3.
It is a diagnostic of what those summaries fail to identify, not evidence about
a language model and not a new theorem about interactions.

## What would count as a contribution

| Proposed claim | Existing overlap | Evidence still needed |
| --- | --- | --- |
| Persona inputs can distort subgroups | Already central in [Taday Morocho et al.](https://arxiv.org/html/2602.18462v1) | A generic repetition is insufficient. Show what the specified welfare contrast and explicit-income intervention add. |
| Statistical relations matter beyond averages | Already explicit in [SSDataBench](https://doi.org/10.1073/pnas.2538145123), including bivariate and multivariate checks | Do not claim prior work checks only means. Specify exactly which checks miss a result and which stronger checks would catch it. |
| Persona ablation and demographic gradients | Also studied in [economic-preference validation](https://www.nature.com/articles/s41562-026-02611-4) | Income omission alone is not a new method. Demonstrate a use-specific discrepancy with a matched human task reference. Publisher search excerpts were available; full text was not fetched in this pass. |
| Allocation format changes model judgments | Addressed systematically in [FairFund-Bench](https://arxiv.org/html/2607.28934v2) | Presentation sensitivity is a necessary diagnostic, not an independent novelty claim. |
| A practical audit of consequential welfare conclusions | Potential applied contribution; not established yet | Matched human comparison, explicit-input intervention, task-composition diagnostic, completion ranges and real presentation/repeat evidence must jointly change or qualify an inference. |

The strongest current candidate is **conclusion-level validation of conditional
welfare survey components**. The benefit is a defensible decision about what a
particular generator can support, under declared inputs and tasks. It is not a
general replacement for human participants or an interacting society model.
No desired sign of J_FN is an inclusion or publication criterion.

## New offline diagnostic and its limits

`marginal_control.py` transfers integer allocations around four-row cycles:
low-income respondent/profile A, high-income respondent/profile B, high-income
respondent/profile A, low-income respondent/profile B. Positive and negative
transfers cancel within each income group and within every complete recipient
profile. All allocations remain integer0–4000. Thus the construction preserves
the grand mean, both respondent-group means, every complete-profile mean and
pooled additive-regression sufficient statistics. It does not preserve conditional
group-by-profile outcomes, distributions or individual trajectories. The greedy
construction has no general optimality certification.

On the fixed556-person design, the observed human contrast is55.16 CAD. Two
outcome-informed software tables preserve the summaries above while producing
contrasts1900.26 and-1752.22 CAD. They change652 and657 rows respectively.
**These are constructed counterexamples, not model responses, statistical
uncertainty intervals or empirical estimates of model error.** A diagnostic that
already evaluates the correct group-by-profile interaction would detect them.
The construction does not establish novelty relative to such a diagnostic.

This replaces the weak human-mean-only example as the principal *software*
sanity check. It does not replace the actual N/F/F-I experiment or change its
cohort, primary contrast, loss or input rules. The control reads outcomes only
in the evaluation environment and must never enter generation inputs.

## Evidence required at each decision

| Decision | Required evidence | Current status |
| --- | --- | --- |
| Engineering pilot | Coherent incremental question; source crosswalk; frozen repeat/presentation plan; isolated native request/log path; model/settings and budget | Incomplete; do not generate |
| Main collection | Frozen campaign; operational pilot accounting, validity and missing contrast weight; planned repeat/presentation diagnostics; no tuning on confirmation outcomes | No pilot exists; do not generate |
| Strong paper/award case | Real results interpreted against closest work; useful limits or advances; supporting diagnostics; actual platform reproduction, paper and demo | Cannot be established from design tests |

These are evidence gates, not scores that predict acceptance or awards. Review
quality and test counts cannot substitute for experimental evidence. A limited
pilot is eventually necessary to learn model-dependent quantities; waiting for
publication certainty before any empirical work would be circular. Its execution
remains conditional on satisfying its own readiness requirements and budget.

## Competition rubric: gaps that matter

The [official competition](https://socioverse.fudan-disc.com/challenge/) weights
are25/25/20/20/10. This is a qualitative gap map, not an assigned jury score.

| Dimension | Weight | Deliverable and unresolved requirement |
| --- | --- | --- |
| Social-science value/novelty | 25 | Explain the class structure of deservingness and the incremental inference beyond existing persona/structure audits. Not established by changing datasets. |
| Design rigor | 25 | Same-task N/F/F-I, reconstruction crosswalk, task-composition audit, repeat/presentation plan and failure bounds. Live isolation and diagnostics remain open. |
| Results/theoretical contribution | 20 | A substantive, qualified finding supported by actual responses. Currently no model results. |
| Reproduction/engineering | 20, mandatory gate | Actual native study layout, saved-output replay and new-call separation, model/call/cost logs and one command. Offline core passes; final platform package does not yet exist. |
| Presentation/potential | 10 | A4–8-page evidence-based report and actual-run demo/replay. No simulated success story or fabricated results. |

## Next bounded research iteration

1. Finish the source-to-prompt crosswalk and specify the targeted repeat and
   presentation comparisons before adding endpoints or unrelated interactions.
2. Independently criticize whether this particular audit would add an inference
   beyond the nearest published benchmarks. Retain a negative verdict.
3. Implement the native isolated execution path and validate it with labelled
   software controls. No engineering success alone opens model generation.
4. Reassess the engineering-pilot gate using concrete artifacts. Prioritize
   testing this bounded claim over an expanding catalogue of generic metrics.

Competition outcome and eventual peer review remain external decisions. The
user's aim is a high-quality competitive entry; no artificial numeric win or
acceptance probability is assigned.
