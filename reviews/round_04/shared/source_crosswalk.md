# Study1 source-to-prompt crosswalk — version5

Checked on2026-10-29 against the [published article](https://doi.org/10.1017/XPS.2021.10),
its Table2 instrument and the final supplement, TablesA1 andA5:
[published supplement](https://static.cambridge.org/content/id/urn%3Acambridge.org%3Aid%3Aarticle%3AS2052263021000105/resource/name/S2052263021000105sup001.pdf).
The earlier preregistration/power document is not a substitute for the published
factorial levels. This is an author source audit, not independent certification.

| Input | Source meaning and render rule | Remaining limitation |
| --- | --- | --- |
| Respondent income | TableA1: household-income bands up to60k, above60k through90k, above90k. Article discussion confirms the high band above90k. | The supplement has an apparent high-band typographical error; do not interpret it as900,001. The released categories omit exact income. |
| Respondent employment | TableA1's binary positive category combines reported job risk and already-laid-off status. Renderer describes the category, not a complete employment biography. | The negative category is not proof of secure full-time employment; the original question has an intermediate uncertainty response. |
| Respondent parenthood | TableA1 collapses any positive number of children versus none. | Do not invent ages or exact counts for respondents. |
| Recipient name | TableA5 has gender/ethnicity-associated name pools. Released gender and ethnicity determine a canonical mapping. | Original name draw and language absent. White English/French mapping and repeated-name disambiguation are prospective adaptations. |
| Citizenship | Three released levels distinguish born citizen, naturalized/foreign-born citizen, and foreign-born noncitizen. | Do not infer residency duration or legal eligibility. |
| Marital status | Single or married. | No additional relationship or household facts. |
| Recipient children | No children, or two children in one of three age bands: below5,5–12,above12. | These counts apply to recipient profiles, not respondent parenthood. |
| Recipient employment | Full-time/no wage loss; full-time with reduced wages/hours; unemployed because of the pandemic; unemployed for unrelated reasons. | Do not collapse the last two categories or equate reduced hours with complete job loss. |
| Recipient health | Healthy versus a pre-existing condition increasing COVID complication risk. | Study2 generic health wording is not substituted. This field does not identify a specific diagnosis. |
| Recipient income | Table2 describes income before the pandemic; TableA5 provides30k/60k/90k/120k. Version5 follows that wording. | **Annual period and explicit individual-versus-household language are not stated in the printed recipient instrument.** Version4's extra expansion was removed before any model generation. |
| Residence/context | Table2 places the hypothetical recipient in a large Canadian city; fieldwork was May2020. | Renderer uses a historical2020 context; no current-event facts or exact city are invented. |
| Outcome | Table2 asks monthly government support per recipient, using a0–4000 slider defaulting to zero. | JSON integer output and explicit independent amounts adapt the interface. Original slider behavior is not replayed. |
| Pairing | Original design has two pairs per respondent. | Released pair/name/language assignments are absent.1/2 and3/4 reconstruction is an assumption. |

## Provenance limits retained

The article reports2522 recruited Study1 respondents; the released table has2295.
The full recruitment-to-release exclusion mapping is not reconstructed here.
Within the released archive,2003 people have four complete recipient profiles;
selection differs by respondent income. The primary target stays the fixed
selected high/low cohort, not the recruitment population or Canada generally.

The article describes equally likely unconstrained profile permutations, whereas
released citizenship/employment margins are notably uneven. This discrepancy
requires provenance clarification and does not by itself establish that the
original experiment was invalid. We do not assume known assignment probabilities
or label the new fixed-design coefficient a causal AMCE.

## What is and is not closed

This crosswalk checks published semantics and corrects a documented wording
expansion. It cannot recover missing pair IDs, source names, language or the
original UI. A predeclared and executed presentation audit remains required
for robustness claims. The current generator remains disabled.
