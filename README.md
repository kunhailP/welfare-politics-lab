# Welfare Politics Lab

Human-grounded evaluation of income-group-conditioned welfare allocations.
How closely do generated responses reproduce both groups' recipient-income
comparisons, and how does adding socioeconomic facts change their errors?

**Start here: [한국어 인계 안내](docs/USER_HANDOFF_KO.md).**

[공개 내용 점검](docs/REPOSITORY_AUDIT_KO.md) ·
[대회 실행 순서: 웹 플랫폼 제공 크레딧](docs/COMPETITION_EXECUTION_KO.md)

## Included

- Verified local source ingestion and descriptive human reanalysis.
- Fixed main design:556 high/low respondents,2224 judgments,3336 primary requests.
- Separate96-request model-only common-task plan.
- Keyed response evaluation, both group components, missing-action bounds and
  same-output mean/distribution diagnostics.
- Three fixed human-trained references using877 disjoint people.
- Tests, source sensitivity, fresh blind review records and reproduction receipts.
- A sealed generation-only ZIP exporter, primary/common-task keyed log replay,
  and explicit platform-credit accounting without guessed USD conversion.

**Actual respondent-model calls:0. Paid generation:0.** This is an offline
research/evaluation repository. Native SocioVerse execution, live audit adapters,
model/settings and campaign cap remain unfinished. See [remaining work](docs/NEXT_STEPS_KO.md).
Statistical predictions and software controls are not model responses. A new
empirical contribution remains to be demonstrated with actual results.

To prepare data and the input-only ZIP for the owner's chosen web-platform
execution, see [플랫폼 준비 안내](docs/PLATFORM_PREPARATION_KO.md). Model/settings
selection belongs to the owner. Exporting inputs does not start generation.

## Reproduce

Python3.12 is the tested environment. Installation requires internet; reproduction
itself has no network or model-call path. Obtain the original archive separately.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-tested.txt
python -m pip install -e . --no-deps
python scripts/reproduce_handoff.py \
  --archive /absolute/path/to/dataverse.zip \
  --output runs/my_first_check
```

Use a new output directory every time. The wrapper ingests source, reproduces
core analysis, source sensitivity and statistical references, then runs tests
and writes `handoff_receipt.json`. Tests also run without original data:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Research and execution map

| Document | Purpose |
| --- | --- |
| [Claim/table specification](docs/EMPIRICAL_CLAIM_SPEC_V1.md) | Fixed primary/secondary interpretations |
| [Current protocol](docs/CURRENT_PROTOCOL.md) | Source, design, estimands and failure policy |
| [Source scope](docs/SOURCE_SCOPE_KO.md) | Selection flow, income-specific retention and human contrasts |
| [Stimulus crosswalk](docs/STIMULUS_CROSSWALK.md) | Original instrument and reconstruction limits |
| [Reference results](docs/STATISTICAL_REFERENCE_RESULTS_KO.md) | Human-trained calculations and limits |
| [Response log contract](docs/RESPONSE_LOG_FORMAT.md) | Future actual primary logs and frozen-input check |
| [Final blind review response](reviews/final_09/response.md) | Two fresh-context reviews, revisions and open issues |
| [Final validation](docs/FINAL_HANDOFF_VALIDATION.json) | Local checks and reproduction evidence |
| [Delivery/publication](docs/DELIVERY.md) | Public repository and original handoff archives |

The target is a fixed selected cohort and reconstructed tasks, not a national
population. Household-income bands operationalize the group comparison; they do
not measure class identity, assets or occupation. Respondent income was not
randomized. The primary F-versus-N comparison adds income/job-risk/parenthood
together; explicit-income F-versus-F-I is secondary. No human-income causal,
psychological-mechanism or actual-voting inference follows from these contrasts.

## Data, license and GitHub

Source: Bridgman et al., *All in This Together? A Preregistered Report on
Deservingness of Government Aid During the COVID-19 Pandemic*,
[article](https://doi.org/10.1017/XPS.2021.10),
[replication data](https://doi.org/10.7910/DVN/LPHMB7).
Read [data provenance](data/README.md). Raw data, individual outputs, PDFs,
credentials and generated runs are excluded from Git and delivery. The MIT
license covers original software, not third-party data or published text.

Public repository: [kunhailP/welfare-politics-lab](https://github.com/kunhailP/welfare-politics-lab).
Maintainer: [Kun woo Park (@kunhailP)](https://github.com/kunhailP).
Research design, implementation and internal reviews used AI assistance.
[Publication provenance](docs/PUBLICATION.md) preserves the mapping from the
reviewed local history to the owner-attributed public commits.
