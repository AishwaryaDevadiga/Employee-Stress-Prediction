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
                heart_rate = st.number_input("Resting Heart Rate (BPM)", min_value=40, max_value=120, value=75)
                company = st.selectbox("Company", list(range(4)))
            
            if st.button("🔮 Predict Stress Level", key="predict_single"):
                # Prepare features (19 features matching training data structure)
                age_when_joined = age - years_company
                workload_score = (years_company / 10) * 10
                experience_pressure = max(years_company - prior_exp, 0)
                heart_rate_stress = ((heart_rate - 40) / (200 - 40)) * 10
                
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
                    prediction = models['general'].predict(features)[0]
                    probability = models['general'].predict_proba(features)[0]
                    
                    stress_levels = ['Low Stress', 'Medium Stress', 'High Stress']
                    predicted_level = stress_levels[int(prediction)]
                    
                    st.success(f"### Predicted Stress Level: {stress_level_color(stress_levels[int(prediction)].split()[0])} {predicted_level}")
                    
                    # Probability distribution
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Low Stress", f"{probability[0]*100:.1f}%")
                    with col2:
                        st.metric("Medium Stress", f"{probability[1]*100:.1f}%")
                    with col3:
                        st.metric("High Stress", f"{probability[2]*100:.1f}%")
                    
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
                                ((row.get('heart_rate', 75) - 40) / (200 - 40)) * 10
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
