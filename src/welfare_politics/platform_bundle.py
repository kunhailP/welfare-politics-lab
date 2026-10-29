"""Offline export of frozen generation-only requests; never executes a model."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from .common_task_responses import validate_plan as validate_common
from .render import ARMS, load_jsonl, message_digest, request_identity

PRIMARY_KEYS = {'agent_id', 'arm', 'profile_numbers', 'rollout', 'messages',
                'messages_sha256', 'same_canonical_name', 'status', 'request_id'}
COMMON_KEYS = {'audit_base', 'income_label', 'focal_income', 'focal_position',
               'messages_sha256', 'messages', 'interpretation'}


def validate_messages(messages):
    if not isinstance(messages, list) or len(messages) != 2:
        raise ValueError('Only the fixed fresh-context system/user messages may be exported')
    for message, role in zip(messages, ('system', 'user')):
        if set(message) != {'role', 'content'} or message['role'] != role or not isinstance(message['content'], str):
            raise ValueError('Unexpected message fields or roles')


def validate_primary(requests):
    seen, by_arm = set(), {arm: set() for arm in ARMS}
    for request in requests:
        if set(request) != PRIMARY_KEYS:
            raise ValueError('Unexpected primary request field; no extra outcome/annotation fields allowed')
        validate_messages(request['messages'])
        if request['arm'] not in ARMS or type(request['rollout']) is not int or request['rollout'] != 0:
            raise ValueError('Unexpected arm or rollout')
        numbers = request['profile_numbers']
        if (not isinstance(numbers, list) or len(numbers) != 2 or len(set(numbers)) != 2
                or any(type(n) is not int or n not in (1, 2, 3, 4) for n in numbers)):
            raise ValueError('Invalid A/B profile mapping')
        if (message_digest(request['messages']) != request['messages_sha256']
                or request_identity(request) != request['request_id'] or request['request_id'] in seen):
            raise ValueError('Request identity/hash changed or duplicated')
        if request['status'] != 'planned_only_no_model_response' or type(request['same_canonical_name']) is not bool:
            raise ValueError('Unexpected plan status or name metadata')
        rows = {(request['agent_id'], number) for number in numbers}
        arm = request['arm']
        if by_arm[arm] & rows:
            raise ValueError('Duplicate design row in an arm')
        by_arm[arm].update(rows)
        seen.add(request['request_id'])
    if not seen or any(rows != by_arm[ARMS[0]] for rows in by_arm.values()):
        raise ValueError('All three arms must contain the same nonempty design rows')
    for agent, _ in by_arm[ARMS[0]]:
        if {(agent, n) for n in (1, 2, 3, 4)} - by_arm[ARMS[0]]:
            raise ValueError('Incomplete participant profile set')


INSTRUCTIONS = '''# Input-only package for the SocioVerse web research workspace

This export does not run or import a native study. It contains planned tasks,
not model outputs. Supply only each record's messages to the respondent model
in a fresh context. Keep all other fields solely as linkage metadata. Do not
send the manifest, this README, human results, reviewer files, arm labels or
earlier answers to the respondent model. Persistent per-person conversation
memory would change this protocol and must not be introduced.

primary_requests.jsonl retains the frozen primary plan bytes. Its attempt log
copies request_id, agent_id, arm, profile_numbers, rollout and messages_sha256.
common_task_requests.jsonl adds a stable audit_request_id; its attempt log
copies audit_request_id, audit_base, income_label, focal_income,
focal_position and messages_sha256. Never mix the two log schemas.

Each attempt also records attempt (1..3), status (reply or transport_error),
raw_reply (original text or null for transport error), returned_model_id,
and observed per-attempt accounting. Use either cost_usd OR cost_value plus
cost_unit (USD, SocioVerse_Agent or SocioVerse_Sim). These are log-contract
unit names, not a claim about the platform's API field names. Keep actual
platform billing records. Unknown cost is not zero; no credit/USD conversion
is inferred. Calls paid by provided credits still consume resources.

Only transport failures retry, at most twice. A reply ends the request even
if malformed/refused, and an invalid A/B pair remains wholly unknown. Never
repair, clamp, fallback to a rule, silently rerun or omit unsuccessful tasks.
Save every attempt. Preserve raw export and identify any conversion script.

The owner selects model/settings and available-credit cap. Freeze those plus
this manifest's separately recorded SHA256 before actual collection. The
campaign template is deliberately incomplete and cannot authorize execution.
The full research/evaluation repository and original data stay outside the
respondent-generation workspace. File selection alone is not OS isolation.
This package requires a platform-specific import/call/export integration;
web deployment has not been tested from this environment.
'''


def export_bundle(core, output, expected_receipt_sha256, zip_path=None):
    core, output = Path(core), Path(output)
    raw_receipt = (core / 'receipt.json').read_bytes()
    receipt_hash = hashlib.sha256(raw_receipt).hexdigest()
    if receipt_hash != expected_receipt_sha256:
        raise ValueError('Core receipt differs from its external seal')
    receipt = json.loads(raw_receipt)
    if receipt.get('status') != 'offline_reproduction_complete':
        raise ValueError('A completed core reproduction receipt is required')
    primary_path = core / 'planned_primary_requests/requests.jsonl'
    common_path = core / 'planned_primary_requests/common_task_audit_requests.jsonl'
    for path in (primary_path, common_path):
        key = str(path.relative_to(core))
        if receipt.get('artifacts_sha256', {}).get(key) != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError('Plan differs from frozen core receipt: ' + key)
    primary, common = load_jsonl(primary_path), load_jsonl(common_path)
    validate_primary(primary)
    for request in common:
        if set(request) != COMMON_KEYS:
            raise ValueError('Unexpected common-task annotation/outcome field')
        validate_messages(request['messages'])
    keyed_common = validate_common(common, bases=16)
    if output.exists() or output.is_symlink() or (zip_path is not None and Path(zip_path).exists()):
        raise FileExistsError('Use new output and ZIP paths; existing artifacts are not overwritten')
    campaign = {'status': 'owner_settings_required', 'generation_enabled': False,
        'model': None, 'expected_returned_model_id': None, 'decoding': None,
        'credit_cap': None, 'credit_unit': None, 'execution_version': None,
        'additional_external_api_budget_usd': 0,
        'core_receipt_sha256': receipt_hash,
        'requires_before_execution': ['platform input/export integration', 'generation isolation',
            'repeat and presentation allocation', 'fixed model/settings/resource cap']}
    files = {'primary_requests.jsonl': primary_path.read_bytes(),
        'common_task_requests.jsonl': ''.join(json.dumps(row, ensure_ascii=False)+'\n'
            for row in keyed_common.values()).encode(),
        'campaign.template.json': (json.dumps(campaign, indent=2)+'\n').encode(),
        'README.txt': INSTRUCTIONS.encode()}
    manifest = {'kind': 'generation_only_frozen_input_export', 'actual_model_calls': 0,
        'native_study_import_verified': False, 'isolation_enforced_by_exporter': False,
        'core_receipt_sha256': receipt_hash, 'primary_requests': len(primary),
        'common_task_requests': len(common), 'human_outcomes_included': False,
        'primary_plan_bytes_preserved': True,
        'files_sha256': {name: hashlib.sha256(raw).hexdigest() for name, raw in files.items()}}
    files['manifest.json'] = (json.dumps(manifest, indent=2)+'\n').encode()
    output.mkdir(parents=True, exist_ok=False)
    for name, raw in files.items():
        (output / name).write_bytes(raw)
    if zip_path is not None:
        with zipfile.ZipFile(zip_path, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, raw in files.items():
                archive.writestr(name, raw)
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--core', type=Path, required=True)
    p.add_argument('--expected-receipt-sha256', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--zip', dest='zip_path', type=Path)
    args = p.parse_args()
    result = export_bundle(args.core, args.output, args.expected_receipt_sha256, args.zip_path)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
