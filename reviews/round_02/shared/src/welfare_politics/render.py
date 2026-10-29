"""Whitelisted reconstructed survey requests and a deterministic interleaved plan.

This module never calls a model. Arm labels and source IDs are log metadata,
not messages. The future runner may transmit only the `messages` field.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random

ARMS = ['no_persona', 'socioeconomic_persona', 'socioeconomic_persona_without_income']
PROFILE_FIELDS = {'vignette_gender', 'vignette_ethnicity', 'vignette_health',
                  'vignette_citizen', 'vignette_marital', 'vignette_children',
                  'vignette_employment', 'vignette_income'}
FACT_TEXT = {
    'respondent_income': {
        'Low income': 'Household income: CAD 60,000 or less per year.',
        'Medium income': 'Household income: over CAD 60,000 and at most CAD 90,000 per year.',
        'High income': 'Household income: over CAD 90,000 per year.'},
    'respondent_employment': {
        'At risk/laid off': 'Employment category: classified as at risk of job loss or already laid off.',
        'Not at risk': 'Employment category: not classified in the at-risk or already-laid-off group.'},
    'respondent_children': {'Children': 'Children: has children.', 'No children': 'Children: has no children.'}}
NAME = {('Male', 'White'): 'Matthew Smith', ('Female', 'White'): 'Laurie Smith',
        ('Male', 'East Asian'): 'John Wong', ('Female', 'East Asian'): 'Julia Wong',
        ('Male', 'South Asian'): 'Amir Sandhu', ('Female', 'South Asian'): 'Anya Sandhu',
        ('Male', 'Indigenous'): 'Robert Blackhawk', ('Female', 'Indigenous'): 'Linda Blackhawk'}
CITIZENSHIP = {'Citizen born in Canada': 'was born in Canada and is a Canadian citizen',
               'Citizen not born in Canada': 'was born outside Canada and is a Canadian citizen',
               'Not a citizen': 'was born outside Canada and is not a Canadian citizen'}
CHILDREN = {'No children': 'have no children', 'Children under 5': 'have two children under age five',
            '5-12': 'have two children between ages five and twelve', 'Over 12': 'have two children over age twelve'}
EMPLOYMENT = {'Employed full-time': 'work full time with no loss of wages',
              'Employed, reduced income': 'work full time with reduced wages and hours',
              'Unemployed due to pandemic': 'are unemployed because of the pandemic',
              'Unemployed': 'are unemployed for reasons unrelated to the pandemic'}


def profile_text(attributes, white_names='english'):
    if set(attributes) != PROFILE_FIELDS or any(v is None for v in attributes.values()):
        raise ValueError('Only complete whitelisted recipient facts may be rendered')
    key = (attributes['vignette_gender'], attributes['vignette_ethnicity'])
    name = NAME[key]
    if white_names == 'french' and key[1] == 'White':
        name = 'Thomas Gagnon' if key[0] == 'Male' else 'Emma Gagnon'
    elif white_names not in ['english', 'french']:
        raise ValueError('Unknown name mapping')
    health = {'Healthy': 'are in good health',
              'Poor health': 'have a pre-existing condition that increases the risk of complications from COVID-19'}[attributes['vignette_health']]
    marital = {'Single': 'are single', 'Married': 'are married'}[attributes['vignette_marital']]
    return (f"{name} {CITIZENSHIP[attributes['vignette_citizen']]}. They live in a large Canadian city. "
            f"They {marital} and {CHILDREN[attributes['vignette_children']]}. "
            f"They {EMPLOYMENT[attributes['vignette_employment']]}. They {health}. "
            f"Their annual individual income before the pandemic was CAD {attributes['vignette_income'].lstrip('$')}.")


def messages(facts, pair, white_names='english'):
    if not set(facts) <= set(FACT_TEXT) or len(pair) != 2:
        raise ValueError('Only declared respondent facts and two profiles may be used')
    lines = [FACT_TEXT[key][facts[key]] for key in FACT_TEXT if key in facts]
    persona = '\n'.join(lines)
    intro = ('Consider this Canadian allocation survey in its described 2020 setting. '
             'Choose the monthly government support each person should receive during the pandemic. '
             'Each amount is independent and can be from CAD 0 to CAD 4,000. '
             'There is no shared budget between the two people.')
    text = ((persona + '\n\n') if persona else '') + intro
    text += '\n\nPerson A: ' + profile_text(pair[0], white_names)
    text += '\n\nPerson B: ' + profile_text(pair[1], white_names)
    return [{'role': 'system', 'content': 'Respond as a survey participant. Return only a JSON object with keys A and B, each an integer from 0 through 4000. Do not add explanations.'},
            {'role': 'user', 'content': text}]


def parse_pair(raw):
    def no_duplicates(pairs):
        out = {}
        for key, value in pairs:
            if key in out: raise ValueError('Duplicate response key')
            out[key] = value
        return out
    try:
        value = json.loads(raw, object_pairs_hook=no_duplicates)
        if not isinstance(value, dict) or set(value) != {'A', 'B'}:
            raise ValueError('Exactly A and B required')
        if any(type(v) is not int or not 0 <= v <= 4000 for v in value.values()):
            raise ValueError('Integer actions 0 through 4000 required')
        return {'status': 'valid', 'amounts': value, 'error': None}
    except (ValueError, TypeError) as exc:
        return {'status': 'invalid', 'amounts': None, 'error': str(exc)}


def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line]


def plan(input_root, phase='confirmatory', seed=20261029, primary_only=True,
         pairing=((1, 2), (3, 4)), white_names='english'):
    root = Path(input_root)
    agents = {arm: {a['agent_id']: a for a in load_jsonl(root / arm / 'agents.jsonl') if a['phase'] == phase} for arm in ARMS}
    ids = sorted(agents[ARMS[0]])
    if any(set(agents[a]) != set(ids) for a in ARMS): raise ValueError('Arm populations differ')
    if primary_only:
        ids = [i for i in ids if agents['socioeconomic_persona'][i]['observed_socioeconomic_facts'].get('respondent_income') in ['High income', 'Low income']]
    profiles = {}
    for row in load_jsonl(root / 'recipient_profiles.jsonl'):
        key = (row['agent_id'], row['task_number'])
        if key in profiles: raise ValueError('Duplicate profile key')
        profiles[key] = row['recipient_attributes']
    if sorted(j for pair in pairing for j in pair) != [1, 2, 3, 4] or any(len(pair) != 2 for pair in pairing):
        raise ValueError('Pairing must partition the four profiles')
    blocks = [(i, pair) for i in ids for pair in pairing]
    rng = random.Random(seed); rng.shuffle(blocks)
    output = []
    for agent, numbers in blocks:
        pair = [profiles[(agent, number)] for number in numbers]
        order = ARMS.copy(); rng.shuffle(order)
        for arm in order:
            request = messages(agents[arm][agent]['observed_socioeconomic_facts'], pair, white_names)
            digest = hashlib.sha256(json.dumps(request, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
            output.append({'agent_id': agent, 'arm': arm, 'profile_numbers': list(numbers),
                           'messages': request, 'messages_sha256': digest,
                           'status': 'planned_only_no_model_response'})
    return output


def common_task_plan(input_root, bases=16, seed=20261029):
    """Cross income labels and focal income on exactly shared model-only tasks.

    Counterfactual labels are not observed biographies. No human outcomes exist
    for these new crossed tasks; this diagnoses model information sensitivity.
    """
    root = Path(input_root)
    agents = [a for a in load_jsonl(root / 'socioeconomic_persona/agents.jsonl') if a['phase'] == 'pilot']
    profiles = {(r['agent_id'], r['task_number']): r['recipient_attributes'] for r in load_jsonl(root / 'recipient_profiles.jsonl')}
    contexts = [(a, pair) for a in agents for pair in [(1, 2), (3, 4)]]
    rng = random.Random(seed); rng.shuffle(contexts)
    output = []
    for number, (agent, pair_numbers) in enumerate(contexts[:bases]):
        facts = {k: v for k, v in agent['observed_socioeconomic_facts'].items() if k != 'respondent_income'}
        for label in ['High income', 'Low income', 'omitted']:
            respondent = dict(facts)
            if label != 'omitted': respondent['respondent_income'] = label
            for income in ['$30,000', '$120,000']:
                pair = [{**profiles[(agent['agent_id'], pair_numbers[0])], 'vignette_income': income},
                        dict(profiles[(agent['agent_id'], pair_numbers[1])])]
                rendered = messages(respondent, pair)
                output.append({'audit_base': number, 'income_label': label, 'focal_income': income,
                               'messages': rendered,
                               'interpretation': 'counterfactual model-input audit; no matched human outcome'})
    rng.shuffle(output)
    return output


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--inputs', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--phase', choices=['pilot', 'confirmatory'], default='confirmatory')
    p.add_argument('--all-income-groups', action='store_true')
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    rows = plan(args.inputs, args.phase, primary_only=not args.all_income_groups)
    with (args.output / 'requests.jsonl').open('w') as f:
        for row in rows: f.write(json.dumps(row, ensure_ascii=False) + '\n')
    common = common_task_plan(args.inputs)
    with (args.output / 'common_task_audit_requests.jsonl').open('w') as f:
        for row in common: f.write(json.dumps(row, ensure_ascii=False) + '\n')
    receipt = {'status': 'request_plan_only', 'actual_model_calls': 0,
               'planned_requests': len(rows), 'unique_transmitted_inputs': len({r['messages_sha256'] for r in rows}),
               'common_task_model_only_audit_requests': len(common),
               'source': 'whitelisted input bundle only; no human-reference files read',
               'response_policy': 'invalidate entire pair if JSON or either action is invalid',
               'native_socioverse_runner_implemented': False}
    (args.output / 'receipt.json').write_text(json.dumps(receipt, indent=2))
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
