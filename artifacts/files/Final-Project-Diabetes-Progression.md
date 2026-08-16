# Final Project: Predicting Diabetes Disease Progression with Real Patient Data

## Project overview

This final project uses the real diabetes regression dataset distributed with scikit-learn. The dataset contains 442 patient observations, ten standardized baseline variables, and a quantitative measure of disease progression one year later. According to the scikit-learn documentation, the data originated from a diabetes study reported by Efron et al. (2004). I selected this dataset because it supports a complete, reproducible regression workflow while also requiring careful limits on interpretation.

## Objective and audience

My objective was to compare a transparent linear model with a nonlinear ensemble, select a model using training evidence, and evaluate it once on an untouched test set. The intended audience includes AI/ML employers, technical reviewers, security leaders, and healthcare stakeholders who want to see both the technical evidence and my judgment about responsible use.

## Method

I first saved the complete 442-record dataset as a CSV so the exact input can be inspected. I separated 20% of the observations as an untouched test set using a fixed random seed. On the remaining training data, I compared Ridge regression and a random forest through five-fold shuffled cross-validation. Mean absolute error (MAE) was the main selection measure because it expresses the typical prediction error in the same units as the target. I also recorded the coefficient of determination (R-squared) to describe explained variation. After choosing the model with the lower cross-validated MAE, I fitted it to all training records and evaluated it once on the test set.

## Evidence and interpretation

The downloadable evidence includes the exact data snapshot, Python source, cross-validation comparison, final test metrics, row-level predictions, console output, and a two-panel chart. The left panel compares cross-validated MAE across the candidate models. The right panel compares actual and predicted progression on the untouched test set, with the diagonal line representing perfect predictions. These files make the model-selection decision traceable and allow another reviewer to reproduce the analysis.

This analysis should not be interpreted as a clinical tool. A model can show useful statistical performance and still be inappropriate for diagnosis, treatment, or resource allocation. The dataset is small, the variables are standardized, and the available fields do not support a complete analysis of demographic fairness, clinical workflow, calibration, or changing populations. Before real use, the work would require external validation, clinical review, subgroup evaluation, privacy and security controls, documentation of intended and excluded uses, human oversight, and continuous monitoring.

## Conclusion

The final project demonstrates my ability to move from real-data provenance through reproducible model comparison and untouched evaluation to responsible communication. It also reflects a broader leadership lesson from the course: technical evidence should inform a decision, but accountability remains with people who understand the context, risks, and limitations.

## References

Efron, B., Hastie, T., Johnstone, I., & Tibshirani, R. (2004). Least angle regression. *The Annals of Statistics, 32*(2), 407-499. https://doi.org/10.1214/009053604000000067

scikit-learn developers. (2026). *Diabetes dataset*. https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset
