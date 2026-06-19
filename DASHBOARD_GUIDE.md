# 🎯 How to Run with Web Dashboard

## Quick Start (3 Simple Steps)

### **Option 1: Automatic (Recommended)**

#### On Windows (PowerShell):
```powershell
cd "d:\MCA project"
.\start.bat
```

Then open your browser and go to: **http://localhost:5000/dashboard**

---

### **Option 2: Manual Steps**

#### Step 1: Start the API Server
```bash
cd "d:\MCA project"
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

#### Step 2: Open the Dashboard
Open your web browser and go to:
```
http://localhost:5000/dashboard
```

Or open the file directly:
```
d:\MCA project\dashboard.html
```

---

## 🎨 Dashboard Features

### **Single Prediction**
- Enter employee details
- Choose prediction model (General, Male-Specific, Female-Specific)
- Get instant stress level prediction with confidence score
- See probability distribution for all stress levels

### **Batch Prediction**
- Predict stress for multiple employees at once
- Configure batch size (2, 3, 5, or 10 employees)
- See results side-by-side

### **Compare Models**
- See how different models predict for the same employee
- Compare General vs Male-Specific vs Female-Specific models
- Easy A/B testing

### **System Status**
- Real-time API health monitoring
- View loaded models
- Stress level definitions
- Model accuracy information

---

## 📊 What to Enter

Here's sample data you can use:

### **Low Stress Employee**
- Gender: 0 (Male)
- Age: 25
- Years in Company: 2
- Prior Experience: 3
- Salary: 50000
- Basic Salary: 5000
- Heart Rate: 70
- Company: 0

### **High Stress Employee**
- Gender: 1 (Female)
- Age: 45
- Years in Company: 8
- Prior Experience: 5
- Salary: 80000
- Basic Salary: 8000
- Heart Rate: 95
- Company: 2

---

## 🚀 Features

✅ **Beautiful Modern UI** - Clean, professional interface  
✅ **Real-time API Health Check** - Automatic monitoring  
✅ **Multiple Prediction Types** - Single, batch, compare  
✅ **Confidence Scores** - See how confident the model is  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **Error Handling** - Clear error messages  
✅ **Interactive Visualizations** - Progress bars and probability charts  

---

## 🔍 Stress Level Guide

| Level | Score | Color | Meaning |
|-------|-------|-------|---------|
| **Low** | 0-3 | 🟢 Green | Employee is doing well |
| **Medium** | 3-6 | 🟡 Yellow | Monitor the employee |
| **High** | 6-10 | 🔴 Red | Intervention needed |

---

## 📁 Files

| File | Purpose |
|------|---------|
| `dashboard.html` | Web interface (open in browser) |
| `app.py` | Flask API server |
| `start.bat` | One-click launcher |
| `api_examples.py` | Python code examples |

---

## 🎯 Next Steps

1. **Run the server:** `python app.py`
2. **Open dashboard:** Visit `http://localhost:5000/dashboard`
3. **Make predictions:** Enter employee data and click "Predict"
4. **Compare models:** Use the "Compare Models" tab to see differences

---

## 🆘 Troubleshooting

### **Dashboard won't load**
```
Make sure Flask is running (you should see the message above)
Then try: http://localhost:5000/dashboard
```

### **"API Offline" error**
```
This means Flask server isn't running.
Run: python app.py
```

### **Port already in use (5000)**
```
Edit app.py and change port:
app.run(debug=True, port=5001)
```

---

## 💡 Pro Tips

- **Batch Prediction:** Great for analyzing multiple employees
- **Gender-Specific Models:** More accurate for targeted predictions
- **Model Comparison:** See which model works best for your data
- **Confidence Score:** Higher = more reliable prediction

---

**Enjoy your Employee Stress Prediction Dashboard!** 🎉
