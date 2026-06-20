"""
Professional Employee Stress Prediction System
Streamlit Application - ML-Based HR Analytics Platform

Methodology:
- Load dataset and perform preprocessing
- Feature Engineering (Workload Score, Experience Pressure, Heart Rate Stress)
- Stress Score Calculation (0.4*Workload + 0.3*Experience + 0.3*HeartRate)
- Stress Level Classification (0=Low, 1=Medium, 2=High)
- Decision Tree Model (99.4% Accuracy)

Flow: Login → Dashboard → Prediction → Results → Download Report
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import sys
from datetime import datetime
from io import BytesIO

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Employee Stress Prediction System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PROFESSIONAL STYLING ====================
st.markdown("""
    <style>
    /* Main color scheme - Professional Blue & White */
    :root {
        --primary-color: #0052CC;
        --secondary-color: #003D99;
        --success-color: #28A745;
        --warning-color: #FF9800;
        --danger-color: #F44336;
        --light-bg: #F5F7FA;
    }
    
    /* Professional cards */
    .kpi-card {
        background: linear-gradient(135deg, #0052CC 0%, #003D99 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 82, 204, 0.2);
        text-align: center;
    }
    
    .kpi-card h3 {
        margin: 0;
        font-size: 14px;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .kpi-card h1 {
        margin: 10px 0 0 0;
        font-size: 32px;
        font-weight: bold;
    }
    
    /* Stress level colors */
    .stress-low { background: linear-gradient(135deg, #28A745 0%, #20C997 100%); }
    .stress-medium { background: linear-gradient(135deg, #FF9800 0%, #FFA726 100%); }
    .stress-high { background: linear-gradient(135deg, #F44336 0%, #E53935 100%); }
    
    /* Header */
    .header-section {
        background: linear-gradient(135deg, #0052CC 0%, #003D99 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    
    .header-section h1 {
        margin: 0;
        font-size: 28px;
    }
    
    .header-section p {
        margin: 5px 0 0 0;
        opacity: 0.9;
    }
    
    /* Result card */
    .result-card {
        background: white;
        border-left: 5px solid #0052CC;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* Recommendation box */
    .recommendation-box {
        background: #F5F7FA;
        border-left: 4px solid #0052CC;
        padding: 15px;
        border-radius: 6px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
def initialize_session():
    """Initialize session state."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None

initialize_session()

# ==================== DEMO CREDENTIALS ====================
VALID_USERS = {
    'admin': 'admin123',
    'hr': 'hr123'
}

# ==================== LOAD DATA & MODELS ====================
@st.cache_resource
def load_data_and_models():
    """Load processed data and trained models."""
    data = None
    model = None
    
    try:
        # Load processed data
        if os.path.exists('outputs/processed_data.csv'):
            data = pd.read_csv('outputs/processed_data.csv')
        
        # Load best model
        if os.path.exists('models/best_general_model.pkl'):
            model = joblib.load('models/best_general_model.pkl')
    except Exception as e:
        st.warning(f"⚠️ Could not load data/models: {e}")
    
    return data, model

# ==================== LOGIN PAGE ====================
def show_login_page():
    """Display professional login page."""
    # Center layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>" * 3, unsafe_allow_html=True)
        
        # Company branding
        st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='color: #0052CC; font-size: 36px; margin: 0;'>🏢</h1>
            <h2 style='color: #0052CC; margin: 10px 0;'>Employee Stress Prediction System</h2>
            <p style='color: #666; font-size: 14px;'>Machine Learning Based HR Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login card
        st.markdown("""
        <div style='background: white; border-radius: 10px; padding: 30px; box-shadow: 0 4px 15px rgba(0,82,204,0.15);'>
        """, unsafe_allow_html=True)
        
        st.markdown("### Login")
        
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.button("🔓 Login", use_container_width=True, type="primary")
        
        if login_btn:
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Demo credentials info
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        **Demo Credentials:**
        
        👤 **Admin**
        - Username: `admin`
        - Password: `admin123`
        
        👥 **HR Manager**
        - Username: `hr`
        - Password: `hr123`
        """)

# ==================== DASHBOARD PAGE ====================
def show_dashboard(data, model):
    """Display dashboard with analytics."""
    st.markdown("""
    <div class='header-section'>
        <h1>📊 Dashboard</h1>
        <p>Employee Stress Analytics & Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    if data is None:
        st.error("❌ Data not available. Please run training first: python train.py")
        return
    
    # KPI Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_emp = len(data)
    low_stress = len(data[data['Stress_Level'] == 0]) if 'Stress_Level' in data.columns else 0
    medium_stress = len(data[data['Stress_Level'] == 1]) if 'Stress_Level' in data.columns else 0
    high_stress = len(data[data['Stress_Level'] == 2]) if 'Stress_Level' in data.columns else 0
    avg_score = data['Stress_Score'].mean() if 'Stress_Score' in data.columns else 0
    
    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <h3>Total Employees</h3>
            <h1>{total_emp}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-card stress-low'>
            <h3>🟢 Low Stress</h3>
            <h1>{low_stress}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='kpi-card stress-medium'>
            <h3>🟡 Medium Stress</h3>
            <h1>{medium_stress}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='kpi-card stress-high'>
            <h3>🔴 High Stress</h3>
            <h1>{high_stress}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class='kpi-card'>
            <h3>Avg Stress Score</h3>
            <h1>{avg_score:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Stress_Level' in data.columns:
            # Create data with explicit colors for each stress level
            stress_data = {
                'Stress Level': ['Low Stress', 'Medium Stress', 'High Stress'],
                'Count': [
                    len(data[data['Stress_Level'] == 0]),
                    len(data[data['Stress_Level'] == 1]),
                    len(data[data['Stress_Level'] == 2])
                ]
            }
            stress_df = pd.DataFrame(stress_data)
            
            fig = px.pie(
                stress_df,
                values='Count',
                names='Stress Level',
                title="Stress Distribution",
                hole=0.3
            )
            # Apply colors directly to pie slices
            fig.update_traces(
                marker=dict(colors=['#28A745', '#FF9800', '#F44336'])  # Green, Orange, Red
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Gender' in data.columns:
            gender_counts = data['Gender'].value_counts()
            gender_labels = ['Male' if x == 0 else 'Female' for x in gender_counts.index]
            fig = px.bar(
                x=gender_labels, y=gender_counts.values,
                title="Employee Distribution by Gender",
                color=gender_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)


# ==================== PREDICTION PAGE ====================
def show_prediction_page(model, data):
    """Display prediction form."""
    st.markdown("""
    <div class='header-section'>
        <h1>🔮 Stress Prediction</h1>
        <p>Predict employee stress level using ML model</p>
    </div>
    """, unsafe_allow_html=True)
    
    if model is None:
        st.error("❌ Model not available. Please run training first: python train.py")
        return
    
    st.markdown("### Employee Information")
    
    # Two-column layout for form
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=70, value=35)
        gender = st.selectbox("Gender", ["Male", "Female"])
        years_company = st.number_input("Years in Company", min_value=0.0, max_value=50.0, value=5.0, step=0.5)
        prior_exp = st.number_input("Prior Years Experience", min_value=0.0, max_value=50.0, value=3.0, step=0.5)
        age_when_joined = age - years_company
    
    with col2:
        salary = st.number_input("Salary (₹)", min_value=20000, max_value=500000, value=60000, step=5000)
        bonus = st.number_input("Annual Bonus (₹)", min_value=0.0, max_value=100000.0, value=5000.0, step=1000.0)
        heart_rate = st.number_input("Resting Heart Rate (BPM)", min_value=40, max_value=120, value=75)
        company = st.selectbox("Company", [0, 1, 2])
    
    st.markdown("---")
    
    if st.button("🔮 Predict Stress Level", use_container_width=True, type="primary"):
        try:
            # ==================== FEATURE ENGINEERING ====================
            # Using exact same methodology as training
            
            # 1. Workload_Score
            max_years = data['years_in_the_company'].max() if 'years_in_the_company' in data.columns else 50
            workload_score = (years_company / max_years) * 10
            
            # 2. Experience_Pressure
            experience_pressure = max(years_company - prior_exp, 0)
            
            # 3. HeartRate_Stress
            min_hr = data['Resting_Heart_Rate'].min() if 'Resting_Heart_Rate' in data.columns else 40
            max_hr = data['Resting_Heart_Rate'].max() if 'Resting_Heart_Rate' in data.columns else 120
            heart_rate_stress = ((heart_rate - min_hr) / (max_hr - min_hr)) * 10 if max_hr != min_hr else 0
            
            # 4. Stress_Score
            stress_score = 0.4 * workload_score + 0.3 * experience_pressure + 0.3 * heart_rate_stress
            
            # 5. Stress_Level (for reference)
            if stress_score < 3:
                stress_level_text = "Low"
                stress_level_color = "🟢"
                stress_level_class = "stress-low"
            elif stress_score < 6:
                stress_level_text = "Medium"
                stress_level_color = "🟡"
                stress_level_class = "stress-medium"
            else:
                stress_level_text = "High"
                stress_level_color = "🔴"
                stress_level_class = "stress-high"
            
            # ==================== PREPARE FEATURES FOR MODEL ====================
            # Build feature array with 19 features (matching training data structure)
            # Feature order: employee_id, age, age_when_joined, years_in_the_company, salary, 
            # annual_bonus, prior_years_experience, Gender, Resting_Heart_Rate,
            # company_Glasses, company_Pear, department_BigData, department_Design,
            # department_Sales, department_Search Engine, department_Support,
            # Workload_Score, Experience_Pressure, HeartRate_Stress
            
            features = np.array([[
                0,  # employee_id (0 for new predictions)
                age,
                age_when_joined,
                years_company,
                salary,
                bonus,
                prior_exp,
                1 if gender == "Female" else 0,  # Gender (0=Male, 1=Female)
                heart_rate,
                1 if company == 0 else 0,  # company_Glasses
                1 if company == 1 else 0,  # company_Pear
                0,  # department_BigData (set to 0 for implicit reference category)
                0,  # department_Design
                0,  # department_Sales
                0,  # department_Search Engine
                0,  # department_Support
                workload_score,
                experience_pressure,
                heart_rate_stress
            ]])
            
            # ==================== MAKE PREDICTION ====================
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            
            # Store in session
            st.session_state.last_prediction = {
                'age': age,
                'gender': gender,
                'years_company': years_company,
                'salary': salary,
                'heart_rate': heart_rate,
                'stress_score': stress_score,
                'stress_level': stress_level_text,
                'prediction': prediction,
                'probabilities': probabilities,
                'timestamp': datetime.now()
            }
            
            # ==================== DISPLAY RESULTS ====================
            st.markdown("---")
            st.markdown("### 📈 Prediction Results")
            
            # Result cards
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class='kpi-card {stress_level_class}'>
                    <h3>Predicted Stress Level</h3>
                    <h1>{stress_level_color} {stress_level_text}</h1>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Stress Score", f"{stress_score:.2f}/10")
            
            with col3:
                confidence = max(probabilities) * 100
                st.metric("Confidence", f"{confidence:.1f}%")
            
            st.markdown("---")
            
            # Gauge chart
            st.markdown("### 📊 Stress Level Gauge")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stress_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Stress Score (0-10)"},
                gauge={
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 3], 'color': "#28A745"},
                        {'range': [3, 6], 'color': "#FF9800"},
                        {'range': [6, 10], 'color': "#F44336"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': stress_score
                    }
                }
            ))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Recommendations
            st.markdown("### 💡 HR Recommendation")
            
            if stress_level_text == "Low":
                st.markdown("""
                <div class='recommendation-box'>
                <h4>✅ Employee Status: Healthy</h4>
                
                **Actions:**
                - Continue current work arrangement
                - Recognize and reward good performance
                - Support career development opportunities
                - Maintain regular check-ins
                </div>
                """, unsafe_allow_html=True)
            
            elif stress_level_text == "Medium":
                st.markdown("""
                <div class='recommendation-box'>
                <h4>⚠️ Monitor Required</h4>
                
                **Actions:**
                - Reduce workload where possible
                - Offer wellness programs and activities
                - Schedule one-on-one meetings with manager
                - Consider flexible work arrangements
                </div>
                """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div class='recommendation-box'>
                <h4>🚨 Intervention Required</h4>
                
                **Actions:**
                - Schedule urgent meeting with HR department
                - Offer mental health counseling services
                - Consider temporary workload reduction
                - Explore mentoring and support programs
                </div>
                """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Prediction error: {e}")

# ==================== REPORTS PAGE ====================
def show_reports_page():
    """Display report download options."""
    st.markdown("""
    <div class='header-section'>
        <h1>📁 Download Reports</h1>
        <p>Export prediction reports and employee data</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.last_prediction is None:
        st.info("ℹ️ No predictions yet. Go to Stress Prediction to make a prediction.")
        return
    
    pred = st.session_state.last_prediction
    
    st.markdown("### 📊 Generate Report")
    
    col1, col2 = st.columns(2)
    
    # CSV Report
    with col1:
        if st.button("📥 Download as CSV", use_container_width=True):
            report_data = {
                'Date': [pred['timestamp'].strftime('%Y-%m-%d %H:%M:%S')],
                'Age': [pred['age']],
                'Gender': [pred['gender']],
                'Years in Company': [pred['years_company']],
                'Salary': [pred['salary']],
                'Heart Rate': [pred['heart_rate']],
                'Stress Score': [f"{pred['stress_score']:.2f}"],
                'Stress Level': [pred['stress_level']],
                'Confidence': [f"{max(pred['probabilities'])*100:.1f}%"]
            }
            
            df_report = pd.DataFrame(report_data)
            csv = df_report.to_csv(index=False)
            
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"stress_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Excel Report
    with col2:
        if st.button("📊 Download as Excel", use_container_width=True):
            report_data = {
                'Date': [pred['timestamp'].strftime('%Y-%m-%d %H:%M:%S')],
                'Age': [pred['age']],
                'Gender': [pred['gender']],
                'Years in Company': [pred['years_company']],
                'Salary': [pred['salary']],
                'Heart Rate': [pred['heart_rate']],
                'Stress Score': [f"{pred['stress_score']:.2f}"],
                'Stress Level': [pred['stress_level']],
                'Confidence': [f"{max(pred['probabilities'])*100:.1f}%"]
            }
            
            df_report = pd.DataFrame(report_data)
            
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_report.to_excel(writer, index=False, sheet_name='Prediction')
            buffer.seek(0)
            
            st.download_button(
                label="📊 Download Excel",
                data=buffer.getvalue(),
                file_name=f"stress_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    st.markdown("---")
    
    # Display report preview
    st.markdown("### 📋 Report Preview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Date:** {pred['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Age:** {pred['age']} years")
        st.write(f"**Gender:** {pred['gender']}")
        st.write(f"**Years in Company:** {pred['years_company']} years")
    
    with col2:
        st.write(f"**Salary:** ₹{pred['salary']:,.0f}")
        st.write(f"**Heart Rate:** {pred['heart_rate']} BPM")
        st.write(f"**Stress Score:** {pred['stress_score']:.2f}/10")
        st.write(f"**Stress Level:** {pred['stress_level']}")

# ==================== MAIN APP ====================
def main():
    """Main application flow."""
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        # Load data and models
        data, model = load_data_and_models()
        
        # Sidebar
        st.sidebar.markdown("---")
        st.sidebar.title(f"👤 {st.session_state.username.upper()}")
        st.sidebar.markdown(f"*Logged in*")
        st.sidebar.markdown("---")
        
        # Navigation
        page = st.sidebar.radio(
            "Navigation",
            ["📊 Dashboard", "🔮 Stress Prediction", "📁 Reports"],
            label_visibility="collapsed"
        )
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        **Employee Stress Prediction System**
        
        Version: 1.0
        
        ML-Based HR Analytics Platform
        """)
        
        # Route pages
        if page == "📊 Dashboard":
            show_dashboard(data, model)
        elif page == "🔮 Stress Prediction":
            show_prediction_page(model, data)
        elif page == "📁 Reports":
            show_reports_page()

if __name__ == "__main__":
    main()

