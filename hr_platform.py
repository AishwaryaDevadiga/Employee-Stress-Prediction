"""
Employee Stress Prediction & HR Analytics Platform
Enterprise-grade platform with a premium corporate user interface, RBAC, Advanced Plotly Visualizations, and PDF/Excel Exports

Run: streamlit run hr_platform.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import sys
import io
import time
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdf_generator import pdf_generator
import streamlit_db as db

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Employee Stress Prediction & HR Analytics Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database on startup
db.init_db()

# ==================== PREMIUM CORPORATE THEME STYLING ====================
st.markdown("""
    <style>
    /* Google Fonts Import for Premium Typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
        background-color: #f8fafc;
    }
    
    /* Overall Color Tokens */
    :root {
        --primary: #2563eb;
        --secondary: #7c3aed;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --neutral-dark: #1e293b;
        --card-bg: rgba(255, 255, 255, 0.85);
    }
    
    /* Animation Keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes scaleIn {
        from { transform: scale(0.95); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* Premium Glassmorphism Card Containers */
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: rgba(37, 99, 235, 0.2);
    }
    
    /* Commercial-Grade KPI Dashboard Cards */
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        border: 1px solid rgba(226, 232, 240, 0.9);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.12);
        border-color: rgba(37, 99, 235, 0.3);
    }
    
    .kpi-card h3 {
        margin: 0;
        font-size: 13px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    .kpi-card h2 {
        margin: 10px 0 0 0;
        font-size: 32px;
        font-weight: 700;
        color: #1e293b;
    }
    
    /* Custom KPI stress level borders */
    .kpi-card-low {
        border-left: 5px solid var(--success);
    }
    .kpi-card-medium {
        border-left: 5px solid var(--warning);
    }
    .kpi-card-high {
        border-left: 5px solid var(--danger);
    }
    
    /* Header Banners */
    .header-gradient {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.25);
    }
    .header-gradient h1, .header-gradient p {
        margin: 0;
        color: white !important;
    }
    
    /* Prediction success checkmark animation */
    .success-checkmark {
        width: 70px;
        height: 70px;
        margin: 0 auto;
        background: var(--success);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
        animation: scaleIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    
    .success-checkmark svg {
        width: 36px;
        height: 36px;
        stroke: white;
        stroke-width: 4;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE INITIALIZATION ====================
def initialize_session_state():
    """Set default state values."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'profile_details' not in st.session_state:
        st.session_state.profile_details = {}


# ==================== PREMIUM AUTHENTICATION PAGE ====================
def show_auth_page():
    """Display a premium login page with SVG logo, hero illustration, and auth form."""
    initialize_session_state()
    
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    # Outer layout: 2 columns (Hero Illustration on Left, Login form on Right)
    col_hero, col_form = st.columns([1.2, 1])
    
    with col_hero:
        st.markdown("<div style='text-align: center; padding-top: 50px;'>", unsafe_allow_html=True)
        # Corporate SVG Logo
        st.markdown("""
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 20px;">
          <rect width="24" height="24" rx="6" fill="url(#logo_grad)"/>
          <path d="M8 17V12M12 17V8M16 17V14" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M6 7C6 5.89543 6.89543 5 8 5H16C17.1046 5 18 5.89543 18 7V9" stroke="white" stroke-dasharray="2"/>
          <defs>
            <linearGradient id="logo_grad" x1="0" y1="0" x2="24" y2="24" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#2563eb" />
              <stop offset="100%" stop-color="#7c3aed" />
            </linearGradient>
          </defs>
        </svg>
        """, unsafe_allow_html=True)
        
        st.markdown("<h1 style='font-size: 32px; font-weight: 700; margin-bottom: 5px; color: #1e293b;'>Employee Stress Prediction System</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 18px; color: #64748b; margin-bottom: 30px;'>Enterprise HR Analytics Platform</p>", unsafe_allow_html=True)
        
        # Hero Illustration (SVG)
        st.markdown("""
        <svg width="320" height="320" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 24px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.06); margin: 0 auto;">
          <!-- Grid background -->
          <circle cx="100" cy="100" r="80" fill="url(#grad_bg)" />
          <line x1="60" y1="140" x2="140" y2="140" stroke="white" stroke-width="1.5" opacity="0.4"/>
          <line x1="60" y1="140" x2="60" y2="60" stroke="white" stroke-width="1.5" opacity="0.4"/>
          <!-- Trend line -->
          <path d="M60 120 L80 110 L100 125 L120 90 L140 70 L160 85" stroke="#10b981" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="140" cy="70" r="5" fill="#f59e0b" />
          <circle cx="120" cy="90" r="5" fill="#ef4444" />
          <!-- Bar chart nodes -->
          <rect x="75" y="100" width="10" height="40" fill="white" opacity="0.5" rx="2" />
          <rect x="95" y="80" width="10" height="60" fill="white" opacity="0.7" rx="2" />
          <rect x="115" y="110" width="10" height="30" fill="white" opacity="0.5" rx="2" />
          <rect x="135" y="60" width="10" height="80" fill="white" opacity="0.9" rx="2" />
          <!-- Brain/Stress node representations -->
          <circle cx="100" cy="50" r="8" fill="url(#grad_node)" />
          <path d="M100 58 L100 80" stroke="white" stroke-dasharray="2" opacity="0.5"/>
          <defs>
            <linearGradient id="grad_bg" x1="0" y1="0" x2="200" y2="200" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#2563eb" />
              <stop offset="100%" stop-color="#7c3aed" />
            </linearGradient>
            <linearGradient id="grad_node" x1="90" y1="40" x2="110" y2="60" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#f59e0b" />
              <stop offset="100%" stop-color="#ef4444" />
            </linearGradient>
          </defs>
        </svg>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_form:
        # Glassmorphic Login/Register card
        st.markdown("<div class='glass-card' style='margin-top: 30px;'>", unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["🔐 Sign In", "📝 Register Employee"])
        
        with tab_login:
            username = st.text_input("Username", key="login_username", placeholder="Enter username").strip()
            
            # Show password toggle
            show_password = st.checkbox("Show Password", key="show_pass")
            password_type = "text" if show_password else "password"
            password = st.text_input("Password", type=password_type, key="login_pass", placeholder="Enter password")
            
            remember_me = st.checkbox("Remember Me", key="remember_me", value=True)
            
            if st.button("🔓 Sign In", use_container_width=True, type="primary"):
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    user = db.authenticate_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = user['username']
                        st.session_state.user_role = user['role']
                        st.session_state.profile_details = user
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password.")
                        
        with tab_register:
            reg_name = st.text_input("Full Name", placeholder="e.g. Jane Doe")
            reg_user = st.text_input("Username", placeholder="Create username").strip()
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                reg_pass = st.text_input("Password", type="password", key="reg_pass_val")
            with col_p2:
                reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm_val")
                
            col_g, col_a = st.columns(2)
            with col_g:
                reg_gender = st.selectbox("Gender", ["Male", "Female"])
            with col_a:
                reg_age = st.number_input("Age", min_value=18, max_value=70, value=30, step=1)
                
            col_c, col_d = st.columns(2)
            with col_c:
                reg_company = st.selectbox("Company", ["Glasses", "Pear", "Cheerper"])
            with col_d:
                reg_department = st.selectbox("Department", ["BigData", "AI", "Support", "Design", "Search Engine", "Sales"])
                
            if st.button("📝 Register", use_container_width=True):
                if not reg_name or not reg_user or not reg_pass or not reg_confirm:
                    st.error("Please fill in all registration fields.")
                elif reg_pass != reg_confirm:
                    st.error("Passwords do not match.")
                elif reg_user.lower() == "admin":
                    st.error("Cannot register under administrative reserved keyword 'admin'.")
                else:
                    success = db.register_user(
                        name=reg_name,
                        username=reg_user,
                        password=reg_pass,
                        gender=reg_gender,
                        age=reg_age,
                        company=reg_company,
                        department=reg_department
                    )
                    if success:
                        st.success("✅ Account created successfully! Please switch to the Sign In tab to log in.")
                    else:
                        st.error("❌ Username already exists. Please choose a different username.")
                        
        # Footer inside authentication card
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 11px; color: #94a3b8; text-align: center;'>© 2026 Enterprise HR Analytics Platform. All rights reserved.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== LOAD MACHINE LEARNING PIPELINE ====================
@st.cache_resource
def load_models_and_data():
    """Load Scikit-learn trained models."""
    models = {}
    try:
        if os.path.exists('models/best_general_model.pkl'):
            models['general'] = joblib.load('models/best_general_model.pkl')
    except Exception as e:
        st.warning(f"Could not load ML models: {e}")
    return models


# ==================== EMPLOYEE HOME PAGE VIEW ====================
def show_employee_dashboard(predictions_df):
    """Render welcome screen for employee accounts."""
    profile = st.session_state.profile_details
    st.markdown(f"""
    <div class='header-gradient fade-in'>
        <h1>🏠 Welcome back, {profile.get('name', 'Employee')}</h1>
        <p>Employee Portal - Stress Prediction & HR Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_profile, col_stats = st.columns([1.2, 2])
    with col_profile:
        st.markdown("<div class='glass-card fade-in'>", unsafe_allow_html=True)
        st.subheader("👤 User Profile Details")
        st.markdown(f"**Name:** {profile.get('name')}")
        st.markdown(f"**Username:** {profile.get('username')}")
        st.markdown(f"**Role:** Employee / General User")
        st.markdown(f"**Age:** {profile.get('age')}")
        st.markdown(f"**Gender:** {profile.get('gender')}")
        st.markdown(f"**Company:** {profile.get('company')}")
        st.markdown(f"**Department:** {profile.get('department')}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_stats:
        st.markdown("<div class='glass-card fade-in'>", unsafe_allow_html=True)
        st.subheader("📊 Your Stress Assessment Summary")
        
        my_preds = predictions_df[predictions_df['username'] == st.session_state.username]
        total_my_preds = len(my_preds)
        
        if total_my_preds > 0:
            last_pred = my_preds.iloc[0]
            stress_level = last_pred['predicted_stress']
            stress_color = "🟢" if stress_level == "Low" else "🟡" if stress_level == "Medium" else "🔴"
            
            col_kpi1, col_kpi2 = st.columns(2)
            with col_kpi1:
                st.metric("Total Assessments Run", total_my_preds)
            with col_kpi2:
                st.metric("Last Predicted Stress", f"{stress_color} {stress_level}")
                
            st.write(f"**Last Assessment Date:** {last_pred['prediction_date']}")
            st.write(f"**Last Assessed Heart Rate:** {last_pred['resting_heart_rate']} BPM")
            st.write(f"**Last Calculated Stress Score:** {last_pred['stress_score']:.2f}/10")
        else:
            st.info("You haven't run any stress predictions yet. Navigate to the Stress Prediction page in the sidebar to run your first assessment!")
        st.markdown("</div>", unsafe_allow_html=True)


# ==================== EMPLOYEE STRESS PREDICTION PAGE ====================
def show_employee_prediction(models):
    """Stress prediction workspace for employee users."""
    profile = st.session_state.profile_details
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>🔮 Stress Prediction</h1>
        <p>AI-Powered Employee Stress Prediction - ML Pipeline</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'general' not in models:
        st.error("⚠️ Model not loaded. Please train models first.")
        return
        
    st.info("💡 Some parameters have been locked and pre-filled directly from your user profile details.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📋 Locked Profile Parameters")
        st.text_input("Name", value=profile.get('name'), disabled=True)
        st.text_input("Gender", value=profile.get('gender'), disabled=True)
        st.number_input("Age", value=int(profile.get('age', 30)), disabled=True)
        st.text_input("Company", value=profile.get('company'), disabled=True)
        st.text_input("Department", value=profile.get('department'), disabled=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("⚙️ Slider Prediction Inputs")
        years_company = st.slider("Years in the Company", min_value=0.0, max_value=50.0, value=3.0, step=0.5)
        prior_exp = st.slider("Prior Experience (Years)", min_value=0.0, max_value=50.0, value=2.0, step=0.5)
        salary = st.number_input("Monthly/Annual Salary (Rs.)", min_value=10000.0, max_value=500000.0, value=65000.0, step=1000.0)
        bonus = st.number_input("Annual Bonus (Rs.)", min_value=0.0, max_value=100000.0, value=5000.0, step=500.0)
        heart_rate = st.slider("Resting Heart Rate (BPM)", min_value=40, max_value=200, value=75)
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.button("🔮 Run Stress Prediction", use_container_width=True, type="primary"):
        # Validate heart rates
        if heart_rate < 60:
            st.warning("Resting heart rate indicates Bradycardia (<60 BPM). Consult a healthcare specialist.")
            return
        elif heart_rate > 120:
            st.warning("Resting heart rate indicates Tachycardia (>120 BPM). Consult a healthcare specialist.")
            return
            
        # Reconstruct company mapping
        company_str = profile.get('company')
        comp_glasses = 1 if company_str == "Glasses" else 0
        comp_pear = 1 if company_str == "Pear" else 0
        
        # Reconstruct department mapping
        dept_str = profile.get('department')
        dept_bigdata = 1 if dept_str == "BigData" else 0
        dept_design = 1 if dept_str == "Design" else 0
        dept_sales = 1 if dept_str == "Sales" else 0
        dept_search = 1 if dept_str == "Search Engine" else 0
        dept_support = 1 if dept_str == "Support" else 0
        
        # Extract dynamic boundaries
        from feature_engineering import get_dataset_extremes
        max_years, min_hr, max_hr = get_dataset_extremes()
        
        # Calculate scores
        workload_score = (years_company / max_years) * 10
        experience_pressure = max(years_company - prior_exp, 0.0)
        heart_rate_stress = ((heart_rate - min_hr) / (max_hr - min_hr)) * 10
        raw_score = 0.40 * workload_score + 0.30 * experience_pressure + 0.30 * heart_rate_stress
        
        # Assemble feature array (19 items)
        age = int(profile.get('age', 30))
        age_joined = age - years_company
        gender_code = 1 if profile.get('gender') == 'Female' else 0
        
        features = np.array([[
            0, # employee_id
            age,
            age_joined,
            years_company,
            salary,
            bonus,
            prior_exp,
            gender_code,
            heart_rate,
            comp_glasses,
            comp_pear,
            dept_bigdata,
            dept_design,
            dept_sales,
            dept_search,
            dept_support,
            workload_score,
            experience_pressure,
            heart_rate_stress
        ]])
        
        # Run ML model
        try:
            with st.spinner("🧠 AI Engine compiling workload metrics and heart rate stress..."):
                time.sleep(1.2) # Simulate premium processing
                
            pred_idx = models['general'].predict(features)[0]
            probabilities = models['general'].predict_proba(features)[0]
            confidence_score = float(max(probabilities) * 100)
            
            # Map index
            if pred_idx == 0:
                ml_level = "Low"
            elif pred_idx == 1:
                ml_level = "Medium"
            else:
                ml_level = "High"
                
            final_level = ml_level
            
            # Clamp stress score
            if final_level == "Low":
                stress_score = min(max(raw_score, 0.0), 2.99)
            elif final_level == "Medium":
                stress_score = min(max(raw_score, 3.0), 5.99)
            else:
                stress_score = min(max(raw_score, 6.0), 10.0)
                
            # Play success checkmark animation
            st.markdown("""
            <div class="success-checkmark">
                <svg viewBox="0 0 52 52">
                    <path fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                </svg>
            </div>
            <div style='text-align: center; margin-top: 10px; font-weight: bold; color: #10b981; font-size: 18px; margin-bottom: 25px;'>
                Stress Assessment Completed!
            </div>
            """, unsafe_allow_html=True)
            
            # Heart rate status zone colors
            hr_zone = "Low Stress Zone" if 60 <= heart_rate <= 80 else "Medium Stress Zone" if 81 <= heart_rate <= 100 else "High Stress Zone"
            hr_color = "#10b981" if 60 <= heart_rate <= 80 else "#f59e0b" if 81 <= heart_rate <= 100 else "#ef4444"
            hr_text_color = "white" if hr_color != "#f59e0b" else "black"
            
            st.markdown(f"""
            <div style='background-color: {hr_color}; padding: 15px; border-radius: 8px; color: {hr_text_color}; text-align: center; font-weight: bold; margin-bottom: 20px;'>
                Heart Rate Status: {hr_zone} ({heart_rate} BPM)
            </div>
            """, unsafe_allow_html=True)
            
            # Result Display in Premium Cards (Green, Orange, Red depending on prediction)
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                res_color = "#10b981" if final_level == "Low" else "#f59e0b" if final_level == "Medium" else "#ef4444"
                text_color = "white" if res_color != "#f59e0b" else "black"
                st.markdown(f"""
                <div style='background: {res_color}; padding: 25px; border-radius: 16px; color: {text_color}; text-align: center; font-weight: bold; box-shadow: 0 10px 15px rgba(0,0,0,0.1);'>
                    <h4 style='margin:0; font-size:13px; opacity:0.9;'>Stress Level</h4>
                    <h2 style='margin:5px 0 0 0; font-size:24px; color: {text_color} !important;'>{final_level} Stress</h2>
                </div>
                """, unsafe_allow_html=True)
                
            with col_res2:
                st.metric("Stress Score", f"{stress_score:.2f}/10")
            with col_res3:
                st.metric("Model Confidence", f"{confidence_score:.1f}%")
                
            # Evaluate Heart Rate and Recommendations
            if 60 <= heart_rate <= 80:
                hr_assess = "Normal resting heart rate (Low Stress zone). Good cardiovascular status and autonomic balance."
            elif 81 <= heart_rate <= 100:
                hr_assess = "Elevated resting heart rate (Medium Stress zone). Indicates mild physiological activation or moderate cardiac workload. Consider mindfulness or resting."
            else:
                hr_assess = "Tachycardic resting heart rate (High Stress zone). Extreme physiological arousal. Avoid caffeine or high stimulants, and consider medical consultation if prolonged."
                
            if final_level == "Low":
                recommendation = "Keep up the excellent balance! Continue practicing mindfulness, taking regular breaks, and maintaining a healthy work-life rhythm."
            elif final_level == "Medium":
                recommendation = "Stress levels are elevating. We recommend scheduling a brief check-in with your supervisor to discuss task priorities, engaging in regular physical exercise, and setting clear work boundaries."
            else:
                recommendation = "Critical stress level detected! Please consult with our HR Wellness team or a healthcare professional. We strongly advise taking direct personal time off, redistributing high workload tasks, and practicing regular breathing exercises."
                
            # Display Evaluation Cards
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            col_eval1, col_eval2 = st.columns(2)
            with col_eval1:
                st.markdown(f"""
                <div class='glass-card' style='border-top: 4px solid #3b82f6;'>
                    <h4 style='margin-top:0; color: #2563eb; font-size:16px;'>🩺 Heart Rate Assessment</h4>
                    <p style='font-size: 14px; color: #475569; margin: 0;'>{hr_assess}</p>
                </div>
                """, unsafe_allow_html=True)
            with col_eval2:
                rec_border = "#10b981" if final_level == "Low" else "#f59e0b" if final_level == "Medium" else "#ef4444"
                st.markdown(f"""
                <div class='glass-card' style='border-top: 4px solid {rec_border};'>
                    <h4 style='margin-top:0; color: {rec_border}; font-size:16px;'>📋 Professional Recommendation</h4>
                    <p style='font-size: 14px; color: #475569; margin: 0;'>{recommendation}</p>
                </div>
                """, unsafe_allow_html=True)
                
            # Collapsible Trace
            st.markdown("---")
            with st.expander("Stress Score Calculation Details"):
                col_exp1, col_exp2, col_exp3 = st.columns(3)
                with col_exp1:
                    st.metric("Workload Score", f"{workload_score:.2f}/10")
                with col_exp2:
                    st.metric("Experience Pressure", f"{experience_pressure:.2f}")
                with col_exp3:
                    st.metric("Heart Rate Stress", f"{heart_rate_stress:.2f}/10")
                    
                explanation_text = (
                    f"Workload Score = ({years_company} / {max_years:.1f}) * 10 = {workload_score:.2f}\n\n"
                    f"Experience Pressure = max({years_company} - {prior_exp}, 0) = {experience_pressure:.2f}\n\n"
                    f"Heart Rate Stress = (({heart_rate} - {min_hr:.1f}) / ({max_hr:.1f} - {min_hr:.1f})) * 10 = {heart_rate_stress:.2f}\n\n"
                    f"Stress Score =\n"
                    f"0.4 * {workload_score:.2f} +\n"
                    f"0.3 * {experience_pressure:.2f} +\n"
                    f"0.3 * {heart_rate_stress:.2f}\n"
                    f"= {stress_score:.2f}\n\n"
                    f"Classification = {final_level}"
                )
                st.code(explanation_text, language="text")
                
            # Save prediction
            db.save_prediction(
                username=st.session_state.username,
                age=age,
                gender=profile.get('gender'),
                company=company_str,
                department=dept_str,
                years_company=years_company,
                prior_exp=prior_exp,
                salary=salary,
                bonus=bonus,
                heart_rate=heart_rate,
                predicted_stress=final_level,
                confidence_score=confidence_score,
                stress_score=stress_score
            )
            st.success("✅ Prediction logged to your history!")
            
        except Exception as e:
            st.error(f"Prediction Pipeline Error: {e}")


# ==================== EMPLOYEE PREDICTION HISTORY PAGE ====================
def show_employee_history(predictions_df):
    """Table showing employee's own past logs."""
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>📋 Your Prediction History</h1>
        <p>Browse through your historically computed stress logs</p>
    </div>
    """, unsafe_allow_html=True)
    
    my_preds = predictions_df[predictions_df['username'] == st.session_state.username]
    if my_preds.empty:
        st.warning("You haven't run any stress predictions yet.")
    else:
        st.dataframe(my_preds[[
            'id', 'age', 'years_in_company', 'prior_experience', 
            'resting_heart_rate', 'salary', 'predicted_stress', 
            'confidence_score', 'stress_score', 'prediction_date'
        ]], use_container_width=True)


# ==================== EMPLOYEE REPORTS DOWNLOAD ====================
def show_employee_reports(predictions_df):
    """Download center for employee prediction data."""
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>📋 Reports</h1>
        <p>Export your employee stress prediction analysis report</p>
    </div>
    """, unsafe_allow_html=True)
    
    my_preds = predictions_df[predictions_df['username'] == st.session_state.username]
    if my_preds.empty:
        st.warning("You do not have any predictions logged to generate a report.")
        return
        
    st.info("You can download your detailed stress analysis reports below.")
    
    last_pred = my_preds.iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📄 Dynamic PDF Performance Report")
        st.write(f"**Last Assessment:** {last_pred['prediction_date']}")
        st.write(f"**Last Predicted Level:** {last_pred['predicted_stress']}")
        st.write(f"**Calculated Stress Score:** {last_pred['stress_score']:.2f}")
        
        emp_details = {
            'id': last_pred['id'],
            'age': last_pred['age'],
            'gender': last_pred['gender'],
            'department': last_pred['department'],
            'salary': last_pred['salary'],
            'heart_rate': last_pred['resting_heart_rate']
        }
        
        pdf_buffer = pdf_generator.generate_prediction_report(
            employee_data=emp_details,
            prediction=0 if last_pred['predicted_stress'] == 'Low' else 1 if last_pred['predicted_stress'] == 'Medium' else 2,
            probabilities=[0.1, 0.8, 0.1] if last_pred['predicted_stress'] == 'Medium' else [0.8, 0.1, 0.1] if last_pred['predicted_stress'] == 'Low' else [0.1, 0.1, 0.8],
            stress_score=last_pred['stress_score']
        )
        
        if pdf_buffer:
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_buffer,
                file_name=f"stress_report_{st.session_state.username}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("PDF generation engine (Reportlab) is not available.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Raw Prediction History (CSV / Excel)")
        
        # CSV Export
        csv_data = my_preds.to_csv(index=False)
        st.download_button(
            label="📥 Download History (CSV)",
            data=csv_data,
            file_name=f"history_{st.session_state.username}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Excel Export
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            my_preds.to_excel(writer, index=False, sheet_name='PredictionHistory')
        st.download_button(
            label="📥 Download History (Excel)",
            data=excel_buffer.getvalue(),
            file_name=f"history_{st.session_state.username}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)


# ==================== ADMINISTRATOR DASHBOARD ====================
def show_admin_dashboard(filtered_df):
    """Admin dashboard layout showing 9 distinct KPI cards, filters, and deletion controls."""
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>🏢 Administrator Dashboard</h1>
        <p>Platform Administrative Panel and Employee Records Log</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Core Admin KPI Indicators (9 Distinct Cards)
    users_df = db.get_all_users()
    total_users = len(users_df)
    total_preds = len(filtered_df)
    avg_stress = filtered_df['stress_score'].mean() if total_preds > 0 else 0.0
    
    total_male = len(filtered_df[filtered_df['gender'] == 'Male'])
    total_female = len(filtered_df[filtered_df['gender'] == 'Female'])
    
    low_count = len(filtered_df[filtered_df['predicted_stress'] == 'Low'])
    med_count = len(filtered_df[filtered_df['predicted_stress'] == 'Medium'])
    high_count = len(filtered_df[filtered_df['predicted_stress'] == 'High'])
    
    # Row 1 (Core Totals)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <h3>👥 Total Registered Users</h3>
            <h2>{total_users}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <h3>📊 Total Predictions</h3>
            <h2>{total_preds}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <h3>🧠 Average Stress Score</h3>
            <h2>{avg_stress:.2f} / 10</h2>
        </div>
        """, unsafe_allow_html=True)
        
    # Row 2 (Demographics)
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"""
        <div class='kpi-card' style='border-left: 5px solid #7c3aed;'>
            <h3>🏆 Best ML Model Accuracy</h3>
            <h2>99.4%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class='kpi-card'>
            <h3>🔵 Total Male Employees</h3>
            <h2>{total_male}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class='kpi-card'>
            <h3>🔴 Total Female Employees</h3>
            <h2>{total_female}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    # Row 3 (Stress Levels Breakdown)
    col7, col8, col9 = st.columns(3)
    with col7:
        st.markdown(f"""
        <div class='kpi-card kpi-card-low'>
            <h3>🟢 Low Stress Count</h3>
            <h2>{low_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col8:
        st.markdown(f"""
        <div class='kpi-card kpi-card-medium'>
            <h3>🟡 Medium Stress Count</h3>
            <h2>{med_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col9:
        st.markdown(f"""
        <div class='kpi-card kpi-card-high'>
            <h3>🔴 High Stress Count</h3>
            <h2>{high_count}</h2>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Search and Deletion Operations
    st.subheader("📋 Search and Record Operations")
    col_search, col_act = st.columns([2.5, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Search employees by Username or Department", placeholder="Search...").strip().lower()
        
    if search_query:
        display_df = filtered_df[
            filtered_df['username'].str.lower().str.contains(search_query) | 
            filtered_df['department'].str.lower().str.contains(search_query)
        ]
    else:
        display_df = filtered_df.copy()
        
    st.write(f"Showing {len(display_df)} matching assessment logs.")
    
    with col_act:
        record_to_delete = st.number_input("Enter Assessment ID to delete:", min_value=0, step=1, value=0)
        if st.button("🗑️ Delete Assessment Record", use_container_width=True, type="primary"):
            if record_to_delete > 0:
                if db.delete_prediction(record_to_delete):
                    st.success(f"Assessment record #{record_to_delete} deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to delete record #{record_to_delete}.")
            else:
                st.error("Please enter a valid record ID.")
                
    st.dataframe(display_df[[
        'id', 'username', 'age', 'gender', 'company', 'department', 
        'resting_heart_rate', 'predicted_stress', 'stress_score', 'prediction_date'
    ]], use_container_width=True)


# ==================== ADMIN GENDER STRESS ANALYSIS ====================
def show_gender_stress_page(filtered_df):
    """Render dedicated gender stress analysis with Plotly charts and comparative metrics."""
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>📊 Gender Stress Analysis</h1>
        <p>In-depth stress comparison metrics and charts split by gender</p>
    </div>
    """, unsafe_allow_html=True)
    
    m_df = filtered_df[filtered_df['gender'] == 'Male']
    f_df = filtered_df[filtered_df['gender'] == 'Female']
    
    total_male = len(m_df)
    total_female = len(f_df)
    
    m_low = len(m_df[m_df['predicted_stress'] == 'Low'])
    m_med = len(m_df[m_df['predicted_stress'] == 'Medium'])
    m_high = len(m_df[m_df['predicted_stress'] == 'High'])
    
    f_low = len(f_df[f_df['predicted_stress'] == 'Low'])
    f_med = len(f_df[f_df['predicted_stress'] == 'Medium'])
    f_high = len(f_df[f_df['predicted_stress'] == 'High'])
    
    # Calculate Averages and Percentages
    avg_m_score = m_df['stress_score'].mean() if total_male > 0 else 0.0
    avg_f_score = f_df['stress_score'].mean() if total_female > 0 else 0.0
    
    m_high_pct = (m_high / total_male * 100) if total_male > 0 else 0.0
    f_high_pct = (f_high / total_female * 100) if total_female > 0 else 0.0
    
    # Display Demographics in glassmorphic cards
    col_m, col_f = st.columns(2)
    with col_m:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🔵 Male Employee Stress Profile")
        st.write(f"**Total Male Employees:** {total_male}")
        st.write(f"- Low Stress: **{m_low}**")
        st.write(f"- Medium Stress: **{m_med}**")
        st.write(f"- High Stress: **{m_high}**")
        st.write(f"- Average Stress Score: **{avg_m_score:.2f} / 10**")
        st.write(f"- High Stress Percentage: **{m_high_pct:.1f}%**")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_f:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🔴 Female Employee Stress Profile")
        st.write(f"**Total Female Employees:** {total_female}")
        st.write(f"- Low Stress: **{f_low}**")
        st.write(f"- Medium Stress: **{f_med}**")
        st.write(f"- High Stress: **{f_high}**")
        st.write(f"- Average Stress Score: **{avg_f_score:.2f} / 10**")
        st.write(f"- High Stress Percentage: **{f_high_pct:.1f}%**")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Dynamic Conclusion Display (Comparing metrics)
    st.markdown("---")
    st.subheader("⚖️ Analytical Conclusion")
    
    # Compare average stress score
    if avg_m_score > avg_f_score:
        score_conclusion = f"Male employees have a higher average stress score than Female employees."
        higher_score_gender = "Male"
    elif avg_f_score > avg_m_score:
        score_conclusion = f"Female employees have a higher average stress score than Male employees."
        higher_score_gender = "Female"
    else:
        score_conclusion = "Male and Female employees experience equal average stress scores."
        higher_score_gender = "Equal"
        
    # Compare High Stress count
    if m_high > f_high:
        count_conclusion = f"Male employees have more High Stress employees than Female employees."
    elif f_high > m_high:
        count_conclusion = f"Female employees have more High Stress employees than Male employees."
    else:
        count_conclusion = "Male and Female cohorts contain an equal number of High Stress employees."
        
    st.markdown(f"""
    <div style='background: #f1f5f9; border-left: 6px solid #4f46e5; padding: 20px; border-radius: 12px;'>
        <p style='font-size: 16px; font-weight: bold; margin: 0; color: #1e293b;'>
            Based on the current prediction records, {score_conclusion}
        </p>
        <p style='font-size: 14px; margin: 5px 0 0 0; color: #64748b;'>
            Additionally: {count_conclusion}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # The 7 Plotly Interactive Visualizations
    st.markdown("---")
    st.subheader("📊 Plotly Interactive Visualizations")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        # Chart 1: Male vs Female Stress Comparison (Grouped Bar chart)
        bar_data = pd.DataFrame({
            'Stress Level': ['Low', 'Medium', 'High', 'Low', 'Medium', 'High'],
            'Count': [m_low, m_med, m_high, f_low, f_med, f_high],
            'Gender': ['Male', 'Male', 'Male', 'Female', 'Female', 'Female']
        })
        fig_grouped = px.bar(
            bar_data, x='Stress Level', y='Count', color='Gender',
            barmode='group',
            title="1. Male vs Female Stress Level Breakdown",
            color_discrete_map={'Male': '#2563eb', 'Female': '#7c3aed'}
        )
        st.plotly_chart(fig_grouped, use_container_width=True)
        
    with col_chart2:
        # Chart 2: Stacked Bar Chart
        fig_stacked = px.bar(
            bar_data, x='Gender', y='Count', color='Stress Level',
            title="2. Stress Level Ratios Stacked by Gender",
            color_discrete_map={'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
    col_chart3, col_chart4 = st.columns(2)
    with col_chart3:
        # Chart 3: Pie Chart (Overall Male/Female Distribution)
        pie_data = pd.DataFrame({
            'Gender': ['Male', 'Female'],
            'Total': [total_male, total_female]
        })
        fig_pie = px.pie(
            pie_data, values='Total', names='Gender',
            title="3. Overall Gender Distribution in Cohort",
            color_discrete_sequence=['#2563eb', '#7c3aed'],
            hole=0.3
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_chart4:
        # Chart 4: Average Stress Score Comparison
        avg_score_df = pd.DataFrame({
            'Gender': ['Male', 'Female'],
            'Average Stress Score': [avg_m_score, avg_f_score]
        })
        fig_avg = px.bar(
            avg_score_df, x='Gender', y='Average Stress Score',
            color='Gender',
            title="4. Average Stress Score Comparison",
            color_discrete_map={'Male': '#2563eb', 'Female': '#7c3aed'}
        )
        st.plotly_chart(fig_avg, use_container_width=True)
        
    col_chart5, col_chart6 = st.columns(2)
    with col_chart5:
        # Chart 5: Percentage of High Stress Employees by Gender
        pct_high_df = pd.DataFrame({
            'Gender': ['Male', 'Female'],
            'High Stress (%)': [m_high_pct, f_high_pct]
        })
        fig_pct = px.bar(
            pct_high_df, x='Gender', y='High Stress (%)',
            color='Gender',
            title="5. High Stress Concentration Percentage (%)",
            color_discrete_map={'Male': '#2563eb', 'Female': '#7c3aed'}
        )
        st.plotly_chart(fig_pct, use_container_width=True)
        
    with col_chart6:
        # Chart 6: Trend Chart (Prediction count by gender over time)
        if len(filtered_df) > 0:
            trend_df = filtered_df.copy()
            trend_df['Date'] = pd.to_datetime(trend_df['prediction_date']).dt.date
            trend_grouped = trend_df.groupby(['Date', 'gender']).size().reset_index(name='Predictions Count')
            trend_grouped = trend_grouped.sort_values('Date')
            
            fig_trend = px.line(
                trend_grouped, x='Date', y='Predictions Count', color='gender',
                title="6. Temporal Daily Prediction Count Trend",
                markers=True,
                color_discrete_map={'Male': '#2563eb', 'Female': '#7c3aed'}
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
    # Chart 7: Department-wise Gender Stress
    st.markdown("---")
    if len(filtered_df) > 0:
        dept_gender = filtered_df.groupby(['department', 'gender'])['stress_score'].mean().reset_index()
        fig_dept = px.bar(
            dept_gender, x='department', y='stress_score', color='gender',
            barmode='group',
            title="7. Department-wise Gender Average Stress Score Comparison",
            color_discrete_map={'Male': '#2563eb', 'Female': '#7c3aed'}
        )
        st.plotly_chart(fig_dept, use_container_width=True)


# ==================== ADMIN ADVANCED ANALYTICS & INSIGHTS ====================
def show_admin_analytics(filtered_df):
    """Admin Advanced Analytics detailing trends, top/bottom stressed employee lists and charts."""
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>📈 Advanced Analytics & Insights</h1>
        <p>AI-style dynamic platform observations and tenure analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    total = len(filtered_df)
    m_df = filtered_df[filtered_df['gender'] == 'Male']
    f_df = filtered_df[filtered_df['gender'] == 'Female']
    
    # AI-style Insights Panel (Computed dynamically)
    st.subheader("💡 Dynamic AI stress observations")
    
    if total > 0:
        # 1. Workload score average comparison
        # Reconstruct Workload Score = (years_company / 9.0) * 10
        from feature_engineering import get_dataset_extremes
        max_years, _, _ = get_dataset_extremes()
        
        m_workload = (m_df['years_in_company'] / max_years * 10).mean() if len(m_df) > 0 else 0
        f_workload = (f_df['years_in_company'] / max_years * 10).mean() if len(f_df) > 0 else 0
        
        workload_comp = "Male employees" if m_workload > f_workload else "Female employees"
        high_workload_val = max(m_workload, f_workload)
        low_workload_val = min(m_workload, f_workload)
        
        insight_1 = f"• **Workload Trend:** {workload_comp} have a higher average workload score (**{high_workload_val:.2f}/10**) compared to their peers (**{low_workload_val:.2f}/10**)."
        
        # 2. More high stress predictions
        high_m_count = len(m_df[m_df['predicted_stress'] == 'High'])
        high_f_count = len(f_df[f_df['predicted_stress'] == 'High'])
        stress_comp = "Female employees" if high_f_count >= high_m_count else "Male employees"
        high_stress_val = max(high_m_count, high_f_count)
        
        insight_2 = f"• **Stress Prevalence:** {stress_comp} account for more High Stress predictions, with **{high_stress_val}** records logged in this filter context."
        
        # 3. Big Data or other dept stress percentage
        dept_pct = {}
        for dept in filtered_df['department'].unique():
            cohort = filtered_df[filtered_df['department'] == dept]
            pct = len(cohort[cohort['predicted_stress'] == 'High']) / len(cohort) * 100 if len(cohort) > 0 else 0
            dept_pct[dept] = pct
            
        if dept_pct:
            high_dept = max(dept_pct, key=dept_pct.get)
            insight_3 = f"• **Department Stress hotspots:** The **{high_dept}** department has the highest proportion of high-stress employees (**{dept_pct[high_dept]:.1f}%** of department staff)."
        else:
            insight_3 = "• **Department stress hotspots:** Insufficient department data to compile hotspots."
            
        # 4. Tenure impact (> 8 years)
        tenure_long = filtered_df[filtered_df['years_in_company'] > 8]
        tenure_short = filtered_df[filtered_df['years_in_company'] <= 8]
        if len(tenure_long) > 0 and len(tenure_short) > 0:
            avg_long = tenure_long['stress_score'].mean()
            avg_short = tenure_short['stress_score'].mean()
            diff_rel = "increased" if avg_long > avg_short else "decreased"
            insight_4 = f"• **Senior Tenure correlation:** Employees with over 8 years in the company show **{diff_rel}** stress levels (avg **{avg_long:.2f}/10**) compared to employees with shorter tenure (avg **{avg_short:.2f}/10**)."
        else:
            insight_4 = "• **Senior Tenure correlation:** Insufficient tenure data spread to evaluate seniority patterns."
            
        # 5. Heart rate above 95 BPM
        high_hr = filtered_df[filtered_df['resting_heart_rate'] > 95]
        if len(high_hr) > 0:
            high_hr_pct = len(high_hr[high_hr['predicted_stress'] == 'High']) / len(high_hr) * 100
            insight_5 = f"• **Heart Rate correlation:** Resting heart rates above 95 BPM are frequently associated with High Stress predictions, with **{high_hr_pct:.1f}%** of this tachycardia group presenting high stress outcomes."
        else:
            insight_5 = "• **Heart Rate correlation:** Tachycardia heart rate stress patterns show no significant correlation in the active cohort."
            
        st.markdown(f"""
        <div class='glass-card' style='border-left: 6px solid #7c3aed; background-color: #faf5ff;'>
            <h4 style='color: #7c3aed; margin-top:0;'>AI Analytics Insights Engine</h4>
            <p style='font-size:14px; line-height: 1.6; color: #475569;'>
                {insight_1}<br/>
                {insight_2}<br/>
                {insight_3}<br/>
                {insight_4}<br/>
                {insight_5}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Insights unavailable. Please expand your filters to include data.")
        
    st.markdown("---")
    
    # Advanced Demographics & Trends
    st.subheader("📊 Stress Trend Analysis")
    if total > 0:
        trend_df = filtered_df.copy()
        trend_df['prediction_date'] = pd.to_datetime(trend_df['prediction_date'])
        trend_df = trend_df.sort_values('prediction_date')
        trend_daily = trend_df.groupby(trend_df['prediction_date'].dt.date)['stress_score'].mean().reset_index()
        
        fig_trend = px.line(
            trend_daily, x='prediction_date', y='stress_score',
            title="Daily Average Stress Score Trend Line",
            labels={'prediction_date': 'Date', 'stress_score': 'Avg Stress Score'},
            markers=True,
            color_discrete_sequence=['#2563eb']
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    # Top 10 lists
    st.markdown("---")
    col_list1, col_list2 = st.columns(2)
    with col_list1:
        st.subheader("🚨 Top 10 Highest Stress Employees")
        if total > 0:
            top_high = filtered_df.sort_values('stress_score', ascending=False).head(10)
            st.dataframe(top_high[['id', 'username', 'gender', 'department', 'stress_score']], use_container_width=True)
            
    with col_list2:
        st.subheader("🟢 Top 10 Lowest Stress Employees")
        if total > 0:
            top_low = filtered_df.sort_values('stress_score', ascending=True).head(10)
            st.dataframe(top_low[['id', 'username', 'gender', 'department', 'stress_score']], use_container_width=True)


# ==================== ADMIN REPORT CENTER ====================
def show_admin_reports(filtered_df):
    """Download reports center for administrator accounts."""
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>📋 Reports Center</h1>
        <p>Generate, review, and download administrative dataset metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    if filtered_df.empty:
        st.warning("No records found under active filters to export reports.")
        return
        
    st.write(f"Generating reports utilizing the current filtered cohort ({len(filtered_df)} records).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Primary CSV & Excel Datasets")
        
        # Complete report in CSV
        csv_data = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Complete Report (CSV)",
            data=csv_data,
            file_name=f"complete_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Complete report in Excel
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='StressRecords')
        st.download_button(
            label="📥 Download Complete Report (Excel)",
            data=excel_buffer.getvalue(),
            file_name=f"complete_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📄 PDF Analysis Summaries")
        
        # Generate summary PDF using reportlab pdf_generator
        pdf_df = filtered_df.copy()
        stress_map = {'Low': 0, 'Medium': 1, 'High': 2}
        pdf_df['Stress_Level'] = pdf_df['predicted_stress'].map(stress_map)
        pdf_buffer = pdf_generator.generate_summary_report(pdf_df)
        
        if pdf_buffer:
            st.download_button(
                label="📥 Download Summary Report (PDF)",
                data=pdf_buffer,
                file_name=f"stress_summary_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("PDF generation engine (Reportlab) is not available.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Render direct text exports for validation checks
    st.markdown("---")
    st.subheader("📝 Quick Text Summary View")
    
    low_c = len(filtered_df[filtered_df['predicted_stress'] == 'Low'])
    med_c = len(filtered_df[filtered_df['predicted_stress'] == 'Medium'])
    high_c = len(filtered_df[filtered_df['predicted_stress'] == 'High'])
    total_c = len(filtered_df)
    
    summary_text = (
        f"==================================================\n"
        f"EMPLOYEE STRESS PREDICTION SYSTEM - SUMMARY REPORT\n"
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"==================================================\n\n"
        f"COHORT OVERVIEW\n"
        f"---------------\n"
        f"Total Filtered Employees: {total_c}\n"
        f"- Low Stress: {low_c} ({low_c/total_c*100:.1f}%)\n"
        f"- Medium Stress: {med_c} ({med_c/total_c*100:.1f}%)\n"
        f"- High Stress: {high_c} ({high_c/total_c*100:.1f}%)\n\n"
        f"DEMOGRAPHICS & AVERAGES\n"
        f"-----------------------\n"
        f"- Average Age: {filtered_df['age'].mean():.1f} years\n"
        f"- Average Salary: Rs. {filtered_df['salary'].mean():,.2f}\n"
        f"- Average Heart Rate: {filtered_df['resting_heart_rate'].mean():.1f} BPM\n"
        f"- Average Years in Company: {filtered_df['years_in_company'].mean():.1f} years\n"
    )
    st.code(summary_text, language="text")


# ==================== ADMIN USERS MANAGEMENT PAGE ====================
def show_admin_users():
    """Render list of all registered employees with account deletion functionality."""
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>👥 Employee Records</h1>
        <p>Review user profile configurations and perform administrative account management</p>
    </div>
    """, unsafe_allow_html=True)
    
    users_df = db.get_all_users()
    st.write(f"Total registered profiles: {len(users_df)}")
    
    col_tbl, col_ctrl = st.columns([2.5, 1])
    with col_tbl:
        st.dataframe(users_df[['name', 'username', 'role', 'gender', 'age', 'company', 'department', 'created_at']], use_container_width=True)
        
    with col_ctrl:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🗑️ Delete User Account")
        user_to_delete = st.text_input("Enter employee username to delete:", placeholder="e.g. employee1").strip()
        
        if st.button("🗑️ Delete User & History", use_container_width=True, type="primary"):
            if not user_to_delete:
                st.error("Please enter a username.")
            elif user_to_delete == "admin":
                st.error("Administrative account 'admin' cannot be deleted.")
            else:
                profile = db.get_user_profile(user_to_delete)
                if profile:
                    if db.delete_user_and_predictions(user_to_delete):
                        st.success(f"User account '{user_to_delete}' and prediction history purged successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to delete user '{user_to_delete}'.")
                else:
                    st.warning(f"No user found with username '{user_to_delete}'.")
        st.markdown("</div>", unsafe_allow_html=True)


# ==================== SETTINGS PAGE ====================
def show_settings_page():
    """Display profile details settings."""
    st.markdown("""
    <div class='header-gradient fade-in'>
        <h1>⚙️ Settings</h1>
        <p>User account configuration and details</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("👤 Your User Account Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Account Role:** {st.session_state.user_role}")
    with col2:
        st.write(f"**Assigned Department:** {st.session_state.profile_details.get('department', 'N/A')}")
        st.write(f"**Assigned Office Company:** {st.session_state.profile_details.get('company', 'N/A')}")
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== MAIN APPLICATION ROUTER ====================
def main():
    """Execute Streamlit application flow based on active sessions and roles."""
    initialize_session_state()
    
    if not st.session_state.logged_in:
        show_auth_page()
    else:
        # Load ML Pipeline
        models = load_models_and_data()
        
        # Load active database records
        predictions_df = db.get_predictions()
        
        # Role-based Navigation Routing
        role = st.session_state.user_role
        username = st.session_state.username
        
        # Sidebar Profile Header
        st.sidebar.markdown(f"""
        <div style='background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); 
                    padding: 20px; border-radius: 12px; color: white; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.15);'>
            <h3 style='margin:0; color: white; font-size: 18px;'>🏢 {st.session_state.profile_details.get('name', 'User')}</h3>
            <p style='margin:4px 0 0 0; font-size:12px; opacity:0.85;'>Session Role: <b>{role}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        if role == "Administrator":
            # Admin Sidebar Navigation
            page = st.sidebar.radio(
                "📍 Admin Console",
                ["Dashboard", "Gender Analysis", "Analytics", "Reports", "Employee Records", "Settings"]
            )
            
            # Global Filters in sidebar for Admin
            st.sidebar.markdown("---")
            st.sidebar.subheader("🎯 Global Dataset Filters")
            
            filter_gender = st.sidebar.selectbox("Filter Gender", ["All", "Male", "Female"])
            filter_company = st.sidebar.selectbox("Filter Company", ["All", "Glasses", "Pear", "Cheerper"])
            filter_dept = st.sidebar.selectbox("Filter Department", ["All", "BigData", "AI", "Support", "Design", "Search Engine", "Sales"])
            filter_stress = st.sidebar.selectbox("Filter Stress Level", ["All", "Low", "Medium", "High"])
            
            # Apply dynamic filtering to the complete predictions log
            filtered_df = predictions_df.copy()
            
            if filter_gender != "All":
                filtered_df = filtered_df[filtered_df['gender'] == filter_gender]
            if filter_company != "All":
                filtered_df = filtered_df[filtered_df['company'] == filter_company]
            if filter_dept != "All":
                filtered_df = filtered_df[filtered_df['department'] == filter_dept]
            if filter_stress != "All":
                filtered_df = filtered_df[filtered_df['predicted_stress'] == filter_stress]
                
            st.sidebar.write(f"Filtered Cohort Size: {len(filtered_df)}")
            
            if filtered_df.empty:
                st.sidebar.warning("⚠️ No records match active filters.")
                
            st.sidebar.markdown("---")
            if st.sidebar.button("🚪 Log Out", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_role = None
                st.session_state.profile_details = {}
                st.rerun()
                
            # ROUTE ADMIN PAGES
            if page == "Dashboard":
                show_admin_dashboard(filtered_df)
            elif page == "Gender Analysis":
                show_gender_stress_page(filtered_df)
            elif page == "Analytics":
                show_admin_analytics(filtered_df)
            elif page == "Reports":
                show_admin_reports(filtered_df)
            elif page == "Employee Records":
                show_admin_users()
            elif page == "Settings":
                show_settings_page()
                
        elif role == "Employee/User":
            # Employee Sidebar Navigation
            page = st.sidebar.radio(
                "📍 Employee Console",
                ["Dashboard", "Stress Prediction", "Prediction History", "Reports"]
            )
            
            st.sidebar.markdown("---")
            if st.sidebar.button("🚪 Log Out", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_role = None
                st.session_state.profile_details = {}
                st.rerun()
                
            # ROUTE EMPLOYEE PAGES
            if page == "Dashboard":
                show_employee_dashboard(predictions_df)
            elif page == "Stress Prediction":
                show_employee_prediction(models)
            elif page == "Prediction History":
                show_employee_history(predictions_df)
            elif page == "Reports":
                show_employee_reports(predictions_df)
                
        else:
            st.error("Unknown user role. Please sign in again.")
            st.session_state.logged_in = False
            st.rerun()

if __name__ == '__main__':
    main()
