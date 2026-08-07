# Workshop 5: Real-Data Model Validation and Verification

## Artifact purpose

This artifact demonstrates verification, model comparison, threshold selection, final validation, and release judgment using the real Wisconsin Diagnostic Breast Cancer dataset. The analysis uses 569 observations and 30 numeric features loaded from scikit-learn’s copy of the UCI dataset. It is educational evidence and does not authorize clinical use.

## Development and evaluation design

The target was recoded so malignant cases are the positive class. This makes malignant recall easy to interpret because a false negative represents a missed malignant observation. The data were divided with stratification into 341 training observations, 114 validation observations, and 114 untouched test observations.

Training data were used to fit logistic regression and random forest candidates. Validation data were used to select a decision threshold while requiring at least 0.90 malignant recall. The final model was chosen by malignant F1 and ROC-AUC. The test set was used once after the model and threshold were fixed.

## Verification evidence

The program ran seven assertions before validation:

| Verification check | Result |
|---|---|
| Expected 30-feature schema | Passed |
| Binary target values | Passed |
| Training and validation indices disjoint | Passed |
| Training and test indices disjoint | Passed |
| Validation and test indices disjoint | Passed |
| No missing values in source data | Passed |
| Split sizes equal source size | Passed |

## Validation comparison

| Candidate model | Threshold | Accuracy | Malignant precision | Malignant recall | Malignant F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic regression | 0.62 | 0.9825 | 0.9762 | 0.9762 | 0.9762 | 0.9974 |
| Random forest | 0.35 | 0.9825 | 0.9545 | 1.0000 | 0.9767 | 0.9974 |

Random forest was selected because it produced the slightly higher malignant F1 while detecting every malignant case in the validation split. The selected threshold was 0.35.

## Untouched test evidence

| Metric | Result |
|---|---:|
| Accuracy | 0.9123 |
| Malignant precision | 0.8235 |
| Malignant recall | 0.9767 |
| Malignant F1 | 0.8936 |
| ROC-AUC | 0.9918 |

The confusion matrix contained 62 true benign predictions, nine benign observations predicted malignant, one missed malignant observation, and 42 correctly detected malignant observations. The decrease from validation performance to test performance demonstrates why an untouched test set is necessary. Reporting only the validation score would have overstated expected performance.

## Ethical release decision and monitoring

The technical validation completed successfully for an educational experiment, but clinical deployment is not authorized. The dataset does not prove performance across hospitals, devices, time periods, or demographic populations. A real release would require independent external validation, clinical and regulatory review, privacy and security controls, calibration assessment, documented human oversight, and an appeal or escalation pathway.

Post-deployment monitoring should track input drift, malignant recall, false-negative counts, calibration, missingness, schema changes, and performance for relevant groups when lawful demographic data are available. A material recall decline or data-quality failure should pause automated use and trigger human review.

## Included evidence files

- `model_validation_verification.py` — complete reproducible code
- `workshop5_outputs/verification_checklist.csv` — verification results
- `workshop5_outputs/validation_model_comparison.csv` — model-selection evidence
- `workshop5_outputs/untouched_test_metrics.csv` — final metrics
- `workshop5_outputs/confusion_matrix.csv` — error counts
- `workshop5_outputs/test_predictions.csv` — row-level predictions and probabilities
- `workshop5_outputs/run_output.txt` — recorded console evidence
- `workshop5_outputs/workshop5_evidence.png` — confusion matrix and ROC curve

## References

Scikit-learn Developers. (n.d.). *load_breast_cancer*. https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html

UCI Machine Learning Repository. (n.d.). *Breast Cancer Wisconsin (Diagnostic)*. https://archive.ics.uci.edu/dataset/17/breast-cancer-wisconsin-diagnostic
