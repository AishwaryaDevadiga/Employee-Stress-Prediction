# 🧠 Employee Stress Prediction System

An **industry-level HR Analytics platform** that predicts employee stress levels using Machine Learning and provides an interactive Streamlit dashboard for real-time insights.

## 🎯 Project Overview

This system combines advanced ML models with an intuitive UI to:
- **Predict** employee stress levels (Low, Medium, High)
- **Analyze** employee wellness metrics
- **Generate** HR recommendations
- **Track** stress trends across departments and demographics
- **Support** data-driven HR decisions

## 📊 Key Features

### 1. **Machine Learning Models**
- ✅ Logistic Regression
- ✅ Decision Tree (Best: 99.4% accuracy)
- ✅ Random Forest
- ✅ Support Vector Machine
- ✅ Gender-Specific Models for targeted predictions

### 2. **Interactive Dashboard**
- 📊 Real-time analytics with Plotly charts
- 🎯 Employee search and filtering
- 👥 Gender-wise analysis
- 📈 Stress distribution visualization
- 💼 Department analytics

### 3. **Prediction Capabilities**
- 🔮 Single employee stress prediction
- 📁 Batch prediction from CSV files
- 💾 Export predictions with recommendations

### 4. **HR Analytics**
- 📋 Comprehensive reports
- 🎓 Risk assessment and categorization
- 💡 Personalized HR recommendations
- 📥 CSV and report export

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-Learn, Joblib |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Dashboard** | Streamlit |
| **Data Format** | CSV |

## 📁 Project Structure

```
Employee_Stress_Prediction/
│
├── dataset/
│   └── company_employee_details4999.csv    # Raw employee data
│
├── models/
│   ├── best_general_model.pkl             # Best trained model
│   └── gender_specific/                   # Gender-specific models
│       ├── male_decision_tree.pkl
│       └── female_decision_tree.pkl
│
├── outputs/
│   ├── plots/                             # Generated visualizations
│   └── reports/                           # Analysis reports
│       ├── model_results.csv
│       └── gender_models_summary.txt
│
├── src/
│   ├── data_loader.py                     # Load and explore data
│   ├── preprocessing.py                   # Data cleaning
│   ├── feature_engineering.py             # Feature creation
│   ├── model_training.py                  # Train ML models
│   ├── evaluation.py                      # Model evaluation
│   ├── personalized_models.py             # Gender-specific models
│   └── prediction.py                      # Make predictions
│
├── train.py                               # Training script
├── dashboard.py                           # Streamlit dashboard
├── requirements.txt                       # Dependencies
└── README.md                              # This file
```

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements_streamlit.txt
```

### Step 2: Train Models
```bash
python train.py
```

This will:
- Load and preprocess the dataset
- Engineer features
- Train all ML models
- Save best models to `models/`
- Generate reports to `outputs/reports/`

**Output:**
```
✓ Dataset loaded successfully!
✓ Data split completed!
✓ Trained Logistic Regression
✓ Trained Decision Tree
✓ Trained Random Forest
✓ Trained SVM
✓ All models trained successfully!
✓ Best model saved: Decision Tree
```

### Step 3: Launch Dashboard
```bash
streamlit run dashboard.py
```

Opens at: `http://localhost:8501`

## 📊 Feature Engineering

### Calculated Features

```python
Workload_Score = (Years_in_Company / Max_Years) * 10

Experience_Pressure = max(Years_in_Company - Prior_Experience, 0)

HeartRate_Stress = ((Resting_Heart_Rate - 40) / (200 - 40)) * 10

Stress_Score = 0.4*Workload + 0.3*Experience + 0.3*HeartRate
```

### Stress Levels

| Level | Score | Status | Action |
|-------|-------|--------|--------|
| **Low** | 0-3 | ✅ Healthy | Monitor regularly |
| **Medium** | 3-6 | ⚠️ Caution | Intervention needed |
| **High** | 6-10 | 🚨 Alert | Immediate action |

## 🎯 Dashboard Sections

### 1. **Dashboard (📊)**
- Overview metrics
- Stress distribution pie chart
- Age vs Heart Rate scatter
- Gender distribution
- Salary vs Workload analysis

### 2. **Analytics (📈)**
- Feature distributions
- Correlation heatmap
- Gender-wise analysis
- Department breakdown

### 3. **Predictions (🔮)**
- Single employee prediction form
- Batch CSV upload and prediction
- Probability distribution
- HR recommendations

### 4. **Employee Search (👥)**
- Search by Employee ID
- Filter by Stress Level
- Department-wise search
- Risk categorization

### 5. **Reports (📋)**
- Generate summary reports
- Export dataset (CSV)
- Model information
- Performance metrics

## 🤖 Model Information

### Models Trained
- **Logistic Regression** - Baseline model
- **Decision Tree** - Best performer (99.4% accuracy)
- **Random Forest** - Ensemble approach
- **SVM** - Support Vector Machine

### Performance Metrics
- **Accuracy**: ~99%
- **Precision**: High
- **Recall**: High
- **F1-Score**: High
- **Cross-Validation**: 5-fold

### Gender-Specific Models
- **Male Model**: Optimized for male employees
- **Female Model**: Optimized for female employees
- Separate training data per gender
- Tailored feature importance

## 📈 Data Insights

### Dataset Statistics
- **Total Employees**: 5,000
- **Features**: 21 (after engineering)
- **Target Variable**: Stress_Level (0=Low, 1=Medium, 2=High)

### Stress Distribution (Example)
- Low Stress: ~35%
- Medium Stress: ~45%
- High Stress: ~20%

## 💡 HR Recommendations

### For Low Stress Employees ✅
- ✓ Recognize and reward performance
- ✓ Continue current arrangements
- ✓ Regular check-ins

### For Medium Stress Employees ⚠️
- • Reduce workload
- • Offer wellness programs
- • Schedule meetings
- • Flexible arrangements
- • Work-life balance check

### For High Stress Employees 🚨
- ! Urgent HR meeting
- ! Mental health counseling
- ! Temporary workload reduction
- ! Mentoring opportunities
- ! Role review and adjustment

## 📥 Import/Export Features

### Batch Prediction
1. Prepare CSV with columns: `age`, `gender`, `salary`, `years_in_company`, etc.
2. Upload via dashboard
3. Get predictions for all employees
4. Download results with stress levels

### Report Export
- Summary reports (TXT)
- Full dataset (CSV)
- Model results (CSV)
- Visualizations (PNG/HTML)

## 🔧 Configuration

### Model Parameters
Edit `src/model_training.py`:
```python
# Random Forest
n_estimators=100
max_depth=15

# SVM
kernel='rbf'
gamma='scale'
```

### Feature Engineering
Edit `src/feature_engineering.py`:
```python
# Adjust weights
Stress_Score = 0.4*Workload + 0.3*Experience + 0.3*HeartRate
```

## 🐛 Troubleshooting

### Models not loading?
```bash
# Retrain models
python train.py
```

### Dashboard crashes?
```bash
# Clear cache
streamlit cache clear

# Restart
streamlit run dashboard.py
```

### Import errors?
```bash
# Reinstall dependencies
pip install -r requirements_streamlit.txt --force-reinstall
```

## 📊 Sample Usage

### Single Prediction
1. Go to **Predictions** tab
2. Fill employee details
3. Click "🔮 Predict Stress Level"
4. View result + recommendations

### Batch Analysis
1. Create CSV with employee data
2. Upload to dashboard
3. Click "🚀 Predict for All Employees"
4. Download results

### Employee Search
1. Go to **Employee Search** tab
2. Select search type (ID / Stress Level / Department)
3. View matching employees
4. Export if needed

## 🎓 Learning Outcomes

By using this system, you'll learn:
- ✅ ML model training and evaluation
- ✅ Feature engineering techniques
- ✅ Streamlit dashboard development
- ✅ Data visualization with Plotly
- ✅ Model deployment
- ✅ HR analytics insights

## 📝 Code Quality

- ✅ **Modular**: Separate files for each functionality
- ✅ **Documented**: Comprehensive docstrings
- ✅ **Type Hints**: Clear parameter types
- ✅ **Error Handling**: Graceful error messages
- ✅ **Comments**: Inline explanations

## 🔐 Data Privacy

- No personal data stored on disk (except dataset)
- Models are trained locally
- No external API calls
- Results can be cleared anytime

## 📞 Support

For issues or improvements:
1. Check error messages
2. Review README
3. Check source code comments
4. Run training again if needed

## 📄 License

This project is provided as-is for educational and professional use.

## 🎉 Next Steps

1. **Run training**: `python train.py`
2. **Launch dashboard**: `streamlit run dashboard.py`
3. **Explore data**: Check Dashboard tab
4. **Make predictions**: Use Predictions tab
5. **Generate reports**: Export from Reports tab

---

**🚀 Ready to get started?**

```bash
# Install packages
pip install -r requirements_streamlit.txt

# Train models
python train.py

# Launch dashboard
streamlit run dashboard.py
```

Then open `http://localhost:8501` in your browser! 🎯

