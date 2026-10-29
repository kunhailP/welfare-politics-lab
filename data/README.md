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

On 2026-10-29 the official dataset API reported CC0 1.0 for the released dataset.
[The metadata receipt](DATASET_LICENSE_RECEIPT.json) records its version, license,
seven file IDs/checksums and download links. This is the dataset's license;
the journal article/PDF and this project's MIT software license have separate scopes.

The four non-tabular source files match the API's MD5 checksums. The three `.tab`
files do not match those MD5 values. Dataverse normalizes ingested tables and
retains an original-file checksum; see its [tabular-data guide](https://guides.dataverse.org/en/6.12.1/user/tabulardataingest/ingestprocess.html).
Fresh source-file requests in this environment returned HTTP403, so a bytewise
comparison against a new live TAB download was not completed. Do not describe
this as seven new downloads verified against metadata. The supplied archive
and all seven local source SHA256 values remain verified against the pinned
source manifest. Later licensing verification does not rewrite earlier receipts.

Original archives, individual response tables, PDFs and derived human-level
responses remain excluded from public Git. Keep the evaluation workspace separate
from the generation-only export and retain source attribution in downstream use.
