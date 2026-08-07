# Workshop 4: Real-Data Quality Audit and Responsible Preprocessing

## Artifact purpose

This artifact provides executable evidence of data-quality analysis using the real Wisconsin Diagnostic Breast Cancer dataset. The source contains 569 observations, 30 numeric features, and two diagnostic classes. Features were computed from digitized images of fine-needle aspirates of breast masses (UCI Machine Learning Repository, n.d.). This project is educational and is not a clinical diagnostic system.

## Why this dataset was selected

The dataset is a recognized binary-classification resource with clear provenance. Scikit-learn distributes a copy originating from the UCI Machine Learning Repository and documents 212 malignant and 357 benign observations (Scikit-learn Developers, n.d.). Loading it through `load_breast_cancer()` makes the analysis reproducible without requiring a Kaggle account or an unofficial dataset mirror.

## Evidence-producing process

The original dataset has no missing values, so controlled defects were added only to a copy of the training data. The untouched test set was never modified. The controlled defects included 37 missing values, eight duplicate rows, and extreme values in selected features. This approach permits a reproducible cleaning demonstration without claiming that the original UCI records contained those problems.

The cleaning workflow removed exact duplicates, capped numeric values using the 1st and 99th percentiles learned from training data, and placed median imputation and standardization inside a scikit-learn pipeline. Logistic regression used balanced class weights because the classes are not evenly distributed. Performance was measured on the same untouched test set before and after cleaning.

## Measured data-quality results

| Quality check | Before cleaning | After cleaning |
|---|---:|---:|
| Missing values | 37 | 0 |
| Duplicate rows | 8 | 0 |
| Values outside learned caps | 34 | 0 |

## Model-impact results

| Training input | Accuracy | Malignant precision | Malignant recall | Malignant F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Controlled defects | 0.9720 | 0.9804 | 0.9434 | 0.9615 | 0.9958 |
| Cleaned training data | 0.9720 | 0.9804 | 0.9434 | 0.9615 | 0.9962 |

The similarity of the classification metrics is itself an honest result. It shows that a robust pipeline and this relatively separable dataset limited the effect of the controlled defects. Cleaning still removed measurable quality problems, produced a documented training set, and slightly improved ROC-AUC. The artifact does not exaggerate the improvement.

## Bias, privacy, and leadership analysis

The dataset does not include demographic variables. Therefore, this analysis cannot test demographic fairness and does not claim that performance is equal across populations. That limitation is important because an overall metric cannot establish fairness for groups that are not represented or identified. A responsible leader should require representative external validation, privacy review, clinical review, data lineage, access controls, and monitoring before considering a healthcare use.

The leadership value of the artifact is its transparent evidence chain: source data, controlled defects, cleaning decisions, code, audit CSV, model metrics, and a visual output are all available. This supports informed discussion rather than asking stakeholders to accept a theoretical description.

## Included evidence files

- `responsible_data_pipeline.py` — reproducible analysis code
- `workshop4_outputs/real_dataset_snapshot.csv` — dataset used by the analysis
- `workshop4_outputs/data_quality_audit.csv` — before-and-after audit counts
- `workshop4_outputs/model_impact_metrics.csv` — measured evaluation results
- `workshop4_outputs/run_output.txt` — recorded console evidence
- `workshop4_outputs/workshop4_evidence.png` — generated results visualization

## References

Scikit-learn Developers. (n.d.). *load_breast_cancer*. https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html

UCI Machine Learning Repository. (n.d.). *Breast Cancer Wisconsin (Diagnostic)*. https://archive.ics.uci.edu/dataset/17/breast-cancer-wisconsin-diagnostic
