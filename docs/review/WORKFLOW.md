# Independent review and revision workflow

Each round has a fixed, hashed anonymous packet and separate reviewer outputs.
Review A assesses theory, scientific novelty and interpretation. Review B assesses
estimands, selection, missingness, uncertainty and implementation. Both are
explicitly internal AI reviews, not external venue decisions or acceptance odds.

The user authorized two independent reviewers. They receive fresh conversation
contexts and are instructed to read only the packet and enclosed code, not this
repository's identity/README, prior plans or each other's report. This reduces
context contamination; it is not an access-control guarantee or perfect blinding.
Disclose any identity/history exposure the reviewers report.

## Per-round record

1. Freeze packet contents, hashes, allowed context and scope.
2. Obtain reviews independently before showing them to the author/revision step.
3. Record each issue with severity, evidence, scientific consequence, proposed
   fix and acceptance/verification criterion.
4. Respond accept/partially accept/disagree with evidence. A rebuttal is not a fix.
5. Version the protocol and code, run the relevant checks and link evidence.
6. Send the revised anonymous packet to a fresh review context for a second
   round. Specify whether it receives the first report (re-review) or not (fresh
   independent review). Do not claim both kinds of blindness simultaneously.
7. Retain unresolved issues and failed experiments; do not delete unfavorable
   findings or repeat reviews until they become positive.

The author may perform self-audits while waiting; label them as self-audits.
Scientific issues requiring raw model data remain open until those data exist.
An issue is resolved only when its verification criterion is met.
