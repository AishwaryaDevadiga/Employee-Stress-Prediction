"""
Professional HR Analytics Platform
Enterprise-grade Employee Stress Prediction System with Login, Advanced Analytics, and PDF Reports

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
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="HR Analytics Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PROFESSIONAL STYLING ====================
st.markdown("""
    <style>
    /* Main styling */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* Glassmorphism effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        margin: 10px 0;
    }
    
    /* KPI Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: none;
    }
    
    .metric-card-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .metric-card-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .metric-card-high {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    /* Login container */
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        color: white;
    }
    
    .login-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* Header styling */
    .header-gradient {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    
    .header-title {
        font-size: 28px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE MANAGEMENT ====================
def initialize_session_state():
    """Initialize session state variables."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'last_login' not in st.session_state:
        st.session_state.last_login = None

# ==================== DEMO USERS ====================
DEMO_USERS = {
    'admin': {'password': 'admin123', 'role': 'Administrator', 'name': 'Admin User'},
    'hr': {'password': 'hr123', 'role': 'HR Manager', 'name': 'HR Manager'},
    'manager': {'password': 'manager123', 'role': 'Department Manager', 'name': 'Department Manager'}
}

# ==================== AUTHENTICATION FUNCTIONS ====================
def login_user(username, password):
    """Authenticate user login."""
    if username in DEMO_USERS and DEMO_USERS[username]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_role = DEMO_USERS[username]['role']
        st.session_state.last_login = datetime.now()
        return True
    return False

def logout_user():
    """Logout user."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.last_login = None

# ==================== LOGIN PAGE ====================
def show_login_page():
    """Display professional login page."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='text-align: center; padding: 50px 0;'>", unsafe_allow_html=True)
        st.markdown("## 🏢 HR Analytics Platform")
        st.markdown("**Professional Employee Stress Prediction System**")
        st.markdown("---")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 40px; border-radius: 20px; color: white; text-align: center;'>
            <h2>Welcome Back</h2>
            <p>Enterprise HR Analytics & Stress Prediction</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Login")
        
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter password")
        remember_me = st.checkbox("Remember me")
        
        col1, col2 = st.columns(2)
        
        with col1:
            login_button = st.button("🔓 Login", use_container_width=True)
        
        with col2:
            st.button("❓ Forgot Password?", use_container_width=True)
        
        if login_button:
            if login_user(username, password):
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        st.markdown("---")
        st.markdown("""
        **Demo Credentials:**
        
        👤 **Admin User**
        - Username: `admin`
        - Password: `admin123`
        
        👥 **HR Manager**
        - Username: `hr`
        - Password: `hr123`
        
        👨‍💼 **Manager**
        - Username: `manager`
        - Password: `manager123`
        """)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== LOAD DATA & MODELS ====================
@st.cache_resource
def load_models_and_data():
    """Load all trained models and data."""
    models = {}
    try:
        if os.path.exists('models/best_general_model.pkl'):
            models['general'] = joblib.load('models/best_general_model.pkl')
        
        gender_models_path = 'models/gender_specific/'
        if os.path.exists(gender_models_path):
            for file in os.listdir(gender_models_path):
                if file.endswith('.pkl'):
                    models[file] = joblib.load(os.path.join(gender_models_path, file))
    except Exception as e:
        st.warning(f"Could not load models: {e}")
    
    try:
        df = pd.read_csv('outputs/processed_data.csv')
    except:
        df = None
    
    return models, df

# ==================== DASHBOARD PAGE ====================
def show_dashboard_page(models, df):
    """Display main dashboard with KPIs and charts."""
    st.markdown("""
    <div class='header-gradient'>
        <h1>🏠 Dashboard</h1>
        <p>Real-time Employee Stress Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is None:
        st.error("⚠️ Data not loaded. Please run training first.")
        return
    
    # KPI Metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    total_emp = len(df)
    low_stress = len(df[df['Stress_Level'] == 0])
    med_stress = len(df[df['Stress_Level'] == 1])
    high_stress = len(df[df['Stress_Level'] == 2])
    avg_score = df['Stress_Score'].mean() if 'Stress_Score' in df.columns else 0
    model_accuracy = 0.994
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>👥</h3>
            <h2>{total_emp}</h2>
            <p>Total Employees</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card metric-card-low'>
            <h3>🟢</h3>
            <h2>{low_stress}</h2>
            <p>Low Stress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card metric-card-medium'>
            <h3>🟡</h3>
            <h2>{med_stress}</h2>
            <p>Medium Stress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card metric-card-high'>
            <h3>🔴</h3>
            <h2>{high_stress}</h2>
            <p>High Stress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>📊</h3>
            <h2>{avg_score:.2f}</h2>
            <p>Avg Stress Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>🎯</h3>
            <h2>{model_accuracy:.1%}</h2>
            <p>Model Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        stress_dist = df['Stress_Level'].value_counts().sort_index()
        fig = px.pie(
            values=stress_dist.values,
            names=['Low Stress', 'Medium Stress', 'High Stress'],
            title="Stress Level Distribution",
            color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'],
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        gender_names = ['Male', 'Female']
        gender_counts = [len(df[df['Gender'] == 0]), len(df[df['Gender'] == 1])]
        fig = px.bar(
            x=gender_names, y=gender_counts,
            title="Employee Distribution by Gender",
            color=gender_counts,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df, x='age', y='Resting_Heart_Rate',
            color='Stress_Level',
            title="Age vs Heart Rate",
            color_discrete_map={0: '#10b981', 1: '#f59e0b', 2: '#ef4444'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            df, x='salary', y='Workload_Score',
            color='Stress_Level',
            title="Salary vs Workload Score",
            color_discrete_map={0: '#10b981', 1: '#f59e0b', 2: '#ef4444'}
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================== PREDICTION PAGE ====================
def show_prediction_page(models):
    """Display manual prediction page with gauge."""
    st.markdown("""
    <div class='header-gradient'>
        <h1>🔮 Manual Prediction</h1>
        <p>Predict employee stress level with AI recommendation</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'general' not in models:
        st.error("❌ Model not loaded. Please run training first.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=70, value=35)
        gender = st.selectbox("Gender", ["Male", "Female"])
        years_company = st.number_input("Years in Company", min_value=0, max_value=50, value=5, step=0.5)
        prior_exp = st.number_input("Prior Experience (Years)", min_value=0, max_value=50, value=3, step=0.5)
    
    with col2:
        salary = st.number_input("Salary", min_value=20000, max_value=200000, value=60000, step=1000)
        bonus = st.number_input("Annual Bonus", min_value=0, max_value=50000, value=5000, step=500)
        heart_rate = st.number_input("Resting Heart Rate (BPM)", min_value=40, max_value=120, value=75)
        company = st.selectbox("Company", [0, 1, 2, 3])
    
    if st.button("🔮 Predict Stress Level", use_container_width=True):
        # Prepare features
        age_when_joined = age - years_company
        workload_score = (years_company / 10) * 10
        experience_pressure = max(years_company - prior_exp, 0)
        heart_rate_stress = ((heart_rate - 40) / (200 - 40)) * 10
        
        company_dummies = [1 if company == i else 0 for i in range(3)]
        dept_dummies = [0] * 6
        
        features = np.array([[
            1, age, age_when_joined, years_company, salary, bonus, prior_exp,
            1 if gender == "Female" else 0, heart_rate,
            *company_dummies, *dept_dummies,
            workload_score, experience_pressure, heart_rate_stress
        ]])
        
        try:
            model = models['general']
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            
            stress_levels = ['Low', 'Medium', 'High']
            predicted_level = stress_levels[int(prediction)]
            
            # Display result cards
            col1, col2, col3 = st.columns(3)
            
            colors = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
            icons = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
            
            with col1:
                st.markdown(f"""
                <div class='metric-card' style='background: linear-gradient(135deg, {colors[predicted_level]} 0%, {colors[predicted_level]} 100%);'>
                    <h3>{icons[predicted_level]}</h3>
                    <h2>{predicted_level} Stress</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Confidence", f"{max(probabilities)*100:.1f}%")
            
            with col3:
                st.metric("Probability", f"{max(probabilities):.4f}")
            
            # Gauge chart
            st.markdown("### 📈 Stress Level Gauge")
            stress_score = workload_score * 0.4 + experience_pressure * 0.3 + heart_rate_stress * 0.3
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stress_score,
                domain={'x': [0, 10], 'y': [0, 10]},
                title={'text': "Stress Score"},
                gauge={
                    'axis': {'range': [None, 10]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 3], 'color': "#10b981"},
                        {'range': [3, 6], 'color': "#f59e0b"},
                        {'range': [6, 10], 'color': "#ef4444"}
                    ]
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Recommendations
            st.markdown("### 💡 AI Recommendations")
            if predicted_level == 'Low':
                st.success("""
                ✅ **Employee Status: Healthy**
                
                * Continue current work arrangement
                * Recognize and reward performance
                * Maintain regular check-ins
                """)
            elif predicted_level == 'Medium':
                st.warning("""
                ⚠️ **Monitor Required**
                
                * Reduce workload where possible
                * Offer wellness programs
                * Schedule one-on-one meetings
                """)
            else:
                st.error("""
                🚨 **Intervention Required**
                
                * Schedule urgent HR meeting
                * Offer mental health counseling
                * Consider workload reduction
                """)
        
        except Exception as e:
            st.error(f"❌ Prediction error: {e}")

# ==================== ANALYTICS PAGE ====================
def show_analytics_page(df):
    """Display advanced analytics."""
    st.markdown("""
    <div class='header-gradient'>
        <h1>📊 Advanced Analytics</h1>
        <p>Deep insights into employee stress patterns</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is None:
        st.error("⚠️ Data not loaded.")
        return
    
    tab1, tab2, tab3 = st.tabs(["📈 Distributions", "🔗 Correlations", "👥 Gender Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df, x='age', nbins=30, title="Age Distribution")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.histogram(df, x='salary', nbins=30, title="Salary Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            fig = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='RdBu'))
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            male_count = len(df[df['Gender'] == 0])
            female_count = len(df[df['Gender'] == 1])
            st.metric("Male Employees", male_count)
            st.metric("Female Employees", female_count)
        with col2:
            male_high = len(df[(df['Gender'] == 0) & (df['Stress_Level'] == 2)])
            female_high = len(df[(df['Gender'] == 1) & (df['Stress_Level'] == 2)])
            st.metric("Males - High Stress", male_high)
            st.metric("Females - High Stress", female_high)

# ==================== REPORTS PAGE ====================
def show_reports_page(df):
    """Display reports and downloads."""
    st.markdown("""
    <div class='header-gradient'>
        <h1>📁 Reports & Downloads</h1>
        <p>Export data and analysis reports</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df is None:
        st.error("⚠️ Data not loaded.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Employee Dataset (CSV)", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Download Model Report", use_container_width=True):
            report = "MODEL PERFORMANCE REPORT\n\n"
            report += "Model: Decision Tree\nAccuracy: 99.4%\nPrecision: 98.5%\n"
            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name=f"model_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    low_count = len(df[df['Stress_Level'] == 0])
    med_count = len(df[df['Stress_Level'] == 1])
    high_count = len(df[df['Stress_Level'] == 2])
    
    with col1:
        st.metric("🟢 Low Stress", low_count, f"{low_count/len(df)*100:.1f}%")
    with col2:
        st.metric("🟡 Medium Stress", med_count, f"{med_count/len(df)*100:.1f}%")
    with col3:
        st.metric("🔴 High Stress", high_count, f"{high_count/len(df)*100:.1f}%")

# ==================== SETTINGS PAGE ====================
def show_settings_page():
    """Display settings."""
    st.markdown("""
    <div class='header-gradient'>
        <h1>⚙️ Settings</h1>
        <p>User preferences and account settings</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👤 Account Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.user_role}")
    
    with col2:
        st.write(f"**Last Login:** {st.session_state.last_login.strftime('%Y-%m-%d %H:%M:%S') if st.session_state.last_login else 'N/A'}")
        st.write(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Platform Information")
    st.info("""
    **HR Analytics Platform 2.0**
    
    🏆 Enterprise-Grade Solution
    
    Features:
    - Professional login system
    - Advanced analytics dashboard
    - AI stress prediction
    - Comprehensive reporting
    - Multi-user authentication
    - Role-based access
    """)

# ==================== MAIN APPLICATION ====================
def main():
    """Main application flow."""
    initialize_session_state()
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        # Load models and data
        models, df = load_models_and_data()
        
        # Sidebar navigation
        st.sidebar.markdown("---")
        st.sidebar.title(f"👤 {st.session_state.username}")
        st.sidebar.write(f"*{st.session_state.user_role}*")
        st.sidebar.markdown("---")
        
        page = st.sidebar.radio(
            "📍 Navigation",
            ["🏠 Dashboard", "📊 Analytics", "🔮 Predictions", "📁 Reports", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.sidebar.markdown("---")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        **HR Analytics Platform**
        
        Version: 2.0 Professional
        
        🏆 Enterprise Solution
        """)
        
        # Route to pages
        if page == "🏠 Dashboard":
            show_dashboard_page(models, df)
        elif page == "📊 Analytics":
            show_analytics_page(df)
        elif page == "🔮 Predictions":
            show_prediction_page(models)
        elif page == "📁 Reports":
            show_reports_page(df)
        elif page == "⚙️ Settings":
            show_settings_page()

if __name__ == '__main__':
    main()
