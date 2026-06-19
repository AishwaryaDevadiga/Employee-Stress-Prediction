# 🚀 Quick Start Guide - Employee Stress Prediction System

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements_streamlit.txt
```

### Step 2: Train Models (First Time Only)
```bash
python train.py
```

**Expected Output:**
```
======================================================================
EMPLOYEE STRESS PREDICTION SYSTEM - MODEL TRAINING
======================================================================
✓ Directories created/verified
✓ Dataset loaded successfully!
  Shape: (5000, 11)
✓ Data preprocessing completed
✓ Feature engineering completed
✓ Trained Logistic Regression
✓ Trained Decision Tree
✓ Trained Random Forest  
✓ Trained SVM
✓ Best model saved: Decision_Tree
✓ Trained gender-specific models
======================================================================
✅ TRAINING COMPLETED SUCCESSFULLY!
======================================================================
```

**This creates:**
- `models/best_general_model.pkl` - Main prediction model
- `models/gender_specific/` - Gender-specific models
- `outputs/processed_data.csv` - Full dataset with features
- `outputs/reports/` - Model evaluation reports

### Step 3: Launch Dashboard
```bash
streamlit run dashboard.py
```

**Opens in browser:**
```
http://localhost:8501
```

---

## 📊 Dashboard Navigation

### 1. **📊 Dashboard** (Home)
- Overall metrics cards
- Stress distribution chart
- Employee analytics
- Age and salary correlations

### 2. **📈 Analytics**
- Feature distributions
- Correlation heatmap
- Gender-wise comparison
- Department analysis

### 3. **🔮 Predictions**
- **Single Prediction:** Predict one employee
- **Batch Prediction:** Upload CSV with 10+ employees

### 4. **👥 Employee Search**
- Search by ID
- Filter by stress level
- Find high-risk employees

### 5. **📋 Reports**
- Download summary reports
- Export full dataset
- View model metrics

---

## 🎯 Example Workflows

### Workflow 1: Check Overall Health
1. Go to **Dashboard** tab
2. Review stress distribution pie chart
3. Check high-risk count

### Workflow 2: Predict Single Employee
1. Go to **Predictions** > **Single Prediction**
2. Fill in employee details:
   - Age: 35
   - Gender: Male
   - Years in Company: 5
   - Prior Experience: 3
   - Salary: 75000
   - Bonus: 8000
   - Heart Rate: 72
3. Click **🔮 Predict Stress Level**
4. View result and recommendations

### Workflow 3: Batch Prediction
1. Create CSV file with employees:
```
age,gender,years_in_company,prior_experience,salary,bonus,heart_rate
35,Male,5,3,75000,8000,72
28,Female,2,1,55000,5000,68
45,Male,15,10,95000,12000,78
```
2. Go to **Predictions** > **Batch Prediction**
3. Upload CSV
4. Click **🚀 Predict for All Employees**
5. Download results with predictions

### Workflow 4: Risk Assessment
1. Go to **Employee Search**
2. Select "Stress Level" filter
3. Choose "High"
4. View all high-risk employees
5. Export for HR review

---

## 📁 File Structure

```
d:\MCA project\
├── dataset/
│   └── company_employee_details4999.csv
├── models/
│   ├── best_general_model.pkl
│   └── gender_specific/
├── outputs/
│   ├── processed_data.csv
│   ├── plots/
│   └── reports/
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── data_preprocessor_class.py
│   ├── feature_engineering.py
│   ├── feature_engineer_class.py
│   ├── model_trainer.py
│   ├── gender_specific_models.py
│   ├── personalized_models.py
│   ├── prediction.py
│   ├── evaluation.py
│   └── visualization.py
├── train.py
├── dashboard.py
├── requirements_streamlit.txt
└── STREAMLIT_README.md
```

---

## 🔧 Troubleshooting

### Issue: "Models not found"
**Solution:** Run `python train.py` again

### Issue: "ModuleNotFoundError"
**Solution:** 
```bash
pip install -r requirements_streamlit.txt --force-reinstall
```

### Issue: "Port 8501 already in use"
**Solution:**
```bash
streamlit run dashboard.py --server.port 8502
```

### Issue: Dataset not found
**Ensure:** `dataset/company_employee_details4999.csv` exists

---

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Decision Tree | 99.4% | 98.5% | 99.4% | 98.9% |
| Random Forest | 98.6% | 97.8% | 98.6% | 98.2% |
| Logistic Regression | 85.1% | 84.2% | 85.1% | 84.6% |
| SVM | 46.8% | 45% | 46.8% | 44.2% |

**Best Model:** Decision Tree ⭐

---

## 💡 Tips & Tricks

### Faster Dashboard Loading
- After training, models are cached
- First load takes ~5 seconds
- Subsequent loads are instant

### Export Data
1. Go to **Reports** tab
2. Click **📥 Download Dataset**
3. Get CSV with all 23 features

### Check Model Training
```bash
# View training logs
cat outputs/reports/model_results.csv

# View gender comparison
cat outputs/reports/gender_models_summary.txt
```

### Retrain Models
```bash
# Remove old models
rmdir models/gender_specific
rm models/best_general_model.pkl

# Retrain
python train.py
```

---

## 🎓 Understanding the System

### Stress Levels
- **🟢 Low (0):** Healthy, normal stress
- **🟡 Medium (1):** Requires monitoring
- **🔴 High (2):** Needs intervention

### Key Features Used
- Age, salary, heart rate
- Years in company, experience
- Company and department
- **5 engineered features:**
  - Workload_Score
  - Experience_Pressure
  - HeartRate_Stress
  - Stress_Score
  - Stress_Level (target)

### Prediction Formula
```
Stress_Score = 0.4×Workload + 0.3×Experience + 0.3×HeartRate

Then: 
- Score < 3 → Low
- 3 ≤ Score < 6 → Medium
- Score ≥ 6 → High
```

---

## 📞 Support

**If something doesn't work:**
1. Check error message
2. Run `python train.py` again
3. Restart dashboard: `Ctrl+C` then `streamlit run dashboard.py`
4. Verify dataset exists in `dataset/` folder
5. Check Python version: `python --version` (should be 3.7+)

---

## ✨ Features Included

✅ Interactive web dashboard  
✅ Single and batch predictions  
✅ Gender-specific models  
✅ Real-time analytics  
✅ Employee search  
✅ Risk detection  
✅ HR recommendations  
✅ Report export (CSV)  
✅ Model comparison  
✅ Feature importance  

---

**Ready to go!** 🚀

```bash
python train.py && streamlit run dashboard.py
```

