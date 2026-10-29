# Delivery and publication

The handoff ZIP contains committed tracked files only. The Git bundle preserves
the local history. Neither includes raw data, generated runs, private reviewer
source supplements, credentials or actual model responses.

```bash
git clone welfare-politics-lab-handoff.bundle welfare-politics-lab
cd welfare-politics-lab
```

Follow [USER_HANDOFF_KO.md](USER_HANDOFF_KO.md) to install and reproduce from the
separate original archive. The ZIP has no Git history; use the bundle to retain
it. The external handoff manifest records the exact commit, archive sizes and
SHA256 hashes. [FINAL_HANDOFF_VALIDATION.json](FINAL_HANDOFF_VALIDATION.json)
records local checks. Historical receipts remain preserved.

The owner subsequently authorized public publication to
[kunhailP/welfare-politics-lab](https://github.com/kunhailP/welfare-politics-lab).
Start further work from its public history:

```bash
git clone https://github.com/kunhailP/welfare-politics-lab.git
cd welfare-politics-lab
```

The original ZIP, bundle, manifest and validation receipts remain historical
artifacts of the pre-publication reviewed history. At the owner's request, the
public copy associates all commit authors and committers with the owner. Its
reviewed source trees were preserved exactly before publication documentation
updates. See [publication provenance](PUBLICATION.md) for the commit mapping,
checks and AI-assistance disclosure. Do not force-push the old bundle history
over the public branch.

The existing `scripts/publish_github.py` remains a helper for a different, new
private destination; it is not needed for this published repository. No
continued model calls or scheduled research/reviews were configured after handoff.
