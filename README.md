# Parkinson's Disease Classification from Voice Features

Final project for the **Mathematics of Machine Learning** course at the **Universidad Nacional de Colombia**.

## Overview

This project investigates how increasing model complexity and nonlinearity affects the ability of machine learning models to detect **Parkinson's disease** from acoustic voice measurements.

Instead of focusing only on predictive accuracy, the project analyzes the tradeoff between **interpretability, complexity, and generalization**, comparing linear and nonlinear classifiers under a validation strategy that avoids patient-level data leakage.

> **Research question:**  
> Does introducing nonlinearity and greater model complexity improve the generalization ability of classification models for detecting Parkinson's disease from voice features?

---

## Dataset

The project uses the **Parkinsons** dataset from the **UCI Machine Learning Repository**.

**Dataset characteristics**

- 195 voice recordings
- 32 patients
- 22 acoustic features
- Binary classification
  - `0` Healthy
  - `1` Parkinson's disease

Since each patient has multiple recordings, observations are **not independent**. This motivated the use of a grouped validation strategy.

<AsyncImage query="UCI Parkinsons dataset voice features machine learning" aspectRatio="16:9" maxHeight=420/>

---

## Methodology

### Exploratory Data Analysis

- Dataset inspection
- Missing-value verification
- Class distribution analysis
- Feature distribution visualization
- Correlation analysis
- Comparison between healthy and Parkinson patients

### Preprocessing

Features were standardized using z-score normalization.

The scaler was fitted **only on training folds** to prevent data leakage.

### Validation Strategy

A key aspect of the project was using:

> **StratifiedGroupKFold (4 folds)**

This ensures that:

- recordings from the same patient never appear in both training and testing,
- class proportions remain balanced across folds,
- evaluation better reflects real-world generalization.

---

## Models Evaluated

The following models were implemented and compared:

- Logistic Regression
- Linear SVM
- RBF SVM
- Optimized RBF SVM
- Random Forest

### Hyperparameter Optimization

For the RBF SVM, a grid search was performed over:

- `C`
- `gamma`

Best parameters:

```text
C = 1
gamma = 0.01
```

---

## Project Workflow

<AsyncImage query="machine learning workflow diagram preprocessing cross validation model training evaluation" aspectRatio="16:9" maxHeight=420/>

1. Load and inspect the dataset.
2. Perform exploratory data analysis.
3. Standardize features.
4. Split data using `StratifiedGroupKFold`.
5. Train multiple classification models.
6. Optimize the RBF SVM.
7. Compare performance and interpretability.

---

## Technologies

- Python
- NumPy
- Pandas
- Scikit-learn
- Matplotlib
- Jupyter Notebook

---

## Repository Structure

```text
.
├── notebooks/
├── data/
├── models/
├── figures/
├── requirements.txt
└── README.md
```

*(Adjust the structure if your repository differs.)*

---

## Key Takeaways

- Proper validation is essential when multiple samples belong to the same subject.
- Nonlinear models can improve predictive performance, but increased complexity should be balanced against interpretability.
- Preventing data leakage through grouped cross-validation produces more reliable estimates of real-world performance.

