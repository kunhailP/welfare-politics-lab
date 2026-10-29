# Welfare Politics Lab

Human-grounded tests of whether synthetic citizens reproduce the structure of
welfare support. The central experiment separates overall generosity, recipient
attribute effects, and differences in those effects between respondent groups.
It compares an unconditioned role, three observed socioeconomic facts, and the
same facts with explicit household income removed.

**Status:** design and offline human-data analysis. No new respondent-model
calls, empirical model results, or paid generation have been performed.
This is an AI-assisted research workspace, not a claim of publication or awards.

**Execution hold:** the user prioritizes a competitive contribution with strong
workshop-paper rigor, originality and depth. Pilot and main respondent generation
remain disabled. [Contribution and decision criteria](docs/CONTRIBUTION_AND_DECISION.md)
map the unresolved evidence to the official competition rubric.
The prospective [analysis plan](docs/ANALYSIS_PLAN.md) specifies same-output
diagnostic comparisons and proposed repeat/presentation checks. The
[source crosswalk](docs/STIMULUS_CROSSWALK.md) records reconstruction limits and
the pre-generation recipient-income wording correction.

The current design is version6 in [docs/CURRENT_PROTOCOL.md](docs/CURRENT_PROTOCOL.md).
Archived plans document earlier decisions; they are not the current authority.
Open scientific issues are in [docs/RESEARCH_QUEUE.md](docs/RESEARCH_QUEUE.md).

## Offline reproduction

Python 3.11 or newer is required. Install the tested dependencies in an isolated
environment, then run from the repository root:

```bash
python -m pip install -r requirements-tested.txt
PYTHONPATH=src python -m welfare_politics.ingest --archive /path/to/dataverse.zip
PYTHONPATH=src python scripts/reproduce.py --output runs/check_01
PYTHONPATH=src python -m unittest discover -s tests
```

Each output directory must be new. Reproduction reads the local archive and
does not call a model or access a network. Raw files are not distributed here.
Acquire them from [Harvard Dataverse](https://doi.org/10.7910/DVN/LPHMB7).
Source provenance and licensing boundaries are in [data/README.md](data/README.md).

The output includes Study 2 human reanalysis, Study 1 adjusted group contrasts,
source-design and selection diagnostics, outcome-free per-arm generation inputs,
and a software-only verification of missing-action contrast bounds. Reanalysis
is not an exact recreation of every R package's standard-error convention.
The keyed evaluator now compares group/profile means and empirical distributions
on the same fixed rows, including a stronger joint conditional diagnostic and
conservative missing-action ranges. A permutation software control preserves
entire lower-order distributions and additive R2 while changing the interaction.
Its result and limits are in [docs/DISTRIBUTION_AUDIT_KO.md](docs/DISTRIBUTION_AUDIT_KO.md).

## Main scientific boundaries

- The released Study 1 contains 2,295 people and 9,180 profile judgments.
  Complete four-profile records are available for 2,003 people. Completeness
  differs by respondent income, so the primary target is explicitly restricted.
- The main comparison is a fixed-design allocation contrast. A causal AMCE
  interpretation requires assignment assumptions that the archive does not
  fully identify. Respondent income itself was not randomized.
- Original pair IDs, individual name assignments and survey language are absent.
  Reconstructed prompts are a disclosed operationalization, not exact UI replay.
- Study 2 contains no equivalent respondent demographic fields. Its general
  rebate versus crisis-relief comparison changes program descriptions together
  with context; it is not an isolated crisis treatment.
- Strictly separate human outcomes from model inputs and use fresh respondent
  contexts. Folder separation alone does not restrict a filesystem-enabled agent.

## Review workflow

[docs/review/WORKFLOW.md](docs/review/WORKFLOW.md) defines packet creation,
independent review exposure records, a severity-based issue ledger and revision
verification. Round one packets are under `reviews/round_01/`.
Two independent round01 reports judged **revise before main collection**.
Their issues, code fixes and open scientific conditions are recorded in
[reviews/round_01/response.md](reviews/round_01/response.md). Round02 is a
re-review, not a fresh context-blind review. The primary matched finite-cohort
evaluation has556 high/low respondents and36 design columns; it does not attach
ordinary bootstrap confidence intervals to the known human reference.
Both round02 reviewers retained that collection gate and identified response
alignment and arm-integrity gaps. The version4 fixes and remaining scientific
conditions are recorded in [reviews/round_02/response.md](reviews/round_02/response.md).
Keyed response replay now rejects contradictory or missing logs and is tested
under shuffled arrival, transport retries and malformed pairs. No live runner
or empirical model validation is implied by these checks.
Round06 limited re-review verifies the stronger distribution-preserving control
and public same-output adapter. Its interpretation constraints and unresolved
empirical/execution gates are retained in
[reviews/round_06/response.md](reviews/round_06/response.md).

The Korean project brief and next research gates are in
[docs/START_HERE_KO.md](docs/START_HERE_KO.md).
The [empirical-value memo](docs/EMPIRICAL_VALUE_PLAN_KO.md) adds an exploratory
human-source cohort-sensitivity audit. It leaves the locked main score unchanged
and narrows the interpretation of a human/model contrast sign change.

## GitHub status

This local repository is intended for `kunhailP/welfare-politics-lab`.
Remote creation and push require an authenticated connection to that account;
the currently connected GitHub account is different. No remote publication is
claimed. The publishing script validates the destination account before creating
or pushing a private repository.

## Source

Bridgman et al., *All in This Together? A Preregistered Report on Deservingness
of Government Aid During the COVID-19 Pandemic*,
[article](https://doi.org/10.1017/XPS.2021.10),
[replication data](https://doi.org/10.7910/DVN/LPHMB7).

The MIT license covers this repository's original software. It does not cover
third-party data, published texts, or the original replication code.
