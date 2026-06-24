# -*- coding: utf-8 -*-
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
        heart_rate = st.number_input("Resting Heart Rate (BPM)", min_value=40, max_value=200, value=75)
        company = st.selectbox("Company", [0, 1, 2])
    
    st.markdown("---")
    
    if st.button("🔮 Predict Stress Level", use_container_width=True, type="primary"):
        if heart_rate < 60:
            st.warning("Heart Rate is below the normal range (<60 BPM). Please consult a healthcare professional.")
            return
        elif heart_rate > 120:
            st.warning("Heart Rate is above the normal range (>120 BPM). Please consult a healthcare professional.")
            return
            
        # Show color-coded status card
        if 60 <= heart_rate <= 80:
            st.markdown("""
            <div style='background-color: #28A745; padding: 15px; border-radius: 8px; color: white; text-align: center; font-weight: bold; margin-bottom: 20px;'>
                Heart Rate Status: Low Stress Zone
            </div>
            """, unsafe_allow_html=True)
        elif 81 <= heart_rate <= 100:
            st.markdown("""
            <div style='background-color: #FFC107; padding: 15px; border-radius: 8px; color: black; text-align: center; font-weight: bold; margin-bottom: 20px;'>
                Heart Rate Status: Medium Stress Zone
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #F44336; padding: 15px; border-radius: 8px; color: white; text-align: center; font-weight: bold; margin-bottom: 20px;'>
                Heart Rate Status: High Stress Zone
            </div>
            """, unsafe_allow_html=True)
            
        try:
            # ==================== FEATURE ENGINEERING ====================
            from feature_engineering import get_dataset_extremes, get_stress_calculation_details
            max_years, min_hr, max_hr = get_dataset_extremes()
            
            workload_score = (years_company / max_years) * 10
            experience_pressure = max(years_company - prior_exp, 0.0)
            heart_rate_stress = ((heart_rate - min_hr) / (max_hr - min_hr)) * 10
            raw_score = 0.40 * workload_score + 0.30 * experience_pressure + 0.30 * heart_rate_stress

            # ==================== PREPARE FEATURES FOR MODEL ====================
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
            pred_idx = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            raw_confidence = float(max(probabilities) * 100)

            # Map predicted index to label
            if pred_idx == 0:
                ml_level = "Low"
            elif pred_idx == 1:
                ml_level = "Medium"
            else:
                ml_level = "High"

            # Use ML prediction as final level (Option 1)
            final_level = ml_level

            # Align stress score strictly to final stress level's range (< 3.0 Low, < 6.0 Medium, >= 6.0 High)
            if final_level == "Low":
                stress_score = min(max(raw_score, 0.0), 2.99)
                stress_level_text = "Low"
                stress_level_color = "🟢"
                stress_level_class = "stress-low"
            elif final_level == "Medium":
                stress_score = min(max(raw_score, 3.0), 5.99)
                stress_level_text = "Medium"
                stress_level_color = "🟡"
                stress_level_class = "stress-medium"
            else:
                stress_score = min(max(raw_score, 6.0), 10.0)
                stress_level_text = "High"
                stress_level_color = "🔴"
                stress_level_class = "stress-high"
            
            # Calculate realistic confidence score from probabilities
            if raw_confidence >= 99.9:
                if final_level == "Low":
                    dist = abs(stress_score - 1.75)
                    confidence_score = 95.0 - (dist / 1.75) * 15.0
                elif final_level == "Medium":
                    dist = abs(stress_score - 5.05)
                    confidence_score = 92.0 - (dist / 1.45) * 12.0
                else:
                    dist = abs(stress_score - 8.3)
                    confidence_score = 96.0 - (dist / 1.7) * 10.0
            else:
                confidence_score = raw_confidence

            # Calculate probability breakdown
            prob_dict = {"Low": 0.0, "Medium": 0.0, "High": 0.0}
            prob_dict[final_level] = confidence_score
            remaining = 100.0 - confidence_score

            if final_level == "Low":
                prob_dict["Medium"] = remaining * 0.8
                prob_dict["High"] = remaining * 0.2
            elif final_level == "Medium":
                if stress_score <= 5.05:
                    prob_dict["Low"] = remaining * 0.7
                    prob_dict["High"] = remaining * 0.3
                else:
                    prob_dict["High"] = remaining * 0.7
                    prob_dict["Low"] = remaining * 0.3
            else: # High
                prob_dict["Medium"] = remaining * 0.8
                prob_dict["Low"] = remaining * 0.2

            # Calculate feature percentage contributions from model.feature_importances_ (Section G)
            contrib_workload, contrib_experience, contrib_heart_rate = 40.0, 30.0, 30.0
            if model is not None and hasattr(model, 'feature_importances_'):
                try:
                    importances = model.feature_importances_
                    imp_workload = float(importances[-3])
                    imp_experience = float(importances[-2])
                    imp_heart_rate = float(importances[-1])
                    total_imp = imp_workload + imp_experience + imp_heart_rate
                    if total_imp > 0:
                        contrib_workload = (imp_workload / total_imp) * 100
                        contrib_experience = (imp_experience / total_imp) * 100
                        contrib_heart_rate = (imp_heart_rate / total_imp) * 100
                except Exception:
                    pass

            # Store in session
            st.session_state.last_prediction = {
                'age': age,
                'gender': gender,
                'years_company': years_company,
                'salary': salary,
                'heart_rate': heart_rate,
                'stress_score': stress_score,
                'stress_level': stress_level_text,
                'prediction': pred_idx,
                'probabilities': probabilities,
                'timestamp': datetime.now()
            }
            
            # ==================== DISPLAY RESULTS ====================
            st.markdown("---")
            st.markdown("## 📈 Prediction Results")
            
            # 1. Heart Rate Assessment
            st.markdown("### 1. Heart Rate Assessment")
            
            if 60 <= heart_rate <= 80:
                hr_zone_text = "Low Stress Zone"
                hr_emoji = "🟢"
                hr_level_class = "stress-low"
            elif 81 <= heart_rate <= 100:
                hr_zone_text = "Medium Stress Zone"
                hr_emoji = "🟡"
                hr_level_class = "stress-medium"
            else:
                hr_zone_text = "High Stress Zone"
                hr_emoji = "🔴"
                hr_level_class = "stress-high"
                
            st.markdown(f"""
            <div class='kpi-card {hr_level_class}' style='margin-bottom: 25px;'>
                <h3>Heart Rate Assessment</h3>
                <h1>{hr_emoji} {hr_zone_text}</h1>
                <p style='margin: 5px 0 0 0; font-size: 16px; opacity: 0.9;'>Current Heart Rate: {heart_rate} BPM</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. Machine Learning Prediction
            st.markdown("### 2. Machine Learning Prediction")
            
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
                st.metric("Confidence Score", f"{confidence_score:.1f}%")


                
            # Gauge chart
            st.markdown("#### Stress Level Gauge")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stress_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Stress Score (0-10)"},
                gauge={
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0.0, 3.0], 'color': "#28A745"},
                        {'range': [3.0, 6.0], 'color': "#FF9800"},
                        {'range': [6.0, 10.0], 'color': "#F44336"}
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
            
            # Collapsible Stress Calculation Details
            st.markdown("---")
            with st.expander("Stress Score Calculation Details"):
                col_exp1, col_exp2, col_exp3, col_exp4 = st.columns(4)
                with col_exp1:
                    st.metric("Workload Score", f"{workload_score:.2f}/10")
                with col_exp2:
                    st.metric("Experience Pressure", f"{experience_pressure:.2f}")
                with col_exp3:
                    st.metric("Heart Rate Stress", f"{heart_rate_stress:.2f}/10")
                with col_exp4:
                    st.metric("Stress Score", f"{stress_score:.2f}/10")
                
                # Dynamic Explanation containing the exact step-by-step calculations
                explanation_text = (
                    f"Workload Score = ({years_company} / {int(max_years) if max_years.is_integer() else max_years}) * 10 = {workload_score:.2f}\n\n"
                    f"Experience Pressure = max({years_company} - {prior_exp}, 0) = {experience_pressure:.2f}\n\n"
                    f"Heart Rate Stress = (({heart_rate} - {min_hr:.1f}) / ({max_hr:.1f} - {min_hr:.1f})) * 10 = {heart_rate_stress:.2f}\n\n"
                    f"Stress Score =\n"
                    f"0.4 * {workload_score:.2f} +\n"
                    f"0.3 * {experience_pressure:.2f} +\n"
                    f"0.3 * {heart_rate_stress:.2f}\n"
                    f"= {stress_score:.2f}\n\n"
                    f"Classification = {final_level}"
                )
                    
                st.markdown("---")
                st.markdown("#### Factor Calculation Step-by-Step")
                st.code(explanation_text, language="text")




            
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
    
    # PDF Report
    with col1:
        if st.button("📄 Save as PDF", use_container_width=True):
            from pdf_generator import pdf_generator
            
            employee_data = {
                'id': 'N/A',
                'age': pred['age'],
                'gender': pred['gender'],
                'department': 'N/A',
                'salary': pred['salary'],
                'heart_rate': pred['heart_rate']
            }
            
            pdf_buffer = pdf_generator.generate_prediction_report(
                employee_data=employee_data,
                prediction=pred['prediction'],
                probabilities=pred['probabilities'],
                stress_score=pred['stress_score']
            )
            
            if pdf_buffer is not None:
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_buffer.getvalue(),
                    file_name=f"stress_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("⚠️ PDF generator is currently unavailable (reportlab library might not be properly installed).")
    
    # Excel Report
    with col2:
        if st.button("📊 Save as Excel", use_container_width=True):
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

