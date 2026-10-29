# Anonymous prospective welfare-allocation validation protocol

No respondent-model generation has occurred. This is a prospective component
validation developed after source-human outcomes were inspected, not an untouched
human test or preregistration of those results. No author identity, career goals,
award objective, prior reviews or prior conversations are supplied.

Question: which class-conditioned recipient-income allocation comparisons are
supported by generated responses, and does adding observed socioeconomic facts
improve a fixed human-reference moderation score without hiding errors in its
two group components? Explicit-income omission remains a secondary comparison.

Source: Bridgman et al., All in This Together? A Preregistered Report on
Deservingness of Government Aid During the COVID-19 Pandemic,
https://doi.org/10.1017/XPS.2021.10 ; data10.7910/DVN/LPHMB7.
Study1 has2295 released people/9180rows,2003 complete4-profile people. Complete
high/low pool1458; main candidates768 include556 high/low people/2224rows;
pilot32 include25 high/low. Training/reference remainder877 are disjoint from
all main/pilot candidates. Completeness is income-dependent; this is a selected
finite benchmark, not nationally representative. Released assignment margins
are nonuniform and full probabilities unverified: fixed-design descriptive
regression contrasts, not causal AMCE or causal own-income/self-interest.

Every person has two reconstructed pairs(1,2),(3,4), with separate monthly0-4000
CAD allocation per recipient, not a shared budget. Names/language/pair IDs are
not released; stimulus_crosswalk.md discloses reconstruction assumptions. Each
pair uses a fresh context; earlier answers and human outcomes never enter prompts.
N=no own facts;F=own household-income/job-risk/parenthood;F-I=F minus explicit
income. These are fixed observed facts, not individual digital twins. F-I may
still convey inferred income. Main requests3x556x2=3336 before retries/repeats.

X is canonical recipient intercept/dummies followed by every interaction with
low-versus-high own-income indicator. gamma is low-minus-high respondent difference
in recipient-income30k-minus120k contrast. Human gamma is known on the fixed cohort.
Primary J_FN=abs(gammaF-gammaH)-abs(gammaN-gammaH) compares the three-fact bundle.
Secondary J_FI usesF-I instead ofN; also report signed gammaF-gammaFI.
Both component slopes and their signed errors must appear next to gamma.
No population sampling/decoding-expectation CIs or p-values are planned, and no
importance/equivalence/pass threshold is justified. Raw CAD discrepancies only.

Strict whole-pair integer JSON0-4000; invalid replies leave both unknown, without
clamping or semantic retry. Only transport errors retry up to3 total attempts.
Keep fixed rows/denominators; exact SVD linear completion bounds and conservative
absolute-loss/W1 ranges. Keyed logs bind arm,person,A/B mapping,rollout,prompt,
modelID and attempts. Consistency does not authenticate a provider. N can exhibit
moderation from unequal tasks under nonlinear group-blind responses.

Additional evaluation software includes same-output means/distributions, stronger
group-by-profile check with many singleton cells, and explicitly outcome-informed
permutation controls. None is empirical model evidence or a new theorem.
Common-task plan16bases x3 income labels x2 focal incomes=96requests; equal-base
DID is model-only input sensitivity, not a human counterfactual or subtraction
based decomposition of archive gamma. Repeats and presentation/model checks are
proposed, not yet executable frozen manifests. Seeclaim_specification.md.

Fixed statistical references use877 disjoint training people/3508 human labels,
not main labels, with all3 fixed models retained and person-level5-fold internal
CV. Different label access/features/output targets from prospective LLMs are
explicit. Continuous conditional means are not fabricated respondent trajectories.
The source and main results were already inspected during development; computational
separation does not remove that history. Author result files are supplied for
checking, not desired conclusions. Private raw supplement permits independent
Study1 numerical checking; no model outputs or native runner are supplied.

Execution status: offline analysis/evaluation components only. Native SocioVerse
execution/isolation, exact model/settings, total cap, live repeat/presentation
adapters and actual model evidence remain unfinished. No generation permission
is conferred by this review. A rigorous component is not a finished empirical study.
