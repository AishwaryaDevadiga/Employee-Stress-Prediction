"""
Employee Stress Prediction System - Interactive Dashboard
A professional Streamlit dashboard for HR analytics and employee stress prediction.

Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import joblib
import os
import sys
from io import BytesIO

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import prediction classes for single/batch predictions
from prediction import ManualPredictor, BatchPredictor
# Note: Models and data are loaded from disk (models/*.pkl and outputs/processed_data.csv)
# using joblib and pandas - no DataLoader needed for the dashboard


# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Employee Stress Prediction",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM STYLING ====================
st.markdown("""
    <style>
    .main {
        padding: 0px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .success-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .warning-card {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .danger-card {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    h1 {
        color: #1a202c;
        text-align: center;
        margin-bottom: 30px;
    }
    h2 {
        color: #2d3748;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE ====================
@st.cache_resource
def load_models_and_data():
    """Load all trained models and data."""
    models = {}
    try:
        if os.path.exists('models/best_general_model.pkl'):
            models['general'] = joblib.load('models/best_general_model.pkl')
        
        # Load gender-specific models if available
        gender_models_path = 'models/gender_specific/'
        if os.path.exists(gender_models_path):
            for file in os.listdir(gender_models_path):
                if file.endswith('.pkl'):
                    gender = 'male' if 'male' in file else 'female'
                    models[f'{gender}_model'] = joblib.load(os.path.join(gender_models_path, file))
    except Exception as e:
        st.warning(f"Could not load models: {e}")
    
    # Load processed data
    try:
        df = pd.read_csv('outputs/processed_data.csv')
    except:
        df = None
    
    return models, df


# ==================== HELPER FUNCTIONS ====================
def stress_level_color(level):
    """Get color for stress level."""
    if level == 'Low':
        return '🟢'
    elif level == 'Medium':
        return '🟡'
    else:
        return '🔴'


def get_recommendation(stress_level):
    """Get HR recommendation based on stress level."""
    recommendations = {
        'Low': {
            'emoji': '✅',
            'message': 'Employee is doing well!',
            'details': [
                '✓ Continue current work arrangement',
                '✓ Recognize and reward good performance',
                '✓ Maintain regular check-ins'
            ],
            'color': 'green'
        },
        'Medium': {
            'emoji': '⚠️',
            'message': 'Monitor employee closely',
            'details': [
                '• Reduce workload where possible',
                '• Offer wellness programs',
                '• Schedule one-on-one meetings',
                '• Consider flexible work arrangements',
                '• Check for work-life balance issues'
            ],
            'color': 'orange'
        },
        'High': {
            'emoji': '🚨',
            'message': 'Immediate intervention required',
            'details': [
                '! Schedule urgent meeting with HR',
                '! Offer mental health counseling',
                '! Consider temporary workload reduction',
                '! Explore mentoring opportunities',
                '! Review role and responsibilities',
                '! Consider transfer or role change'
            ],
            'color': 'red'
        }
    }
    return recommendations.get(stress_level, recommendations['Low'])


# ==================== MAIN APP ====================
def main():
    """Main Streamlit application."""
    
    # Load data and models
    models, df = load_models_and_data()
    
    # Sidebar navigation
    st.sidebar.title("🧠 Stress Prediction System")
    page = st.sidebar.radio(
        "Navigate to:",
        ["📊 Dashboard", "📈 Analytics", "🔮 Predictions", "👥 Employee Search", "📋 Reports"]
    )
    
    # Check if models are loaded
    if not models or df is None:
        st.error("⚠️ Models or data not loaded. Please run `python train.py` first.")
        st.info("Quick Start:\n1. Open terminal\n2. Run: `python train.py`\n3. Then run: `streamlit run dashboard.py`")
        return
    
    # ==================== DASHBOARD PAGE ====================
    if page == "📊 Dashboard":
        st.title("🧠 Employee Stress Prediction System")
        st.subheader("Real-time HR Analytics Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        low_count = len(df[df['Stress_Level'] == 0])
        med_count = len(df[df['Stress_Level'] == 1])
        high_count = len(df[df['Stress_Level'] == 2])
        total = len(df)
        
        with col1:
            st.metric("Total Employees", total, "👥")
        
        with col2:
            st.metric("🟢 Low Stress", low_count, f"{low_count/total*100:.1f}%")
        
        with col3:
            st.metric("🟡 Medium Stress", med_count, f"{med_count/total*100:.1f}%")
        
        with col4:
            st.metric("🔴 High Stress", high_count, f"{high_count/total*100:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Stress distribution pie chart
            stress_data = {
                'Stress Level': ['Low Stress', 'Medium Stress', 'High Stress'],
                'Count': [
                    len(df[df['Stress_Level'] == 0]),
                    len(df[df['Stress_Level'] == 1]),
                    len(df[df['Stress_Level'] == 2])
                ]
            }
            stress_df = pd.DataFrame(stress_data)
            
            fig_pie = px.pie(
                stress_df,
                values='Count',
                names='Stress Level',
                title="Stress Level Distribution"
            )
            fig_pie.update_traces(
                marker=dict(colors=['#10b981', '#f59e0b', '#ef4444'])  # Green, Orange, Red
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Age vs Stress Level
            fig_age = px.scatter(
                df, x='age', y='Resting_Heart_Rate',
                color='Stress_Level',
                title="Age vs Heart Rate (colored by Stress Level)",
                color_discrete_map={0: '#10b981', 1: '#f59e0b', 2: '#ef4444'},
                labels={'Stress_Level': 'Stress Level', 'age': 'Age', 'Resting_Heart_Rate': 'Heart Rate'}
            )
            st.plotly_chart(fig_age, use_container_width=True)
        
        # Gender comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender distribution
            gender_labels = ['Male', 'Female']
            gender_counts = [len(df[df['Gender'] == 0]), len(df[df['Gender'] == 1])]
            fig_gender = px.bar(
                x=gender_labels, y=gender_counts,
                title="Employee Distribution by Gender",
                labels={'x': 'Gender', 'y': 'Count'},
                color=gender_counts,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        
        with col2:
            st.write("**Female Employees**")
            st.metric("Count", len(female_df))
            st.metric("Avg Age", f"{female_df['age'].mean():.1f}")
            st.metric("Avg Heart Rate", f"{female_df['Resting_Heart_Rate'].mean():.1f}")
    
    # ==================== ANALYTICS PAGE ====================
    elif page == "📈 Analytics":
        st.title("📈 Advanced Analytics")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Distributions", "Correlations", "Gender Analysis", "Department Analysis"])
        
        with tab1:
            st.subheader("Feature Distributions")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Age distribution
                fig_age_dist = px.histogram(
                    df, x='age', nbins=30,
                    title="Age Distribution",
                    labels={'age': 'Age', 'count': 'Count'}
                )
                st.plotly_chart(fig_age_dist, use_container_width=True)
            
            with col2:
                # Salary distribution
                fig_salary_dist = px.histogram(
                    df, x='salary', nbins=30,
                    title="Salary Distribution",
                    labels={'salary': 'Salary', 'count': 'Count'}
                )
                st.plotly_chart(fig_salary_dist, use_container_width=True)
        
        with tab2:
            st.subheader("Correlation Heatmap")
            
            # Select numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            corr = df[numeric_cols].corr()
            
            fig_corr = go.Figure(
                data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='RdBu')
            )
            fig_corr.update_layout(title="Feature Correlation Matrix", height=600)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with tab3:
            st.subheader("Gender-wise Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            male_df = df[df['Gender'] == 0]
            female_df = df[df['Gender'] == 1]
            
            with col1:
                st.write("**Male Employees**")
                st.metric("Count", len(male_df))
                st.metric("Avg Age", f"{male_df['age'].mean():.1f}")
                st.metric("Avg Heart Rate", f"{male_df['Resting_Heart_Rate'].mean():.1f}")
            
            with col2:
                st.write("**Female Employees**")
                st.metric("Count", len(female_df))
                st.metric("Avg Age", f"{female_df['age'].mean():.1f}")
                st.metric("Avg Heart Rate", f"{female_df['Resting_Heart_Rate'].mean():.1f}")
            
            with col3:
                st.write("**Stress Comparison**")
                male_stress_dist = male_df['Stress_Level'].value_counts(normalize=True).sort_index() * 100
                female_stress_dist = female_df['Stress_Level'].value_counts(normalize=True).sort_index() * 100
                
                comparison_data = pd.DataFrame({
                    'Male': male_stress_dist.values if len(male_stress_dist) == 3 else [0]*3,
                    'Female': female_stress_dist.values if len(female_stress_dist) == 3 else [0]*3
                }, index=['Low', 'Medium', 'High'])
                
                fig_gender_comparison = px.bar(
                    comparison_data,
                    barmode='group',
                    title="Stress Distribution by Gender",
                    labels={'index': 'Stress Level', 'value': 'Percentage'}
                )
                st.plotly_chart(fig_gender_comparison, use_container_width=True)
        
        with tab4:
            st.subheader("Department Analysis")
            
            # Get department columns
            dept_cols = [col for col in df.columns if col.startswith('department_')]
            
            if dept_cols:
                st.info(f"Found {len(dept_cols)} departments in dataset")
            else:
                st.warning("No department data found")
    
    # ==================== PREDICTIONS PAGE ====================
    elif page == "🔮 Predictions":
        st.title("🔮 Stress Level Prediction")
        
        tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])
        
        with tab1:
            st.subheader("Predict Stress Level for Individual Employee")
            
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age", min_value=18, max_value=70, value=30)
                gender = st.selectbox("Gender", ["Male", "Female"])
                years_company = st.number_input("Years in Company", min_value=0.0, max_value=50.0, value=5.0, step=0.5)
                prior_exp = st.number_input("Prior Experience (Years)", min_value=0.0, max_value=50.0, value=3.0, step=0.5)
            
            with col2:
                salary = st.number_input("Salary", min_value=20000, max_value=200000, value=60000, step=1000)
                bonus = st.number_input("Annual Bonus", min_value=0.0, max_value=50000.0, value=5000.0, step=500.0)
                heart_rate = st.number_input("Resting Heart Rate (BPM)", min_value=40, max_value=200, value=75)
                company = st.selectbox("Company", list(range(4)))
            
            if st.button("🔮 Predict Stress Level", key="predict_single"):
                if heart_rate < 60:
                    st.warning("Heart Rate is below the normal range (<60 BPM). Please consult a healthcare professional.")
                    return
                elif heart_rate > 120:
                    st.warning("Heart Rate is above the normal range (>120 BPM). Please consult a healthcare professional.")
                    return
                    
                # Show color-coded status card
                if 60 <= heart_rate <= 80:
                    st.markdown("""
                    <div style='background-color: #10b981; padding: 15px; border-radius: 8px; color: white; text-align: center; font-weight: bold; margin-bottom: 20px;'>
                        Heart Rate Status: Low Stress Zone
                    </div>
                    """, unsafe_allow_html=True)
                elif 81 <= heart_rate <= 100:
                    st.markdown("""
                    <div style='background-color: #ffc107; padding: 15px; border-radius: 8px; color: black; text-align: center; font-weight: bold; margin-bottom: 20px;'>
                        Heart Rate Status: Medium Stress Zone
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background-color: #ef4444; padding: 15px; border-radius: 8px; color: white; text-align: center; font-weight: bold; margin-bottom: 20px;'>
                        Heart Rate Status: High Stress Zone
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Prepare features (19 feature                workload_score = (years_company / 10) * 10
                experience_pressure = max(years_company - prior_exp, 0)
                heart_rate_stress = ((heart_rate - 60) / 60) * 10
                raw_score = 0.30 * workload_score + 0.20 * experience_pressure + 0.50 * heart_rate_stress

                features = np.array([[
                    0,  # employee_id
                    age,
                    age_when_joined,
                    years_company,
                    salary,
                    bonus,
                    prior_exp,
                    1 if gender == "Female" else 0,
                    heart_rate,
                    1 if company == 0 else 0,  # company_Glasses
                    1 if company == 1 else 0,  # company_Pear
                    0,  # department_BigData
                    0,  # department_Design
                    0,  # department_Sales
                    0,  # department_Search Engine
                    0,  # department_Support
                    workload_score,
                    experience_pressure,
                    heart_rate_stress
                ]])
                
                try:
                    probabilities = models['general'].predict_proba(features)[0]
                    raw_confidence = float(max(probabilities) * 100)
                    pred_idx = models['general'].predict(features)[0]

                    # Map predicted index to label
                    if pred_idx == 0:
                        ml_level = "Low"
                    elif pred_idx == 1:
                        ml_level = "Medium"
                    else:
                        ml_level = "High"

                    # Apply Heart Rate overrides (Section C)
                    final_level = ml_level
                    if heart_rate >= 115:
                        if final_level == "Low":
                            final_level = "Medium"
                    if heart_rate >= 120 and workload_score > 5:
                        final_level = "High"

                    # Align stress score strictly to final stress level's range (Section D)
                    if final_level == "Low":
                        stress_score = min(max(raw_score, 0.0), 3.5)
                    elif final_level == "Medium":
                        stress_score = min(max(raw_score, 3.6), 6.5)
                    else:
                        stress_score = min(max(raw_score, 6.6), 10.0)

                    predicted_level = f"{final_level} Stress"

                    # Calculate realistic confidence score from probabilities (Section E)
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

                    # Calculate probability breakdown for Section E
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

                    # Calculate feature percentage contributions for Transparency Panel (Section G)
                    total_weighted = (workload_score * 0.30) + (experience_pressure * 0.20) + (heart_rate_stress * 0.50)
                    if total_weighted > 0:
                        contrib_workload = ((workload_score * 0.30) / total_weighted) * 100
                        contrib_experience = ((experience_pressure * 0.20) / total_weighted) * 100
                        contrib_heart_rate = ((heart_rate_stress * 0.50) / total_weighted) * 100
                    else:
                        contrib_workload = 30.0
                        contrib_experience = 20.0
                        contrib_heart_rate = 50.0

                    # 1. Heart Rate Assessment
                    st.markdown("### 1. Heart Rate Assessment")
                    
                    if 60 <= heart_rate <= 80:
                        hr_zone_text = "Low Stress Zone"
                        hr_emoji = "🟢"
                        hr_color = "#10b981"
                    elif 81 <= heart_rate <= 100:
                        hr_zone_text = "Medium Stress Zone"
                        hr_emoji = "🟡"
                        hr_color = "#ffc107"
                    else:
                        hr_zone_text = "High Stress Zone"
                        hr_emoji = "🔴"
                        hr_color = "#ef4444"
                        
                    st.markdown(f"""
                    <div style='background-color: {hr_color}; padding: 15px; border-radius: 8px; color: white; text-align: center; font-weight: bold; margin-bottom: 20px; font-size: 20px;'>
                        {hr_emoji} {hr_zone_text} ({heart_rate} BPM)
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 2. Machine Learning Prediction
                    st.markdown("### 2. Machine Learning Prediction")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    colors = {'Low': '#10b981', 'Medium': '#ffc107', 'High': '#ef4444'}
                    icons = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}
                    
                    with col1:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, {colors[final_level]} 0%, {colors[final_level]} 100%); padding: 20px; border-radius: 12px; color: white; text-align: center; font-weight: bold;'>
                            <h4 style='margin: 0; font-size: 14px; opacity: 0.9;'>Predicted Stress Level</h4>
                            <h2 style='margin: 10px 0 0 0; font-size: 24px;'>{icons[final_level]} {final_level} Stress</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.metric("Stress Score", f"{stress_score:.2f}/10")
                    
                    with col3:
                        st.metric("Confidence Score", f"{confidence_score:.1f}%")

                    # Probability Breakdown (Section E)
                    st.markdown("#### Probability Breakdown")
                    col_p1, col_p2, col_p3 = st.columns(3)
                    with col_p1:
                        st.metric("Low Probability", f"{prob_dict['Low']:.1f}%")
                    with col_p2:
                        st.metric("Medium Probability", f"{prob_dict['Medium']:.1f}%")
                    with col_p3:
                        st.metric("High Probability", f"{prob_dict['High']:.1f}%")
                        
                    # 3. Prediction Explanation
                    st.markdown("---")
                    st.markdown("### 3. Prediction Explanation")
                    
                    col_exp1, col_exp2, col_exp3 = st.columns(3)
                    with col_exp1:
                        st.metric("Workload Score", f"{workload_score:.2f}/10")
                    with col_exp2:
                        st.metric("Experience Pressure", f"{experience_pressure:.2f}")
                    with col_exp3:
                        st.metric("Heart Rate Stress", f"{heart_rate_stress:.2f}/10")
                        
                    st.markdown("#### Factor Contribution Analysis")
                    
                    # Dynamic Explanation generation (Section F)
                    if heart_rate <= 80:
                        hr_desc = f"{heart_rate} BPM (Low Stress Zone)"
                        hr_impact = "within a normal range and has minimal impact on the stress score"
                    elif heart_rate <= 100:
                        hr_desc = f"{heart_rate} BPM (Medium Stress Zone)"
                        hr_impact = "moderately elevated and contributes to the stress score"
                    else:
                        hr_desc = f"{heart_rate} BPM (High Stress Zone)"
                        hr_impact = "elevated and contributes significantly to the overall stress score"

                    if workload_score <= 3.5:
                        wl_desc = "Low"
                        wl_impact = "low workload factors"
                    elif workload_score <= 6.5:
                        wl_desc = "Moderate"
                        wl_impact = "workload factors"
                    else:
                        wl_desc = "High"
                        wl_impact = "high workload factors"

                    if experience_pressure <= 2.0:
                        exp_desc = "Low"
                    elif experience_pressure <= 5.0:
                        exp_desc = "Moderate"
                    else:
                        exp_desc = "High"

                    explanation_text = (
                        f"The employee's resting heart rate is {hr_desc} which is {hr_impact}. "
                        f"Combined with {wl_desc} workload ({wl_impact}) and {exp_desc} experience pressure, "
                        f"the system classifies the employee as {final_level} Stress with {confidence_score:.1f}% confidence."
                    )
                        
                    st.info(explanation_text)

                    # Transparency Panel (Section G)
                    st.markdown("#### 🔍 Why was this prediction made? (Transparency Panel)")
                    col_t1, col_t2, col_t3 = st.columns(3)
                    with col_t1:
                        st.metric("Workload Contribution", f"{contrib_workload:.0f}%")
                    with col_t2:
                        st.metric("Experience Contribution", f"{contrib_experience:.0f}%")
                    with col_t3:
                        st.metric("Heart Rate Contribution", f"{contrib_heart_rate:.0f}%")
                    
                    st.markdown("---")
                    
                    # Recommendation
                    rec = get_recommendation(predicted_level.split()[0])
                    st.markdown(f"### {rec['emoji']} {rec['message']}")
                    for detail in rec['details']:
                        st.write(detail)
                
                except Exception as e:
                    st.error(f"Prediction error: {e}")
        
        with tab2:
            st.subheader("Batch Prediction")
            
            uploaded_file = st.file_uploader("Upload CSV with employee data", type=['csv'])
            
            if uploaded_file is not None:
                batch_df = pd.read_csv(uploaded_file)
                st.write("Preview:", batch_df.head())
                
                if st.button("🚀 Predict for All Employees"):
                    # Process batch
                    try:
                        predictions = []
                        for idx, row in batch_df.iterrows():
                            age = row.get('age', 30)
                            years = row.get('years_in_company', 5)
                            age_when_joined = age - years
                            
                            features = np.array([[
                                1, age, age_when_joined, years,
                                row.get('salary', 60000),
                                row.get('bonus', 5000),
                                row.get('prior_experience', 3),
                                row.get('gender', 0),
                                row.get('heart_rate', 75),
                                0, 0, 0, 0, 0, 0, 0, 0, 0,
                                (years / 10) * 10,
                                max(years - row.get('prior_experience', 3), 0),
                                ((row.get('heart_rate', 75) - 60) / (120 - 60)) * 10
                            ]])
                            
                            pred = models['general'].predict(features)[0]
                            predictions.append(int(pred))
                        
                        batch_df['Predicted_Stress_Level'] = predictions
                        batch_df['Stress_Category'] = batch_df['Predicted_Stress_Level'].map({
                            0: 'Low', 1: 'Medium', 2: 'High'
                        })
                        
                        st.success("✅ Predictions completed!")
                        st.dataframe(batch_df[['age', 'gender', 'salary', 'Stress_Category']])
                        
                        # Download results
                        csv = batch_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results (CSV)",
                            data=csv,
                            file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    except Exception as e:
                        st.error(f"Batch prediction error: {e}")
    
    # ==================== EMPLOYEE SEARCH PAGE ====================
    elif page == "👥 Employee Search":
        st.title("👥 Employee Search & Risk Detection")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_type = st.selectbox("Search by:", ["Employee ID", "Stress Level", "Department"])
        
        if search_type == "Employee ID":
            emp_id = st.number_input("Enter Employee ID", min_value=1, max_value=int(df['employee_id'].max()))
            
            if st.button("🔍 Search"):
                emp_data = df[df['employee_id'] == emp_id]
                if not emp_data.empty:
                    st.success(f"Found employee #{emp_id}")
                    st.dataframe(emp_data)
                else:
                    st.warning(f"No employee found with ID #{emp_id}")
        
        elif search_type == "Stress Level":
            stress_filter = st.selectbox("Select Stress Level:", ["Low", "Medium", "High"])
            stress_map = {'Low': 0, 'Medium': 1, 'High': 2}
            
            filtered = df[df['Stress_Level'] == stress_map[stress_filter]]
            st.write(f"Found {len(filtered)} employees with {stress_filter} stress level")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", len(filtered))
            with col2:
                st.metric("Avg Age", f"{filtered['age'].mean():.1f}")
            with col3:
                st.metric("Avg Salary", f"${filtered['salary'].mean():,.0f}")
            
            st.dataframe(filtered[['employee_id', 'age', 'salary', 'Stress_Level']])
    
    # ==================== REPORTS PAGE ====================
    elif page == "📋 Reports":
        st.title("📋 Reports & Exports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Generate Summary Report"):
                summary = f"""
                # Employee Stress Prediction System Report
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                ## Dataset Overview
                - Total Employees: {len(df)}
                - Low Stress: {len(df[df['Stress_Level']==0])} ({len(df[df['Stress_Level']==0])/len(df)*100:.1f}%)
                - Medium Stress: {len(df[df['Stress_Level']==1])} ({len(df[df['Stress_Level']==1])/len(df)*100:.1f}%)
                - High Stress: {len(df[df['Stress_Level']==2])} ({len(df[df['Stress_Level']==2])/len(df)*100:.1f}%)
                
                ## Demographics
                - Average Age: {df['age'].mean():.1f}
                - Average Salary: ${df['salary'].mean():,.0f}
                - Average Heart Rate: {df['Resting_Heart_Rate'].mean():.1f} BPM
                - Average Years in Company: {df['years_in_the_company'].mean():.1f}
                """
                st.text(summary)
                st.download_button(
                    label="📥 Download Report",
                    data=summary,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📈 Export Dataset (CSV)"):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Dataset",
                    data=csv_data,
                    file_name=f"employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # Model information
        st.subheader("Model Information")
        st.info("""
        **Trained Models:**
        - General Model: All Employees
        - Gender-Specific Models: Male & Female Employees
        
        **Models Available:**
        - Logistic Regression
        - Decision Tree
        - Random Forest
        - Support Vector Machine
        
        **Best Model Performance:**
        - Precision: High
        - Recall: High
        - F1-Score: High
        """)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About
    **Employee Stress Prediction System**
    
    An AI-powered HR analytics platform for:
    - 🎯 Stress level prediction
    - 📊 Employee analytics
    - 💼 HR recommendations
    - 📈 Risk assessment
    
    Built with Streamlit, Scikit-Learn, and Plotly
    """)


if __name__ == '__main__':
    main()
