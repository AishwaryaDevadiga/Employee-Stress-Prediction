# 🏗️ System Architecture - Employee Stress Prediction

## Overview

This document describes the complete architecture of the Employee Stress Prediction System.

## 📊 System Components

```
┌─────────────────────────────────────────────────────────────┐
│         EMPLOYEE STRESS PREDICTION SYSTEM                    │
└─────────────────────────────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼─────┐    ┌──────▼──────┐    ┌─────▼────┐
    │  Data    │    │  Training   │    │ Dashboard│
    │ Pipeline │    │  Pipeline   │    │ (Streamlit)
    └────┬─────┘    └──────┬──────┘    └─────┬────┘
         │                  │                  │
    ┌────▼──────────────────▼──────────────────▼────┐
    │     Trained ML Models (Joblib Pickle)          │
    │                                                 │
    │  - General Model: Decision Tree (99.4%)        │
    │  - Gender-Specific Models (Male/Female)        │
    │  - Multiple algorithms: DT, RF, LR, SVM       │
    └────┬──────────────────┬──────────────────┬────┘
         │                  │                  │
    ┌────▼─────┐    ┌──────▼──────┐    ┌─────▼────┐
    │ Batch    │    │   Single    │    │  Gender- │
    │Predict   │    │ Prediction  │    │ Specific │
    │          │    │             │    │ Predict  │
    └──────────┘    └─────────────┘    └──────────┘
```

## 📁 Directory Structure

### `src/` - Core Modules
```
src/
├── data_loader.py                 # CSV loading functions
├── data_loader_class.py          # OOP wrapper for data loading
├── preprocessing.py               # Data cleaning functions
├── data_preprocessor_class.py    # OOP wrapper for preprocessing
├── feature_engineering.py         # Feature creation functions
├── feature_engineer_class.py     # OOP wrapper for features
├── model_trainer.py              # ML model training (4 models)
├── gender_specific_models.py     # Gender-specific training
├── personalized_models.py        # Gender-specific OOP wrapper
├── prediction.py                 # ManualPredictor, BatchPredictor
├── evaluation.py                 # Model evaluation metrics
├── visualization.py              # Plotting utilities
└── __init__.py
```

### Root Level Files
```
├── train.py                      # Main training orchestrator
├── dashboard.py                  # Streamlit web application
├── requirements_streamlit.txt    # Python dependencies
├── setup_verify.py              # Environment verification
├── QUICK_START.md               # Quick start guide
├── STREAMLIT_README.md          # Detailed documentation
└── ARCHITECTURE.md              # This file
```

### Data Directories
```
├── dataset/
│   └── company_employee_details4999.csv    # Raw data (5000 rows)
├── models/
│   ├── best_general_model.pkl              # Best trained model
│   └── gender_specific/
│       ├── male_decision_tree.pkl
│       ├── male_random_forest.pkl
│       ├── male_logistic_regression.pkl
│       ├── male_svm.pkl
│       ├── female_decision_tree.pkl
│       ├── female_random_forest.pkl
│       ├── female_logistic_regression.pkl
│       └── female_svm.pkl
└── outputs/
    ├── processed_data.csv                 # Final 23-feature dataset
    ├── plots/                             # Generated visualizations
    └── reports/
        ├── model_results.csv              # Performance metrics
        ├── gender_models_summary.txt      # Gender comparison
        └── predictions_{timestamp}.csv    # Batch predictions
```

## 🔄 Data Pipeline

### Stage 1: Data Loading
```
Raw CSV (5000 rows × 11 columns)
    ↓
DataLoader.load_data()
    ↓
DataFrame (5000 rows × 11 columns)
- Columns: employee_id, age, age_when_joined, years_in_company,
  salary, annual_bonus, prior_years_experience, Gender, 
  Resting_Heart_Rate, company, department
```

### Stage 2: Data Preprocessing
```
Raw DataFrame
    ↓
handle_missing_values()     → Remove rows with NaN
    ↓
remove_duplicates()         → Remove duplicate rows (removed 19)
    ↓
encode_gender()             → Male=0, Female=1
    ↓
one_hot_encode()            → company (3 dummies), department (6 dummies)
    ↓
Preprocessed DataFrame (4981 rows × 21 columns)
```

### Stage 3: Feature Engineering
```
Preprocessed DataFrame (21 columns)
    ↓
create_workload_score()
    → Workload_Score = (years_in_company / max_years) * 10
    ↓
create_experience_pressure()
    → Experience_Pressure = max(years_in_company - prior_exp, 0)
    ↓
create_heart_rate_stress()
    → HeartRate_Stress = ((HR - 40) / (200 - 40)) * 10
    ↓
create_stress_score()
    → Stress_Score = 0.4×Workload + 0.3×Experience + 0.3×HeartRate
    ↓
create_stress_level()
    → 0 (Low < 3), 1 (Medium 3-6), 2 (High ≥ 6)
    ↓
Final DataFrame (4981 rows × 23 columns)
Columns: [original 21 + Workload_Score + Experience_Pressure + HeartRate_Stress]
```

### Stage 4: Model Training
```
Final DataFrame (4981 rows × 23 columns)
    ↓
prepare_data()              → Stratified 80/20 split
                             (3984 train, 997 test)
    ↓
train_all_models()
    ├── Logistic Regression  → 85.1% accuracy
    ├── Decision Tree        → 99.4% accuracy ⭐
    ├── Random Forest        → 98.6% accuracy
    └── SVM                  → 46.8% accuracy
    ↓
evaluate_models()           → Accuracy, Precision, Recall, F1
    ↓
save_best_model()          → Decision Tree to models/best_general_model.pkl
```

### Stage 5: Gender-Specific Training
```
Final DataFrame
    ↓
Split by Gender (Gender column)
    ├── Male data (2600 samples)
    └── Female data (2400 samples)
    ↓
For each gender:
    ├── Train 4 models (DT, RF, LR, SVM)
    ├── Evaluate on test set
    └── Save gender_specific/*.pkl
    ↓
Gender-Specific Models (8 total)
```

## 🤖 Model Architecture

### General Models
```
Input Features (21):
├── Demographic: age, age_when_joined, years_in_company
├── Financial: salary, bonus
├── Experience: prior_experience
├── Medical: Gender, Resting_Heart_Rate
├── Categorical: company (3 dummies), department (6 dummies)
└── Engineered: Workload_Score, Experience_Pressure, HeartRate_Stress

↓ (Processed through models)

Output (3 classes):
├── 0: Low Stress (🟢)
├── 1: Medium Stress (🟡)
└── 2: High Stress (🔴)
```

### Model Details

| Model | Type | Best For | Accuracy | Training Time |
|-------|------|----------|----------|---------------|
| Decision Tree | Tree | Interpretability | 99.4% | Fast |
| Random Forest | Ensemble | Robustness | 98.6% | Moderate |
| Logistic Regression | Linear | Baseline | 85.1% | Fast |
| SVM | Kernel | Complex patterns | 46.8% | Slow |

## 🎯 Prediction Workflows

### Single Prediction Flow
```
User Input (21 features)
    ↓
Feature Validation
    ↓
Load best_general_model.pkl
    ↓
model.predict(features)
    ↓
Prediction (0/1/2) + Probabilities
    ↓
HR Recommendation
    ↓
Display Result
```

### Batch Prediction Flow
```
CSV Upload (N employees)
    ↓
Load & Validate
    ↓
For each employee:
    ├── Extract 21 features
    ├── Predict using model
    ├── Get probabilities
    └── Store result
    ↓
Results DataFrame (N × 24 columns)
    ├── Original features
    ├── Predicted stress level
    ├── Stress category (Low/Medium/High)
    └── Confidence score
    ↓
Download CSV
```

### Gender-Specific Prediction Flow
```
Employee Input + Gender
    ↓
Select gender model directory
    ↓
Load specific gender model
    ↓
model.predict(features)
    ↓
Gender-Specific Prediction
    ↓
Compare with general model
```

## 🎨 Streamlit Dashboard Architecture

```
Streamlit App
├── Session State Management
│   ├── Load models (cached)
│   ├── Load data (cached)
│   └── Cache refresh on update
│
├── Sidebar Navigation
│   ├── Page selector
│   ├── Help information
│   └── Model status
│
├── Pages (5 tabs)
│   ├── Dashboard
│   │   ├── KPI cards
│   │   ├── Stress distribution chart
│   │   ├── Age/HR scatter
│   │   ├── Gender distribution
│   │   └── Salary/Workload correlation
│   │
│   ├── Analytics
│   │   ├── Feature distributions
│   │   ├── Correlation heatmap
│   │   ├── Gender comparison
│   │   └── Department analysis
│   │
│   ├── Predictions
│   │   ├── Single Prediction
│   │   │   ├── Input form
│   │   │   ├── Feature calculations
│   │   │   └── Result display
│   │   │
│   │   └── Batch Prediction
│   │       ├── CSV uploader
│   │       ├── Validation
│   │       └── Results download
│   │
│   ├── Employee Search
│   │   ├── Search by ID
│   │   ├── Filter by stress
│   │   └── Risk detection
│   │
│   └── Reports
│       ├── Generate reports
│       ├── Export data
│       └── Model info
│
└── Visualizations
    ├── Plotly charts (interactive)
    ├── Matplotlib plots
    └── Seaborn heatmaps
```

## 💾 Data Persistence

### Model Serialization
```
Training Process:
  Best Model → joblib.dump() → best_general_model.pkl
  
Usage Process:
  best_general_model.pkl → joblib.load() → Ready to predict
```

### CSV Exports
```
Operations:
  Predictions → CSV export
  Reports → TXT export
  Batch results → CSV download
```

## 🔒 Data Flow Security

```
User Input
    ↓
Validation (range checks, type checks)
    ↓
Feature Engineering (local)
    ↓
Model Prediction (local)
    ↓
Result Display (in-memory)
    ↓
Optional: Export to CSV (user choice)
```

No data is sent to external servers. All processing is local.

## 📊 Performance Metrics

### Model Performance
- **Decision Tree**: 99.4% accuracy (best)
- **Random Forest**: 98.6% accuracy
- **Cross-validation**: 5-fold, consistent scores
- **Inference Time**: <10ms per prediction

### System Performance
- **Dashboard Load**: ~2-3 seconds (cached)
- **Prediction**: <100ms
- **Batch Processing**: <5 seconds for 100 employees
- **Memory Usage**: <200MB

## 🔄 Deployment Architecture

### Local Development
```
User PC
├── Python 3.7+
├── Virtual Environment
├── Streamlit (port 8501)
└── All data/models local
```

### Production Considerations
```
Could be deployed to:
├── Heroku
├── AWS EC2
├── Google Cloud Run
├── Docker Container
└── Corporate Server
```

## 🔌 Integration Points

### External Integrations (Optional)
```
Database:
  CSV → SQLite/PostgreSQL
  
API:
  Streamlit → REST API (add FastAPI)
  
Authentication:
  Add OAuth/SSO support
  
Monitoring:
  Add logging/telemetry
```

## 📈 Scalability

### Current Architecture
- Supports 5,000-10,000 employees
- Real-time predictions
- Interactive dashboard

### Scaling Options
```
For larger datasets:
├── Use database instead of CSV
├── Implement caching layer
├── Add async processing
├── Distribute models across servers
└── Use cloud storage
```

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.7+ |
| Data | Pandas | 2.0+ |
| ML | Scikit-Learn | 1.0+ |
| Viz | Plotly/Matplotlib | Latest |
| UI | Streamlit | 1.15+ |
| Serialization | Joblib | 1.1+ |

## 📝 Future Enhancements

```
Short-term:
├── Add more ML models (XGBoost, LightGBM)
├── Implement SHAP for explainability
├── Add real-time monitoring
└── Database integration

Medium-term:
├── Web API with FastAPI
├── Authentication system
├── Role-based access
└── Audit logging

Long-term:
├── Deep learning models
├── Real-time streaming
├── Mobile app
└── Enterprise deployment
```

---

**Last Updated**: 2024  
**System Version**: 1.0  
**Architecture Pattern**: Modular ML Pipeline

