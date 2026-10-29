"""Offline audit of the user-provided Bridgman replication archive.

No model calls, package installation, or modifications to the source files.
Python translation of main.Rmd Study 2 cleaning; not a full R replication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

LEVELS = {
    "vignette_gender": ["Female", "Male"],
    "vignette_ethnicity": ["White", "Visible minority"],
    "vignette_health": ["Healthy", "Poor health"],
    "vignette_citizen": ["Not a citizen", "Citizen born in Canada", "Citizen not born in Canada"],
    "vignette_marital": ["Single", "Married"],
    "vignette_children": ["No children", "Children under 5"],
    "vignette_employment": ["Employed full-time", "Underemployed", "Unemployed"],
    "vignette_income": ["$120,000", "$90,000", "$60,000", "$30,000"],
}


def counts(data):
    return {"rows": len(data), "respondents": int(data.id.nunique())}


def clean_study2(raw):
    """Preserve row-level exclusions and strict inequalities in Rmd 579–592."""
    audit = {"raw": counts(raw)}
    median = float(raw.duration.median())
    data = raw.loc[raw.duration > median * 0.33].copy()
    audit["median_duration_seconds"] = median
    audit["after_duration"] = counts(data)
    data = data.loc[data.vignette_allocation < 9999].copy()
    audit["after_below_9999_and_nonmissing"] = counts(data)
    cutoffs = data.groupby("condition").vignette_allocation.quantile(0.98).to_dict()
    data = data.loc[data.vignette_allocation < data.condition.map(cutoffs)].copy()
    audit["strict_condition_98th_percentile_cutoffs"] = cutoffs
    audit["final"] = counts(data)
    audit["retained_tasks_per_respondent"] = {
        str(k): int(v) for k, v in data.groupby("id").size().value_counts().items()
    }
    audit["straightlining"] = "No extra filter added: the distributed Rmd has none in this block. Upstream preprocessing cannot be verified from this archive."
    return data, audit


def matrix(data):
    arrays, terms = [np.ones(len(data))], [("intercept", "intercept", "intercept")]
    for feature, levels in LEVELS.items():
        if not set(data[feature].dropna().unique()) <= set(levels):
            raise ValueError(f"Unexpected levels in {feature}")
        if data[feature].isna().any():
            raise ValueError(f"Missing randomized attribute {feature}")
        for level in levels[1:]:
            arrays.append((data[feature] == level).to_numpy(dtype=float))
            terms.append((feature, level, levels[0]))
    return np.column_stack(arrays), terms


def fit(data):
    x, terms = matrix(data)
    y = data.vignette_allocation.to_numpy(dtype=float)
    beta, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != x.shape[1]:
        raise ValueError("Rank-deficient design")
    # Validate the solution independently through the normal equations.
    bread = np.linalg.inv(x.T @ x)
    np.testing.assert_allclose(beta, np.linalg.solve(x.T @ x, x.T @ y), rtol=1e-8, atol=1e-8)
    group, ids = pd.factorize(data.id, sort=True)
    scores = np.zeros((len(ids), x.shape[1]))
    np.add.at(scores, group, x * (y - x @ beta)[:, None])
    n, k = x.shape
    correction = len(ids) / (len(ids) - 1) * (n - 1) / (n - k)
    covariance = bread @ (scores.T @ scores) @ bread * correction
    se = np.sqrt(np.maximum(0, np.diag(covariance)))
    rows = []
    for (feature, level, reference), estimate, error in zip(terms[1:], beta[1:], se[1:]):
        rows.append({"feature": feature, "level": level, "reference": reference,
                     "estimate_cad": estimate, "cluster_se_cad": error,
                     "lower95_normal_cad": estimate - 1.96 * error,
                     "upper95_normal_cad": estimate + 1.96 * error,
                     "estimate_divided_by_frame_mean": estimate / y.mean()})
    return rows


def bootstrap_low_income(data, replicates, seed):
    """Cluster bootstrap, re-estimating frame means in every replicate.

    Independent samples across the randomized frames; uncertainty is over
    sampled humans, not over LLM calls. CI is percentile, without multiplicity.
    """
    rng = np.random.default_rng(seed)
    results = {}
    for frame, part in data.groupby("condition", sort=True):
        x, terms = matrix(part)
        index = terms.index(("vignette_income", "$30,000", "$120,000"))
        y = part.vignette_allocation.to_numpy(float)
        group, ids = pd.factorize(part.id, sort=True)
        m = len(ids)
        xx = np.zeros((m, x.shape[1], x.shape[1]))
        xy = np.zeros((m, x.shape[1]))
        sy = np.zeros(m)
        nn = np.bincount(group, minlength=m)
        np.add.at(xx, group, x[:, :, None] * x[:, None, :])
        np.add.at(xy, group, x * y[:, None])
        np.add.at(sy, group, y)
        draws = []
        for _ in range(replicates):
            w = rng.multinomial(m, np.full(m, 1 / m))
            b = np.linalg.solve(np.einsum("i,ijk->jk", w, xx), w @ xy)
            draws.append(b[index] / ((w @ sy) / (w @ nn)))
        results[frame] = np.asarray(draws)
    delta = results["GST"] - results["COVID-19"]
    return {"replicates": replicates, "seed": seed,
            "estimand": "GST minus COVID-19, low-income ($30k vs $120k) adjusted effect divided by each frame mean",
            "percentile95": np.quantile(delta, [0.025, 0.975]).tolist(),
            "normalization_mean_reestimated": True,
            "warning": "Sensitivity to exclusions and published-code comparison remain necessary."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bootstrap", type=int, default=500)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    source = args.source
    inventory = {}
    for file in sorted(source.glob("*.tab")):
        raw = pd.read_csv(file, sep="\t")
        if raw.duplicated(["id", "vignette_num"]).any():
            raise ValueError(f"Duplicate respondent-task identifiers: {file.name}")
        inventory[file.name] = {**counts(raw), "columns": list(raw.columns),
                                "missing_allocation": int(raw.vignette_allocation.isna().sum()),
                                "sha256": hashlib.sha256(file.read_bytes()).hexdigest()}
    raw = pd.read_csv(source / "study2.tab", sep="\t")
    if not (raw.groupby("id").condition.nunique() == 1).all():
        raise ValueError("Condition changes within respondent")
    cleaned, cleaning = clean_study2(raw)
    cleaned.to_csv(args.output / "study2_cleaned.tsv", sep="\t", index=False)
    summaries, effects = [], []
    for frame, part in cleaned.groupby("condition", sort=True):
        summaries.append({"condition": frame, **counts(part),
                          "mean_cad": float(part.vignette_allocation.mean()),
                          "median_cad": float(part.vignette_allocation.median()),
                          "sd_cad": float(part.vignette_allocation.std())})
        effects.extend({"condition": frame, **row} for row in fit(part))
    pd.DataFrame(effects).to_csv(args.output / "study2_attribute_effects.csv", index=False)
    low = {r["condition"]: r["estimate_divided_by_frame_mean"] for r in effects
           if r["feature"] == "vignette_income" and r["level"] == "$30,000"}
    boot = bootstrap_low_income(cleaned, args.bootstrap, 20261029)
    boot["point_estimate"] = low["GST"] - low["COVID-19"]
    report = {"status": "human_data_reanalysis_only", "model_calls": 0,
              "inventory": inventory, "study2_cleaning": cleaning,
              "study2_summary": summaries, "primary_candidate_contrast": boot,
              "method": "OLS with all eight randomized attributes, respondent-clustered CR1 normal intervals. R cregg SE equivalence not yet established.",
              "scope": "Study 2 only; alt dataset catalogued, not pooled or independently replicated.",
              "missing_for_exact_procedure": ["Original individual profile names", "Respondent-level outcome-order assignment", "Verified timing of attitude questions"],
              "integrity_checks": ["Unique id-task pairs", "Condition constant within person", "Expected factor levels and no missing randomized attributes", "Full-rank design", "OLS versus independent normal-equation solution"]}
    speed = raw.loc[raw.duration > raw.duration.median() * 0.33].copy()
    variants = {"all_nonmissing": raw.dropna(subset=["vignette_allocation"]),
                "duration_only_nonmissing": speed.dropna(subset=["vignette_allocation"]),
                "duration_and_below9999": speed.loc[speed.vignette_allocation < 9999],
                "published_code": cleaned}
    sensitivity = {}
    for name, variant in variants.items():
        frames, low_effect = {}, {}
        for frame, part in variant.groupby("condition"):
            row = next(r for r in fit(part) if r["feature"] == "vignette_income" and r["level"] == "$30,000")
            low_effect[frame] = row["estimate_divided_by_frame_mean"]
            frames[frame] = {**counts(part), "mean_cad": float(part.vignette_allocation.mean()),
                             "low_income_effect_cad": row["estimate_cad"],
                             "low_income_effect_divided_by_mean": low_effect[frame]}
        sensitivity[name] = {"frames": frames, "normalized_effect_difference_gst_minus_covid": low_effect["GST"] - low_effect["COVID-19"]}
    (args.output / "exclusion_sensitivity.json").write_text(json.dumps(sensitivity, indent=2))
    (args.output / "audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({k: report[k] for k in ["status", "study2_summary", "primary_candidate_contrast", "model_calls"]}, indent=2))


if __name__ == "__main__":
    main()
