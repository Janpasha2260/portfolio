"""Workshop 4 evidence: data-quality audit on a real UCI dataset.

Dataset: Wisconsin Diagnostic Breast Cancer (569 records, 30 numeric features).
Source: UCI Machine Learning Repository; loaded from scikit-learn.
Controlled defects are added only to a training copy to demonstrate cleaning.
This educational analysis is not a clinical diagnostic system.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42
OUTPUT = Path(__file__).with_name("workshop4_outputs")


def metric_row(name, y_true, prediction, probability):
    return {
        "model_input": name,
        "accuracy": accuracy_score(y_true, prediction),
        "precision_malignant": precision_score(y_true, prediction, zero_division=0),
        "recall_malignant": recall_score(y_true, prediction, zero_division=0),
        "f1_malignant": f1_score(y_true, prediction, zero_division=0),
        "roc_auc": roc_auc_score(y_true, probability),
    }


def count_outside_caps(frame, caps):
    return sum(int(((frame[column] < lower) | (frame[column] > upper)).sum())
               for column, (lower, upper) in caps.items())


def main():
    OUTPUT.mkdir(exist_ok=True)
    dataset = load_breast_cancer(as_frame=True)
    x = dataset.data.copy()
    # Positive class is malignant because missing a malignancy is the costly error.
    y = pd.Series((dataset.target == 0).astype(int), name="malignant")
    source = x.copy(); source["malignant"] = y
    source.to_csv(OUTPUT / "real_dataset_snapshot.csv", index=False)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE
    )
    rng = np.random.default_rng(RANDOM_STATE)
    corrupted = x_train.copy()
    defect_columns = ["mean radius", "mean texture", "mean area"]

    # Controlled quality defects for a reproducible audit.
    for column in defect_columns:
        rows = rng.choice(corrupted.index, size=12, replace=False)
        corrupted.loc[rows, column] = np.nan
    outlier_rows = rng.choice(corrupted.index, size=5, replace=False)
    corrupted.loc[outlier_rows, "mean area"] *= 8
    duplicate_rows = corrupted.sample(8, random_state=RANDOM_STATE)
    corrupted = pd.concat([corrupted, duplicate_rows], axis=0, ignore_index=False)
    corrupted_y = pd.concat([y_train, y_train.loc[duplicate_rows.index]], axis=0)

    reference_caps = {column: tuple(x_train[column].quantile([0.01, 0.99])) for column in defect_columns}
    before = {
        "missing_values": int(corrupted.isna().sum().sum()),
        "duplicate_rows": int(corrupted.duplicated().sum()),
        "values_outside_caps": count_outside_caps(corrupted, reference_caps),
    }

    # Cleaning: remove exact duplicates, median-impute, and cap using training quantiles.
    keep = ~corrupted.duplicated()
    cleaned = corrupted.loc[keep].copy()
    cleaned_y = corrupted_y.loc[keep].copy()
    caps = {}
    for column in cleaned.columns:
        lower, upper = cleaned[column].quantile([0.01, 0.99])
        caps[column] = (lower, upper)
        cleaned[column] = cleaned[column].clip(lower, upper)

    after = {
        "missing_values": 0,
        "duplicate_rows": int(cleaned.duplicated().sum()),
        "values_outside_caps": count_outside_caps(cleaned, caps),
    }
    audit = pd.DataFrame({"quality_check": before.keys(), "before_cleaning": before.values(), "after_cleaning": after.values()})
    audit.to_csv(OUTPUT / "data_quality_audit.csv", index=False)

    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(class_weight="balanced", max_iter=3000, random_state=RANDOM_STATE)),
    ])
    results = []
    for name, train_x, train_y in [("controlled_defects", corrupted, corrupted_y), ("cleaned_training_data", cleaned, cleaned_y)]:
        model.fit(train_x, train_y)
        probability = model.predict_proba(x_test)[:, 1]
        prediction = (probability >= 0.5).astype(int)
        results.append(metric_row(name, y_test, prediction, probability))
    metrics = pd.DataFrame(results)
    metrics.to_csv(OUTPUT / "model_impact_metrics.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    audit.set_index("quality_check")[["before_cleaning", "after_cleaning"]].plot(kind="bar", ax=axes[0], color=["#ef6b56", "#42b883"])
    axes[0].set_title("Controlled Data Defects Before and After Cleaning")
    axes[0].set_ylabel("Count")
    axes[0].tick_params(axis="x", rotation=20)
    metrics.set_index("model_input")[["recall_malignant", "f1_malignant", "roc_auc"]].plot(kind="bar", ax=axes[1], color=["#3478f6", "#8b7cff", "#27b8a7"])
    axes[1].set_title("Impact on the Same Untouched Test Set")
    axes[1].set_ylim(0.75, 1.01)
    axes[1].tick_params(axis="x", rotation=15)
    fig.tight_layout()
    fig.savefig(OUTPUT / "workshop4_evidence.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    with open(OUTPUT / "run_output.txt", "w", encoding="utf-8") as handle:
        handle.write("WORKSHOP 4 — REAL DATA EVIDENCE\n")
        handle.write("Dataset: Wisconsin Diagnostic Breast Cancer (UCI)\n")
        handle.write(f"Records: {len(x)} | Features: {x.shape[1]}\n")
        handle.write(f"Class counts — malignant: {int(y.sum())}, benign: {int((1-y).sum())}\n\n")
        handle.write("DATA QUALITY AUDIT\n" + audit.to_string(index=False) + "\n\n")
        handle.write("MODEL IMPACT ON UNTOUCHED TEST SET\n" + metrics.round(4).to_string(index=False) + "\n\n")
        handle.write("Bias limitation: no demographic attributes are present, so demographic fairness is not claimed.\n")
        handle.write("Clinical limitation: educational evidence only; not approved for diagnosis.\n")
    print((OUTPUT / "run_output.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
