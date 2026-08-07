"""Workshop 5 evidence: validation and verification on a real UCI dataset.

Compares two candidate models, chooses a threshold using validation data, and
evaluates once on an untouched test set. Educational use only; not clinical.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score,
                             confusion_matrix, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 17
OUTPUT = Path(__file__).with_name("workshop5_outputs")


def scores(y_true, probability, threshold):
    prediction = (probability >= threshold).astype(int)
    return {
        "accuracy": accuracy_score(y_true, prediction),
        "precision_malignant": precision_score(y_true, prediction, zero_division=0),
        "recall_malignant": recall_score(y_true, prediction, zero_division=0),
        "f1_malignant": f1_score(y_true, prediction, zero_division=0),
        "roc_auc": roc_auc_score(y_true, probability),
    }


def choose_threshold(y_valid, probability):
    candidates = []
    for threshold in np.arange(0.10, 0.91, 0.01):
        result = scores(y_valid, probability, float(threshold))
        if result["recall_malignant"] >= 0.90:
            candidates.append((result["f1_malignant"], result["precision_malignant"], float(threshold)))
    return max(candidates)[2] if candidates else 0.50


def main():
    OUTPUT.mkdir(exist_ok=True)
    dataset = load_breast_cancer(as_frame=True)
    x = dataset.data.copy()
    y = pd.Series((dataset.target == 0).astype(int), name="malignant")

    # 60/20/20 split: test data remain untouched until final evaluation.
    x_train, x_temp, y_train, y_temp = train_test_split(x, y, test_size=0.40, stratify=y, random_state=RANDOM_STATE)
    x_valid, x_test, y_valid, y_test = train_test_split(x_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=RANDOM_STATE)

    verification = {
        "expected_feature_count": x_train.shape[1] == 30,
        "binary_target": set(y.unique()) == {0, 1},
        "train_validation_disjoint": set(x_train.index).isdisjoint(x_valid.index),
        "train_test_disjoint": set(x_train.index).isdisjoint(x_test.index),
        "validation_test_disjoint": set(x_valid.index).isdisjoint(x_test.index),
        "no_source_missing_values": int(x.isna().sum().sum()) == 0,
        "split_total_matches_source": len(x_train) + len(x_valid) + len(x_test) == len(x),
    }
    assert all(verification.values())
    pd.DataFrame({"verification_check": verification.keys(), "passed": verification.values()}).to_csv(OUTPUT / "verification_checklist.csv", index=False)

    models = {
        "logistic_regression": Pipeline([("scale", StandardScaler()), ("model", LogisticRegression(class_weight="balanced", max_iter=3000, random_state=RANDOM_STATE))]),
        "random_forest": RandomForestClassifier(n_estimators=500, class_weight="balanced", min_samples_leaf=2, random_state=RANDOM_STATE),
    }
    validation_rows = []
    fitted = {}
    for name, model in models.items():
        model.fit(x_train, y_train)
        probability = model.predict_proba(x_valid)[:, 1]
        threshold = choose_threshold(y_valid, probability)
        row = {"model": name, "threshold": threshold, **scores(y_valid, probability, threshold)}
        validation_rows.append(row); fitted[name] = model
    validation = pd.DataFrame(validation_rows)
    validation.to_csv(OUTPUT / "validation_model_comparison.csv", index=False)
    selected_name = validation.sort_values(["f1_malignant", "roc_auc"], ascending=False).iloc[0]["model"]
    selected_threshold = float(validation.loc[validation["model"] == selected_name, "threshold"].iloc[0])
    selected = fitted[selected_name]

    test_probability = selected.predict_proba(x_test)[:, 1]
    test_prediction = (test_probability >= selected_threshold).astype(int)
    test_metrics = pd.DataFrame([{ "selected_model": selected_name, "threshold": selected_threshold, **scores(y_test, test_probability, selected_threshold)}])
    test_metrics.to_csv(OUTPUT / "untouched_test_metrics.csv", index=False)
    predictions = pd.DataFrame({"source_row": x_test.index, "actual_malignant": y_test.values, "predicted_malignant": test_prediction, "malignant_probability": test_probability})
    predictions.to_csv(OUTPUT / "test_predictions.csv", index=False)
    matrix = confusion_matrix(y_test, test_prediction)
    pd.DataFrame(matrix, index=["actual_benign", "actual_malignant"], columns=["predicted_benign", "predicted_malignant"]).to_csv(OUTPUT / "confusion_matrix.csv")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7))
    ConfusionMatrixDisplay(matrix, display_labels=["Benign", "Malignant"]).plot(ax=axes[0], cmap="Blues", colorbar=False)
    axes[0].set_title("Untouched Test Confusion Matrix")
    RocCurveDisplay.from_predictions(y_test, test_probability, ax=axes[1], color="#8b7cff")
    axes[1].set_title("Untouched Test ROC Curve")
    fig.suptitle(f"Workshop 5 Evidence — {selected_name.replace('_', ' ').title()}")
    fig.tight_layout()
    fig.savefig(OUTPUT / "workshop5_evidence.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    with open(OUTPUT / "run_output.txt", "w", encoding="utf-8") as handle:
        handle.write("WORKSHOP 5 — REAL DATA VALIDATION AND VERIFICATION\n")
        handle.write("Dataset: Wisconsin Diagnostic Breast Cancer (UCI)\n")
        handle.write(f"Records: {len(x)} | Features: {x.shape[1]}\n")
        handle.write(f"Split sizes — train: {len(x_train)}, validation: {len(x_valid)}, test: {len(x_test)}\n\n")
        handle.write("VERIFICATION CHECKS\n")
        for name, passed in verification.items(): handle.write(f"{name}: {'PASSED' if passed else 'FAILED'}\n")
        handle.write("\nVALIDATION MODEL COMPARISON\n" + validation.round(4).to_string(index=False) + "\n\n")
        handle.write(f"SELECTED MODEL: {selected_name}; THRESHOLD: {selected_threshold:.2f}\n")
        handle.write("\nUNTOUCHED TEST METRICS\n" + test_metrics.round(4).to_string(index=False) + "\n")
        handle.write("\nCONFUSION MATRIX\n" + np.array2string(matrix) + "\n")
        handle.write("\nRelease decision: educational validation passed; clinical deployment NOT authorized.\n")
    print((OUTPUT / "run_output.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
