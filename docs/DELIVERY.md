# Delivery and publication

The source ZIP contains tracked files only; raw data, generated runs and
credentials are excluded. The Git bundle preserves the local commit history.
Clone the bundle to retain that history:

```bash
git clone welfare-politics-lab.bundle welfare-politics-lab
cd welfare-politics-lab
```

Follow the README to ingest a separately acquired source archive and reproduce
the offline analysis. `docs/VALIDATION.json` records the checks already run.
Neither source ZIP nor bundle contains empirical respondent-model results.

No GitHub remote was created. In an environment with GitHub CLI authenticated
as `kunhailP`, inspect the plan, then create/push the reviewed private repository:

```bash
python scripts/publish_github.py
python scripts/publish_github.py --execute
```

The current connector is authenticated as `kunhail`, a different account, and
does not expose repository creation. No token should be placed in repository
files or chat. Publishing is pending authentication; source preparation and
local commits are complete. The script refuses to overwrite an existing repo.
