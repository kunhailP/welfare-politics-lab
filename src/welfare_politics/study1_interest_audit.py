"""Offline human reference for respondent-interest contrasts in Study 1.

These are subgroup differences in effects of randomized recipient attributes,
not causal effects of respondent income/employment/parenthood. No LLM calls.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

LEVELS = {
    "vignette_gender": ["Female", "Male"],
    "vignette_citizen": ["Not a citizen", "Citizen born in Canada", "Citizen not born in Canada"],
    "vignette_health": ["Healthy", "Poor health"],
    "vignette_marital": ["Single", "Married"],
    "vignette_children": ["No children", "Children under 5", "5-12", "Over 12"],
    "vignette_employment": ["Employed full-time", "Employed, reduced income", "Unemployed due to pandemic", "Unemployed"],
    "vignette_income": ["$120,000", "$90,000", "$60,000", "$30,000"],
    "vignette_ethnicity": ["White", "East Asian", "Indigenous", "South Asian"],
}


def contrast(data, respondent_feature, group0, group1, recipient_feature, level):
    selected = data.loc[data[respondent_feature].isin([group0, group1])].copy()
    d = selected.dropna(subset=list(LEVELS) + ['vignette_allocation']).copy()
    arrays, names = [np.ones(len(d))], ["intercept"]
    for feature, levels in LEVELS.items():
        if d[feature].isna().any() or not set(d[feature]) <= set(levels):
            raise ValueError(f"Missing/unexpected category in {feature}")
        for item in levels[1:]:
            arrays.append((d[feature] == item).to_numpy(float))
            names.append(f"{feature}:{item}")
    base = np.column_stack(arrays)
    g = (d[respondent_feature] == group1).to_numpy(float)
    x = np.column_stack([base, base * g[:, None]])
    y = d.vignette_allocation.to_numpy(float)
    b, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != x.shape[1]:
        raise ValueError("Insufficient rank")
    np.testing.assert_allclose(b, np.linalg.solve(x.T @ x, x.T @ y), atol=1e-7)
    groups, ids = pd.factorize(d.id)
    score = np.zeros((len(ids), x.shape[1]))
    np.add.at(score, groups, x * (y - x @ b)[:, None])
    bread = np.linalg.inv(x.T @ x)
    n, k = x.shape
    cov = bread @ (score.T @ score) @ bread * (len(ids) / (len(ids) - 1)) * ((n - 1) / (n - k))
    target = names.index(f"{recipient_feature}:{level}")
    def estimate(w):
        point = float(w @ b)
        se = float(np.sqrt(w @ cov @ w))
        return {"estimate_cad": point, "cluster_se_cad": se,
                "normal95": [point - 1.96 * se, point + 1.96 * se]}
    w0 = np.zeros(x.shape[1]); w0[target] = 1
    wd = np.zeros(x.shape[1]); wd[target + base.shape[1]] = 1
    return {"respondent_feature": respondent_feature,
            "input_tasks": len(selected), "complete_case_tasks": len(d),
            "recipient_contrast": f"{recipient_feature}: {level} versus {LEVELS[recipient_feature][0]}",
            "group0": group0, "group1": group1,
            "respondents_by_group": d.drop_duplicates('id')[respondent_feature].value_counts().to_dict(),
            "effect_group0": estimate(w0), "effect_group1": estimate(w0 + wd),
            "effect_difference_group1_minus_group0": estimate(wd)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=Path('data/raw'))
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    source = args.source / 'study1.tab'
    d = pd.read_csv(source, sep='\t')
    assert not d.duplicated(['id', 'vignette_num']).any()
    for column in [c for c in d if c.startswith('respondent_')]:
        assert d.groupby('id')[column].nunique(dropna=False).le(1).all()
    specs = [
        ('respondent_income', 'High income', 'Low income', 'vignette_income', '$30,000'),
        ('respondent_employment', 'Not at risk', 'At risk/laid off', 'vignette_employment', 'Unemployed due to pandemic'),
        ('respondent_children', 'No children', 'Children', 'vignette_children', 'Children under 5'),
    ]
    report = {'status': 'human_reanalysis_only', 'model_calls': 0,
              'people': int(d.id.nunique()), 'tasks': len(d),
              'method': 'All randomized recipient attributes fully interacted with respondent subgroup; OLS, respondent-clustered CR1, normal 95% intervals. Adjusted supplementary audit, not exact replication of original one-attribute subgroup regressions.',
              'warning': 'Respondent group is observational. CI including zero is not equivalence. Missing randomized attributes are excluded for this adjusted model; exclusion counts are reported per contrast. This sample represents retained survey respondents; weights are not distributed. Original pair presentation and information timing require verification before model prompting.',
              'contrasts': [contrast(d, *spec) for spec in specs]}
    (args.output / 'audit.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
