# Employee Stress Prediction - Machine Learning Project

A comprehensive machine learning project for predicting employee stress levels based on various employee attributes and health metrics.

## 📋 Project Overview

This project implements a complete ML pipeline to predict employee stress levels using multiple classification algorithms. The model helps organizations identify employees at risk of high stress and implement targeted interventions.

## 📁 Project Structure

```
Employee Stress Prediction/
├── dataset/
│   └── company_employee_details4999.csv   # Input dataset
├── src/
│   ├── data_loader.py                     # Data loading and exploration
│   ├── preprocessing.py                   # Data cleaning and encoding
│   ├── feature_engineering.py             # Feature creation
│   ├── model_trainer.py                   # Model training and evaluation
│   ├── visualization.py                   # Plot generation
│   └── predictor.py                       # Prediction functions
├── models/
│   └── best_stress_model.pkl              # Trained model (generated)
├── outputs/
│   ├── plots/                             # Generated visualizations
│   └── results/                           # Model reports and metrics
├── main.py                                # Main pipeline orchestrator
├── requirements.txt                       # Project dependencies
└── README.md                              # This file
```

## 🔧 Installation

1. **Clone or download the project**

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Dataset

**File:** `dataset/company_employee_details4999.csv`

**Expected Columns:**
- `Gender` - Employee gender (Male/Female)
- `company` - Company name
- `department` - Department
- `years_in_the_company` - Years employed
- `prior_years_experience` - Previous work experience
- `Resting_Heart_Rate` - Resting heart rate (bpm)
- Other employee attributes

## 🚀 Running the Pipeline

```bash
python main.py
```

The script will execute all 11 steps:
1. Create output directories
2. Load dataset
3. Exploratory data analysis
4. Data preprocessing
5. Feature engineering
6. Model training
7. Model evaluation
8. 5-fold cross-validation
9. Visualization generation
10. Results saving
11. Report generation

## 🔄 Pipeline Steps

### Step 1: Data Loading & Exploration
- Loads the CSV dataset
- Displays shape, columns, data types
- Shows first 5 rows
- Identifies missing values and duplicates

### Step 2: Data Preprocessing
- Removes duplicate rows
- Handles missing values
- **Gender Encoding:** Male = 0, Female = 1
- **One-Hot Encoding:** Company and department columns

### Step 3: Feature Engineering

**Created Features:**

1. **Workload_Score**
   ```
   = (years_in_the_company / max(years_in_the_company)) * 10
   ```

2. **Experience_Pressure**
   ```
   = max(years_in_company - prior_years_experience, 0)
   ```

3. **HeartRate_Stress**
   ```
   = ((Resting_Heart_Rate - min_hr) / (max_hr - min_hr)) * 10
   ```

4. **Stress_Score**
   ```
   = 0.4 * Workload_Score +
     0.3 * Experience_Pressure +
     0.3 * HeartRate_Stress
   ```

5. **Stress_Level** (Target Variable)
   - Low: if score < 3
   - Medium: if score < 6
   - High: if score ≥ 6

### Step 4: Model Training

**Models Trained:**
1. Logistic Regression
2. Decision Tree
3. Random Forest
4. Support Vector Machine (SVM)

**Data Split:**
- Training: 80%
- Testing: 20%
- Stratified split to maintain class distribution
- Random seed: 42

### Step 5: Model Evaluation

**Metrics Calculated:**
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Classification Report

### Step 6: Cross-Validation

- 5-fold cross-validation on all models
- Helps assess model stability and generalization

## 📈 Outputs

### Models
- `models/best_stress_model.pkl` - Best performing model

### Visualizations (in `outputs/plots/`)
- `accuracy_comparison.png` - Bar chart of model accuracies
- `confusion_matrices.png` - Confusion matrices for all models
- `feature_importance.png` - Top 15 feature importance (Random Forest)
- `stress_distribution.png` - Stress score and level distributions

### Reports (in `outputs/results/`)
- `model_summary.txt` - Summary of all models
- `{model_name}_classification_report.txt` - Detailed reports for each model

### Data
- `outputs/processed_data.csv` - Preprocessed and engineered features

## 🎯 Making Predictions

### Method 1: Using the Trained Model

```python
from src.predictor import ManualPredictor

# Load the model
predictor = ManualPredictor('models/best_stress_model.pkl')

# Predict for new sample
features = [5.2, 3.1, 0.8, 4.5, 6.2, 2.1]  # Example values
result = predictor.predict_with_probability(features)

print(f"Stress Level: {result['stress_level']}")
print(f"Confidence: {result['confidence']:.4f}")
```

### Method 2: Batch Prediction

```python
from src.predictor import batch_predict

# Predict for multiple samples
predictions = batch_predict('models/best_stress_model.pkl', X_test_data)
```

### Method 3: Interactive Prediction

```python
from src.predictor import ManualPredictor

predictor = ManualPredictor('models/best_stress_model.pkl', 
                           feature_names=['Feature1', 'Feature2', ...])
predictor.interactive_prediction()
```

## 📦 Dependencies

- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning
- **matplotlib** - Plotting
- **seaborn** - Statistical visualization
- **joblib** - Model serialization

## 🔍 Key Results

The pipeline compares 4 different algorithms and identifies the best performer. Random Forest typically shows strong performance due to its ensemble nature and ability to capture non-linear relationships.

## 💡 Tips for Improvement

1. **Feature Engineering:** Consider adding more domain-specific features
2. **Hyperparameter Tuning:** Use GridSearchCV for optimal parameters
3. **Class Imbalance:** If data is imbalanced, consider SMOTE or class weights
4. **Model Stacking:** Combine predictions from multiple models
5. **Cross-Validation:** Use k-fold cross-validation for better evaluation

## 📝 Notes

- Ensure the dataset file is in the correct location before running
- Run the script from the project root directory
- All output files are automatically saved in appropriate directories
- The best model is automatically selected based on accuracy

## 🐛 Troubleshooting

**FileNotFoundError:**
- Check dataset path: `dataset/company_employee_details4999.csv`
- Ensure you're in the project root directory

**Missing Dependencies:**
```bash
pip install -r requirements.txt
```

**Memory Issues (large datasets):**
- Process data in batches
- Use feature selection to reduce dimensionality

## 📧 Contact & Support

For questions or issues, please refer to the project documentation or contact the development team.

---

**Last Updated:** June 2024
**Version:** 1.0
