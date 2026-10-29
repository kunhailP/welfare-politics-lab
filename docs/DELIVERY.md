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

No GitHub remote was created. The connector is authenticated as `kunhail`,
exposes no repository-creation operation, and has no accessible `kunhailP`
repository. The shell also lacks GitHub CLI/authentication. This is a tool/account
limitation, not a rejected approval request. No remote publication is claimed.

On the user's machine, with GitHub CLI authenticated as `kunhailP` and a clean
committed bundle clone, inspect the plan and publish a new private repository:

```bash
gh auth login
python scripts/publish_github.py
python scripts/publish_github.py --execute
```

The script checks the intended account, clean commit and tracked paths and
refuses to overwrite an existing destination. It creates the private repository
`kunhailP/welfare-politics-lab` and pushes the reviewed local source. Never put
a token in repository files or chat. No continued model calls or scheduled
research/reviews have been configured after handoff.
