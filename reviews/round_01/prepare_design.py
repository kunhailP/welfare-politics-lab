"""Prepare reproducible cohorts and outcome-free model inputs, without model calls.

Generation inputs contain only observed factual attributes. Evaluation data and
linkage are stored outside that directory. The future model runner must use a
fresh isolated context and load only its whitelisted input; folder separation
alone is not a security boundary for a filesystem-enabled agent.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .study1_interest_audit import LEVELS

SEED = 20261029
PERSONA = ['respondent_income', 'respondent_employment', 'respondent_children']
RECIPIENT = list(LEVELS)
FORBIDDEN = {'vignette_allocation', 'vignette_deservingness', 'vignette_similarity',
             'get_ahead', 'inequality', 'living', 'gov_cerb', 'gov_cews', 'gov_cesb',
             'gov_tax', 'gov_ccb', 'gov_ei', 'gov_support', 'allocation_normalized'}


def json_value(v):
    return None if pd.isna(v) else v.item() if isinstance(v, np.generic) else v


def write_jsonl(path, rows):
    with path.open('w') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('data/raw'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.source
    args.output.mkdir(parents=True, exist_ok=False)
    inputs = args.output / 'generation_inputs'
    reference = args.output / 'evaluation_reference'
    inputs.mkdir(); reference.mkdir()
    s1 = pd.read_csv(root / 'study1.tab', sep='\t')
    s2 = pd.read_csv(root / 'study2.tab', sep='\t')
    rng = np.random.default_rng(SEED)
    for d in [s1, s2]:
        assert not d.duplicated(['id', 'vignette_num']).any()
        assert d.groupby('id').size().eq(4).all()
    complete = s1[RECIPIENT].notna().all(axis=1).groupby(s1.id).all()
    eligible = np.array(sorted(complete[complete].index), dtype=int)
    order = rng.permutation(eligible)
    pilot, confirm = order[:32], order[32:800]
    assert len(confirm) == 768 and not set(pilot) & set(confirm)
    assert len(s1[s1.id.isin(eligible)]) == 4 * len(eligible)
    assignments = []
    for phase, ids in [('pilot', pilot), ('confirmatory', confirm)]:
        assignments.extend({'study': 'study1', 'source_id': int(i), 'agent_id': f's1:{i}',
                            'phase': phase} for i in ids)
    # Use original assigned frames. Do not invent respondent demographics in Study 2.
    for frame in ['COVID-19', 'GST']:
        ids = np.array(sorted(s2.loc[s2.condition == frame, 'id'].unique()), dtype=int)
        selected = rng.permutation(ids)[:128]
        assignments.extend({'study': 'study2', 'source_id': int(i), 'agent_id': f's2:{i}',
                            'phase': 'context_validation'} for i in selected)
    agents, profiles = [], []
    for a in assignments:
        d = s1 if a['study'] == 'study1' else s2
        rows = d.loc[d.id == a['source_id']].sort_values('vignette_num')
        first = rows.iloc[0]
        facts = {c: json_value(first[c]) for c in PERSONA if pd.notna(first[c])} if a['study'] == 'study1' else {}
        agents.append({'agent_id': a['agent_id'], 'study': a['study'], 'phase': a['phase'],
                       'observed_socioeconomic_facts': facts,
                       'policy_frame': 'COVID-19' if a['study'] == 'study1' else first.condition})
        for _, r in rows.iterrows():
            attrs = {c: json_value(r[c]) for c in RECIPIENT}
            assert all(v is not None for v in attrs.values())
            profiles.append({'agent_id': a['agent_id'], 'task_number': int(r.vignette_num),
                             'recipient_attributes': attrs})
    def verify_input(row):
        if isinstance(row, dict):
            assert not FORBIDDEN & set(row)
            for value in row.values(): verify_input(value)
        elif isinstance(row, list):
            for value in row: verify_input(value)
    for row in agents + profiles: verify_input(row)
    # Each runtime arm gets only the facts that arm is allowed to observe.
    common = [{**a, 'observed_socioeconomic_facts': {}} for a in agents]
    write_jsonl(inputs / 'agents.jsonl', common)
    for arm in ['no_persona', 'socioeconomic_persona', 'socioeconomic_persona_without_income']:
        folder = inputs / arm
        folder.mkdir()
        rows = []
        for a in agents:
            if a['study'] != 'study1':
                continue
            facts = dict(a['observed_socioeconomic_facts'])
            if arm == 'no_persona': facts = {}
            if arm == 'socioeconomic_persona_without_income': facts.pop('respondent_income', None)
            rows.append({**a, 'arm': arm, 'observed_socioeconomic_facts': facts})
        if arm == 'no_persona': assert all(not a['observed_socioeconomic_facts'] for a in rows)
        if arm.endswith('without_income'): assert all('respondent_income' not in a['observed_socioeconomic_facts'] for a in rows)
        write_jsonl(folder / 'agents.jsonl', rows)
    write_jsonl(inputs / 'recipient_profiles.jsonl', profiles)
    pd.DataFrame(assignments).to_csv(reference / 'cohort_linkage.tsv', sep='\t', index=False)
    for name, d in [('study1', s1), ('study2', s2)]:
        selected = [a['source_id'] for a in assignments if a['study'] == name]
        d[d.id.isin(selected)].to_csv(reference / f'{name}_human_reference.tsv', sep='\t', index=False)
    eligible_subjects = s1[s1.id.isin(eligible)].drop_duplicates('id')
    confirm_subjects = s1[s1.id.isin(confirm)].drop_duplicates('id')
    report = {
        'status': 'design_inputs_only_no_model_outputs', 'seed': SEED,
        'model_calls_made': 0, 'paid_spend': 0,
        'generation_enabled': False, 'reason': 'Current model, hosted support/export and campaign budget not established; protocol reconstruction checks pending.',
        'study1_raw_people': int(s1.id.nunique()), 'study1_eligible_complete_people': len(eligible),
        'study1_excluded_incomplete_people': int(s1.id.nunique() - len(eligible)),
        'study1_pilot_people': len(pilot), 'study1_confirmatory_people': len(confirm),
        'study1_complete_pool_income': eligible_subjects.respondent_income.fillna('NOT_REPORTED').value_counts().to_dict(),
        'study1_confirmatory_income': confirm_subjects.respondent_income.fillna('NOT_REPORTED').value_counts().to_dict(),
        'study2_context_people': sum(a['study'] == 'study2' for a in assignments),
        'planned_primary_arms': ['no_persona', 'socioeconomic_persona', 'socioeconomic_persona_without_income'],
        'planned_call_counts': {'study1_primary_pilot': 32 * 3 * 2,
                                'study1_primary_confirmatory': 768 * 3 * 2,
                                'study1_optional_second_model_pilot': 16 * 3 * 2,
                                'study1_optional_second_model_confirmatory': 256 * 3 * 2,
                                'study2_context': 256 * 4},
        'planned_count_assumptions': 'One call per Study1 pair, returning two independently allocated amounts, two pair tasks/person; one call per Study2 single profile, allocation measured first. These are declared adaptations, not exact original UI replication.',
        'no_outcome_based_cohort_selection': 'S1 eligibility uses completeness of randomized recipient attributes only; S1/S2 selection uses seed and IDs (S2 original frame stratification). No allocation values/rankings/effects select participants.',
        'human_results_previously_seen': True,
        'persona_information': 'Three factual socioeconomic fields only; omission of a missing income field is consistent across arms. Not a complete individual digital twin.',
        'human_population_scope': 'Complete-profile retained survey respondents for S1; report selection sensitivity versus full released sample. No national population weights available.',
        'identity_limit': 'Original name assignments not released; reconstructed names and inferred pairing require disclosed assumptions. S2 minority subgroups collapsed in data.',
        'input_integrity_checks': ['unique respondent-task IDs', 'four tasks per source ID',
                                   'no missing recipient attributes in generated input',
                                   'pilot/confirmation IDs disjoint', 'no human outcome/attitude keys in generation input',
                                   'no-persona arm has no socioeconomic facts', 'without-income arm cannot read an income field from its agent file'],
        'source_sha256': {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(root.glob('*.tab'))},
    }
    artifacts = [p for p in args.output.rglob('*') if p.is_file()]
    report['artifact_sha256'] = {str(p.relative_to(args.output)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(artifacts)}
    (args.output / 'manifest.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({k: report[k] for k in ['status', 'study1_eligible_complete_people', 'study1_pilot_people', 'study1_confirmatory_people', 'study1_confirmatory_income', 'study2_context_people', 'planned_call_counts', 'model_calls_made']}, indent=2))


if __name__ == '__main__':
    main()
