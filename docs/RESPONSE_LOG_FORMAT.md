# Primary response log contract

The current public scorer handles the frozen primary rollout0. The live runner
is not included. It must save one JSON object per attempt per line, with arrival
order independent of row order.

Copy six fields verbatim from each planned request: `request_id`, `agent_id`,
`arm`, `profile_numbers`, `rollout`, `messages_sha256`. A/B map to the first/second
entry in `profile_numbers`. Allowed arms are `no_persona`,
`socioeconomic_persona`, `socioeconomic_persona_without_income`.

| Additional field | Required value |
| --- | --- |
| `attempt` | Contiguous integer1,2 or3 per request |
| `status` | `reply` or `transport_error` |
| `raw_reply` | Original text for reply; null for transport error |
| `returned_model_id` | Exact frozen returned ID for reply; null allowed for transport error |
| `cost_usd` | Finite nonnegative per-attempt cost, including failures |

Illustration only, **not an actual response**:

```json
{
  "request_id": "COPY_FROM_PLANNED_REQUEST",
  "agent_id": "COPY_FROM_PLANNED_REQUEST",
  "arm": "socioeconomic_persona",
  "profile_numbers": [1, 2],
  "rollout": 0,
  "messages_sha256": "COPY_FROM_PLANNED_REQUEST",
  "attempt": 1,
  "status": "reply",
  "raw_reply": "{\"A\":1000,\"B\":1500}",
  "returned_model_id": "EXACT_FROZEN_RETURNED_ID",
  "cost_usd": 0.001
}
```

Keep provider token/usage/credit records alongside the log. Do not invent costs
or silently replace unknown cost with0. The scorer requires resolved accounting.

Only transport errors retry. A reply ends the request even if invalid/refused;
that reply leaves both actions unknown. Three transport errors exhaust retries.
Every planned request needs an explicit final history. No cleaned/substituted
response is used. Strict replies contain exactly A/B integer0–4000; booleans,
decimals, duplicate keys, fences and explanations are invalid. Deep JSON decoder
recursion errors invalidate the pair rather than aborting the full evaluation.

## Pre-generation input binding

The scorer CLI also requires `--frozen-receipt` and
`--expected-receipt-sha256`. Use `core/receipt.json` from the offline reproduction
and record its SHA256 separately before generation, for example in a committed
campaign record. The scorer checks both design-file and request-file hashes
against that receipt. Rehashing an altered request alone does not pass.

```bash
python -c "import hashlib,pathlib; print(hashlib.sha256(pathlib.Path('runs/my_first_check/core/receipt.json').read_bytes()).hexdigest())"
```

This receipt binds files only. It does not bind the future provider/model
settings, budget, execution version or variant/rollout adapters as one complete
live campaign. Freeze those separately in the actual runner before execution;
that integration remains unfinished. No hash proves provider authenticity or
that the declared messages were actually transmitted. Preserve provider receipts.

The programmatic evaluator checks internal consistency and is also used by
explicit software controls. It does not automatically authenticate a caller's
frozen campaign. Actual-file CLI evaluation adds the external receipt check.
Arbitrary rollouts, variants and common-task records are not accepted by this
primary scorer; do not relabel repeated outputs as rollout0 to bypass that limit.
