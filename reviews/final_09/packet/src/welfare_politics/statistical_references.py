"""Fixed, human-label-trained conditional-mean references; no model calls.

These are practical predictors with different label access from the LLM arms.
They are neither synthetic respondent trajectories nor oracle software tables.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .paired_evaluation import evaluate_arrays
from .primary_design import construct, matrix_and_contrast
from .study1_interest_audit import LEVELS

NAMES = ['B_mean', 'B_recipient_OLS', 'B_income_interacted_OLS']


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def id_digest(ids):
    return hashlib.sha256(json.dumps(sorted(int(i) for i in ids)).encode()).hexdigest()


def _features(data, name):
    # Explicit whitelist through the canonical builder. No ID, target outcome,
    # task number, job risk or parenthood enters the prediction matrix.
    if not data.respondent_income.isin(['High income', 'Low income']).all():
        raise ValueError('References require observed high/low respondent income')
    if data[list(LEVELS)].isna().any().any():
        raise ValueError('Complete recipient predictors required')
    x, _ = matrix_and_contrast(data)
    if name == 'B_mean':
        return x[:, :1]
    if name == 'B_recipient_OLS':
        return x[:, :x.shape[1]//2]
    if name == 'B_income_interacted_OLS':
        return x
    raise ValueError('Unknown fixed reference')


def fit_predict(training, target_predictors, name):
    """Fit using training labels only; target labels are never read."""
    if set(training.id) & set(target_predictors.id):
        raise ValueError('Training and target people overlap')
    x = _features(training, name)
    target_x = _features(target_predictors, name)
    y = training.vignette_allocation.to_numpy(float)
    if not np.isfinite(y).all() or not ((0 <= y) & (y <= 4000)).all():
        raise ValueError('Observed bounded training labels required')
    beta, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != x.shape[1]:
        raise ValueError('Full-rank statistical reference design required')
    raw = target_x @ beta
    predicted = np.clip(raw, 0, 4000)
    return predicted, {'columns': x.shape[1], 'rank': int(rank),
                       'training_people': int(training.id.nunique()),
                       'training_labels': len(y), 'coefficients': beta.tolist(),
                       'raw_prediction_min': float(raw.min()),
                       'raw_prediction_max': float(raw.max()),
                       'clipped_prediction_rows': int(np.count_nonzero(raw != predicted))}


def person_folds(training, seed, folds):
    if folds < 2:
        raise ValueError('At least two folds required')
    if training.groupby('id').respondent_income.nunique(dropna=False).gt(1).any():
        raise ValueError('Income changes within a person')
    rng = np.random.default_rng(seed)
    groups = training.drop_duplicates('id').groupby('respondent_income')
    chunks = []
    for _, part in groups:
        ids = np.asarray(sorted(part.id.tolist()))
        if len(ids) < folds:
            raise ValueError('Insufficient people for income-stratified folds')
        chunks.append(np.array_split(rng.permutation(ids), folds))
    return [set(int(i) for group_chunks in chunks for i in group_chunks[k])
            for k in range(folds)]


def errors(reference, predicted):
    residual = np.asarray(predicted)-np.asarray(reference)
    return {'rmse_cad': float(np.sqrt(np.mean(residual**2))),
            'mae_cad': float(np.mean(np.abs(residual)))}


def eligible_pool(data):
    """Validate person-level income BEFORE removing non-high/low rows."""
    if data.duplicated(['id', 'vignette_num']).any():
        raise ValueError('Duplicate source row')
    if data.groupby('id').respondent_income.nunique(dropna=False).gt(1).any():
        raise ValueError('Income changes within a source person')
    observed = (data[list(LEVELS)].notna().all(axis=1)
                & data.vignette_allocation.notna()
                & data.vignette_allocation.between(0, 4000))
    complete = observed.groupby(data.id).all() & data.groupby('id').size().eq(4)
    pool = data[data.id.isin(complete[complete].index)
                & data.respondent_income.isin(['High income', 'Low income'])]
    if not pool.groupby('id').size().eq(4).all():
        raise AssertionError('Eligibility must preserve whole four-row people')
    return pool


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, default=Path('data/raw/study1.tab'))
    p.add_argument('--cohort', type=Path, required=True)
    p.add_argument('--spec', type=Path, default=Path('configs/human_statistical_references_v1.json'))
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    spec = json.loads(args.spec.read_text())
    if spec['version'] != 1 or spec['comparators'] != NAMES:
        raise ValueError('Unsupported fixed reference specification')
    for key, path in [('source_sha256', args.source), ('cohort_linkage_sha256', args.cohort)]:
        if digest(path) != spec[key]:
            raise ValueError(f'Specification hash mismatch: {key}')
    data = pd.read_csv(args.source, sep='\t')
    pool = eligible_pool(data)
    linkage = pd.read_csv(args.cohort, sep='\t')
    linkage = linkage[linkage.study.eq('study1')]
    if linkage.source_id.duplicated().any() or not set(linkage.phase) <= {'pilot', 'confirmatory'}:
        raise ValueError('Unexpected or duplicated candidate people')
    main_ids = set(linkage.loc[linkage.phase.eq('confirmatory'), 'source_id'])
    excluded = set(linkage.source_id)
    training = pool[~pool.id.isin(excluded)].sort_values(['id', 'vignette_num'])
    target = pool[pool.id.isin(main_ids)].sort_values(['id', 'vignette_num'])
    x, human, c, rows, design = construct(data, sorted(main_ids))
    if rows != [f's1:{i}:{j}' for i, j in zip(target.id, target.vignette_num)]:
        raise AssertionError('Statistical predictions do not align with locked rows')
    if len(training) == 0 or set(training.id) & excluded:
        raise ValueError('Invalid disjoint training cohort')
    cv_spec = spec['cross_validation']
    folds = person_folds(training, cv_spec['seed'], cv_spec['folds'])
    if set.union(*folds) != set(training.id) or sum(map(len, folds)) != training.id.nunique():
        raise AssertionError('Folds must partition people exactly once')
    cv_predictions = {name: np.full(len(training), np.nan) for name in NAMES}
    fold_records = []
    for index, ids in enumerate(folds):
        test_mask = training.id.isin(ids).to_numpy()
        train = training.loc[~test_mask]
        test = training.loc[test_mask]
        # Outcome-free target frame is a deliberate computational barrier.
        predictors = test.drop(columns=['vignette_allocation'])
        records = {}
        for name in NAMES:
            predictions, metadata = fit_predict(train, predictors, name)
            cv_predictions[name][test_mask] = predictions
            records[name] = metadata
        fold_records.append({'fold': index, 'validation_people': len(ids),
                             'validation_ids_sha256': id_digest(ids), 'fits': records})
    predictions, fits = {}, {}
    target_predictors = target.drop(columns=['vignette_allocation'])
    for name in NAMES:
        predictions[name], fits[name] = fit_predict(training, target_predictors, name)
    evaluation = evaluate_arrays(x, human, predictions, c, rows)
    evaluation['target'] = 'finite matched cohort, fixed design, statistical conditional-mean predictions'
    evaluation['outcome_provenance'] = 'human-label-trained statistical references; no respondent-model outputs'
    for name in NAMES:
        evaluation['arms'][name]['prediction_errors'] = errors(human, predictions[name])
    args.output.mkdir(parents=True, exist_ok=False)
    np.savez(args.output / 'statistical_predictions.npz', row_ids=np.asarray(rows), **predictions)
    pd.DataFrame([{'source_id': int(i), 'fold': k} for k, ids in enumerate(folds)
                  for i in sorted(ids)]).to_csv(args.output / 'training_folds.tsv', sep='\t', index=False)
    report = {'status': 'human_label_trained_statistical_references_only',
              'actual_respondent_model_calls': 0, 'synthetic_respondent_trajectories_generated': False,
              'spec_sha256': digest(args.spec), 'source_sha256': digest(args.source),
              'implementation_sha256': {name: digest(Path(__file__).parent / name)
                                         for name in ['statistical_references.py', 'primary_design.py',
                                                      'paired_evaluation.py', 'contrast_validity.py',
                                                      'diagnostic_comparison.py', 'study1_interest_audit.py']},
              'runtime': {'numpy': np.__version__, 'pandas': pd.__version__},
              'cohort_linkage_sha256': digest(args.cohort),
              'training_people': int(training.id.nunique()), 'training_labels': len(training),
              'training_income_groups': training.drop_duplicates('id').respondent_income.value_counts().to_dict(),
              'training_cohort_sha256': id_digest(training.id.unique()),
              'target_people': int(target.id.nunique()), 'target_rows': len(target),
              'training_target_person_overlap': len(set(training.id) & set(target.id)),
              'target_cohort_sha256': id_digest(target.id.unique()),
              'locked_design_sha256': design['design_sha256'],
              'cross_validation': {'purpose': cv_spec['purpose'], 'folds': fold_records,
                                   'out_of_fold_errors': {name: errors(training.vignette_allocation, pred)
                                                          for name, pred in cv_predictions.items()}},
              'full_training_fits': fits, 'evaluation': evaluation,
              'limitations': [
                  'Source and main outcomes were already inspected during research development.',
                  'These references use disjoint human labels; LLM arms have different information access.',
                  'Conditional-mean predictions are not individual or stochastic respondent trajectories.',
                  'Same source selection and stimulus reconstruction limitations persist.',
                  'No reference, feature, setting or primary endpoint is selected by main results.',
                  'No claim about actual LLM fidelity, inequality, superiority, or human causal mechanisms.',
              ]}
    (args.output / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({'status': report['status'], 'training_people': report['training_people'],
                      'target_people': report['target_people'], 'model_calls': 0,
                      'cv_errors': report['cross_validation']['out_of_fold_errors'],
                      'main': {name: {'moderation': arm['lower'], 'components': arm['group_components'],
                                       'errors': arm['prediction_errors']}
                               for name, arm in evaluation['arms'].items()}}, indent=2))


if __name__ == '__main__':
    main()
