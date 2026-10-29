# Response to round02 re-review — version4

Both reviewers judge the restricted finite-cohort protocol coherent and retain
**not ready for main collection**. This response does not overturn that decision.
Their own prior reports were visible; this was not a fresh blind round. The
round02 packet stays unchanged. Reviewer A's later environment addendum confirms
all31 enclosed tests passed with the documented pandas-enabled interpreter.

| Issue | Revision and verification | Remaining condition |
| --- | --- | --- |
| A11 / B10 arm integrity | `validated_agents` rejects income leakage into N/F-I, changed employment/parenthood, duplicate/missing agents and contradictory arm labels; plan records bind prompt content and identifiers. Corrupted-bundle fixtures pass. | Future native runner must transmit precisely the frozen plan and log actual sent content. Hashes alone do not authenticate a provider. |
| A11 / B11 response alignment | `recorded_responses` joins by request ID, verifies arm/person/profile mapping/rollout/prompt/model, checks every row in every arm, rejects duplicate/unaccounted/non-contiguous logs, handles only transport retries and retains whole invalid pairs. Shuffled arrival and reversed A/B mappings recover identical scores. Human/design/contrast hashes are included. | This is an offline adapter. A live isolated runner, reliable cost logging and resume behavior remain unverified. It cannot detect a dishonest logger attaching a valid reply to an incorrect request. |
| A12 repeated canonical names | No invented alternate name pool. All prompts explicitly distinguish the two hypothetical people even when names repeat. The actual frozen plan has143/1112 same-name pairs per arm,429/3336 requests. Same-cell fixture and collision metadata are implemented. | The handling is prospective and disclosed; model evidence from a frozen presentation audit is still required to assert robustness. |
| A13 common-task target | Version4 defines equal-base focal30k-minus120k contrasts and low-minus-high difference-in-differences; omitted-label comparisons are secondary. Focal position alternates by base and is fixed across cells. `common_task.py` retains missing cells with completion bounds; additive, interacting and incomplete fixtures pass. | No human target for counterfactual biographies. A live common-task log adapter, repeat/stability plan and actual diagnostic results remain open. |
| B6 joint support/leverage | Primary metadata now contains full-profile shared-pattern counts, income-by-employment support and contrast leverage by respondent group. | These are design diagnostics, not evidence of causal identification or real-model behavior. |
| B12 practical ambiguity/stability | Collection gate retained; no fabricated margin, expected-decoding CI or success classification. | Freeze model/settings, cost/resource tier, repeat and presentation plan; execute a pilot and report inconclusive/unstable results honestly. |
| B13 random-failure scenario | Renamed the single seeded scenario and added analytic uniform-subset expected width. | Neither quantity estimates real failure rates. Realized missing contrast weight remains necessary. |
| A1 / A3 / A4 / A10 novelty and validity | Narrow claims, comparison literature and reconstruction limits retained. | Software improvements cannot establish empirical novelty, human mechanisms, exact historical replay, publication readiness or competition strength. |

The first42 current implementation tests pass; current run receipts are generated
under ignored `runs/` directories. No new respondent model calls or paid
generation occurred. A targeted verification packet will distinguish its scope
from the two full review rounds; additional findings stay open instead of
repeating reviews until a favorable verdict appears.
