# Round06 response and author verification

Both reviewers retained prior own-review context; this was not a fresh blinded
review or external peer review. Both verified57 snapshot tests. Reviewer B also
checked400 controls,3750 completion cases and1250 unequal-cell cases, plus a
public keyed-path fixture. Their source-data counts/effects remain author-
reported: neither had raw data or real generator outputs.

| Issue | Disposition | Evidence and remaining condition |
| --- | --- | --- |
| A14: prior oracle changed marginal distributions | Addressed for specified objects | New permutations preserve whole overall/group/profile multisets and additive projection/R2; no general theorem or benchmark-wide result claimed. |
| Comparator omission | Addressed | The stronger group-by-profile check is included and detects changed controls. The target contrast is not uniquely capable of detection. |
| Same-output integration | Addressed offline | Public keyed evaluation attaches all diagnostics; invalid whole pairs keep original rows/cells and suppress R2. Live delivery/isolation remains open. |
| A17: singleton/population interpretation | Accepted | Current code reports cell-size histogram and singleton row fraction. Source1418/2224 singleton rows are about64%; fine partition distances can rise mechanically. These are finite sample comparisons, not population distributions or individual preference truth. |
| A18: real diagnostic consequence and novelty | Open | No real model output; oracle is software validation only. Actual N/F/F-I comparisons, diagnostics and their limits are still required. |
| B17: candidate enumeration scalability | Bounded scope retained | Greedy candidate storage is not certified for arbitrary large duplicate cells. No scalable optimizer claim is made; no broader matching algorithm is added merely for this example. |

After review, the author added cell-size/fraction reporting and a hand-calculated
1/3/2/5-cell regression, extended missing-completion tests to verify partition
refinement on complete outcomes, and made public-path checks explicit. Current
tests total58 and pass; the immutable reviewer packet remains its57-test version.
These minor author revisions are not described as another blind review.

This closes the specific distribution-change/weak-comparator/adapter weaknesses,
not the project's empirical contribution or collection gates. Further oracle
variants are not the next priority. Complete native isolation/logging and the
fixed model/settings/cost manifest before any respondent generation.
