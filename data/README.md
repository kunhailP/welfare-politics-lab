# Source data

The user supplied `dataverse.zip` from DOI `10.7910/DVN/LPHMB7` on 2026-10-29.
Archive SHA256:
`06e74a2df4c0e9b7382ffcacc6d1844cae0b450c07a165b8046620f52c3b8625`.

Seven expected files: study1.tab, study2.tab, study2_alt.tab, main.Rmd,
README.md, renv.lock, deservingness.Rproj. Dataverse supplied tab-separated
files; the original Rmd expects CSV. Our reader explicitly uses TAB parsing.
The distributed README's venue label differs from the publisher record; cite
the publisher article DOI rather than infer a new source from that label.

`raw/` is ignored by Git. The original Rmd is read as source documentation and
is never executed by the offline pipeline. The source hash manifest is tracked
under `docs/source_manifest.json`; file hashes are verified during ingestion.

The current session has not independently retrieved authoritative dataset
licensing metadata. Redistribution is therefore unverified, rather than assumed
to be covered by our code license. Download the original files from the cited
source. Do not commit the uploaded archive, individual response tables, original
PDFs, or derived human-level responses to a public repository by default.
