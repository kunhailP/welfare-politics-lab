# Research and implementation instructions

- Read README.md and docs/CURRENT_PROTOCOL.md before making changes.
- Keep raw data and published reference code immutable. Preserve source hashes.
- Original third-party data and PDFs remain outside Git until redistribution
  rights have been verified. The code license does not license external data.
- Keep human reanalysis, synthetic software checks, and real model outputs
  separately labelled. Current real model calls are zero.
- Do not send reference outcomes, paper results, previous model answers from a
  different arm, or author/reviewer discussions to respondent models.
- Do not run paid generation without an established campaign model and budget.
  The offline pipeline must have no network/model-call path.
- Compare human and model contrasts directly; separate observational group
  differences from interventions on model inputs. Do not assume released
  profile assignment probabilities are uniform or known.
- Complete-profile selection is income-dependent. Limit the estimand or
  explicitly address selection; do not claim a representative population.
- Version protocol changes before generation. Never tune on confirmation
  outputs and keep the same study title while changing the measured target.
- Review packets contain no author identity, repository URL, career goals,
  prize aspirations, desired conclusions, or previous reviews. Record review
  context exposure and access limitations. A self-audit is not a blind review.
- An internal AI review is not external peer review or evidence of acceptance.
- Do not overwrite run directories. Use fresh output paths and report failures.
- Run meaningful numerical, data-isolation and archive-integrity checks after
  relevant changes. Use `PYTHONPATH=src python -m unittest discover -s tests`.
- Competition remains the objective; strong workshop-paper rigor, originality
  and depth are the user's quality standard. Do not reinterpret this as waiting
  for a journal decision or abandoning the current competition.
- Generation, including the engineering pilot, stays on development hold while
  contribution and collection gates are incomplete. Positive AI reviews or more
  tests alone do not satisfy those gates; model/settings and cost cap are needed.
- Distinguish rank of the full coefficient design from estimability of one
  contrast. A full-rank-only evaluator's rejection does not prove that every
  contrast is unidentified. Preserve numerical diagnostics and their tolerance.
