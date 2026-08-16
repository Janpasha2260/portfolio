"""Final project using the real scikit-learn diabetes dataset."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


OUTPUT = Path(__file__).parent / "final_project_outputs"
OUTPUT.mkdir(exist_ok=True)

# I load the real dataset and keep the feature names supplied by scikit-learn.
dataset = load_diabetes(as_frame=True)
data = dataset.frame.copy()
data.insert(0, "record_id", range(1, len(data) + 1))
data.to_csv(OUTPUT / "diabetes_real_dataset.csv", index=False)

X = data.drop(columns=["record_id", "target"])
y = data["target"]

# I reserve the test set before comparing any models.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

models = {
    "Ridge regression": Pipeline([
        ("scale", StandardScaler()),
        ("model", Ridge(alpha=10.0)),
    ]),
    "Random forest": RandomForestRegressor(
        n_estimators=400, min_samples_leaf=4, random_state=42, n_jobs=-1
    ),
}

cv = KFold(n_splits=5, shuffle=True, random_state=42)
rows = []
for name, model in models.items():
    scores = cross_validate(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring={"mae": "neg_mean_absolute_error", "r2": "r2"},
    )
    rows.append({
        "model": name,
        "cv_mae_mean": -scores["test_mae"].mean(),
        "cv_mae_std": scores["test_mae"].std(),
        "cv_r2_mean": scores["test_r2"].mean(),
        "cv_r2_std": scores["test_r2"].std(),
    })

comparison = pd.DataFrame(rows).sort_values("cv_mae_mean")
comparison.to_csv(OUTPUT / "model_comparison.csv", index=False)
selected_name = comparison.iloc[0]["model"]
selected = models[selected_name]
selected.fit(X_train, y_train)
predictions = selected.predict(X_test)

metrics = pd.DataFrame([{
    "selected_model": selected_name,
    "test_records": len(y_test),
    "test_mae": mean_absolute_error(y_test, predictions),
    "test_rmse": mean_squared_error(y_test, predictions) ** 0.5,
    "test_r2": r2_score(y_test, predictions),
}])
metrics.to_csv(OUTPUT / "test_metrics.csv", index=False)

prediction_table = pd.DataFrame({
    "record_id": data.loc[X_test.index, "record_id"],
    "actual_progression": y_test,
    "predicted_progression": predictions,
    "absolute_error": abs(y_test - predictions),
}).sort_values("record_id")
prediction_table.to_csv(OUTPUT / "test_predictions.csv", index=False)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
axes[0].bar(comparison["model"], comparison["cv_mae_mean"], color=["#3478f6", "#ff9d48"])
axes[0].set_title("Five-Fold Cross-Validation")
axes[0].set_ylabel("Mean absolute error (lower is better)")
axes[0].tick_params(axis="x", rotation=12)

axes[1].scatter(y_test, predictions, alpha=0.75, color="#3478f6", edgecolor="white")
low = min(y_test.min(), predictions.min())
high = max(y_test.max(), predictions.max())
axes[1].plot([low, high], [low, high], "--", color="#ff9d48", label="Perfect prediction")
axes[1].set_title(f"Untouched Test Set: {selected_name}")
axes[1].set_xlabel("Actual progression")
axes[1].set_ylabel("Predicted progression")
axes[1].legend()
fig.suptitle("Real Diabetes Dataset - Final Project Evidence", fontweight="bold")
fig.tight_layout()
fig.savefig(OUTPUT / "final_project_evidence.png", dpi=180, bbox_inches="tight")

with (OUTPUT / "run_output.txt").open("w", encoding="utf-8") as handle:
    handle.write("REAL DATASET: scikit-learn diabetes dataset\n")
    handle.write(f"Records: {len(data)} | Features: {X.shape[1]}\n")
    handle.write(f"Training records: {len(X_train)} | Untouched test records: {len(X_test)}\n\n")
    handle.write("MODEL COMPARISON\n")
    handle.write(comparison.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    handle.write("\n\nUNTOUCHED TEST METRICS\n")
    handle.write(metrics.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    handle.write("\n")

print((OUTPUT / "run_output.txt").read_text())
