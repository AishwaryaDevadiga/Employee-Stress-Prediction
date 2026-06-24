import pandas as pd
import numpy as np
import os

_dataset_extremes = None

def get_dataset_extremes():
    """
    Dynamically load min/max values from the dataset to avoid hardcoding.
    """
    global _dataset_extremes
    if _dataset_extremes is not None:
        return _dataset_extremes

    # Known extremes from dataset: Max Years = 9.0, Min HR = 55.0, Max HR = 92.2
    max_years = 9.0
    min_hr = 55.0
    max_hr = 92.2

    # Try to load dynamically
    paths_to_try = [
        'outputs/processed_data.csv',
        '../outputs/processed_data.csv',
        'dataset/company_employee_details4999.csv',
        '../dataset/company_employee_details4999.csv'
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                y_col = 'years_in_the_company' if 'years_in_the_company' in df.columns else 'years_in_company'
                if y_col not in df.columns:
                    cols = {c.lower(): c for c in df.columns}
                    if 'years_in_the_company' in cols:
                        y_col = cols['years_in_the_company']
                    elif 'years_in_company' in cols:
                        y_col = cols['years_in_company']
                
                hr_col = 'Resting_Heart_Rate' if 'Resting_Heart_Rate' in df.columns else 'resting_heart_rate'
                if hr_col not in df.columns:
                    cols = {c.lower(): c for c in df.columns}
                    if 'resting_heart_rate' in cols:
                        hr_col = cols['resting_heart_rate']

                if y_col in df.columns and hr_col in df.columns:
                    max_years = float(df[y_col].max())
                    min_hr = float(df[hr_col].min())
                    max_hr = float(df[hr_col].max())
                    break
            except Exception:
                pass
                
    _dataset_extremes = (max_years, min_hr, max_hr)
    return _dataset_extremes


def get_stress_calculation_details(years_in_company, prior_experience, resting_heart_rate):
    """
    Calculate the precise stress score steps based on the thesis/Colab methodology.
    """
    max_years, min_hr, max_hr = get_dataset_extremes()
    
    workload_score = (years_in_company / max_years) * 10
    experience_pressure = max(years_in_company - prior_experience, 0.0)
    heart_rate_stress = ((resting_heart_rate - min_hr) / (max_hr - min_hr)) * 10
    
    stress_score = 0.4 * workload_score + 0.3 * experience_pressure + 0.3 * heart_rate_stress
    
    if stress_score < 3.0:
        classification = "Low"
    elif stress_score < 6.0:
        classification = "Medium"
    else:
        classification = "High"
        
    return {
        'max_years': max_years,
        'min_hr': min_hr,
        'max_hr': max_hr,
        'workload_score': workload_score,
        'experience_pressure': experience_pressure,
        'heart_rate_stress': heart_rate_stress,
        'stress_score': stress_score,
        'classification': classification,
        'workload_formula': f"Workload Score = ({years_in_company} / {int(max_years) if max_years.is_integer() else max_years}) * 10 = {workload_score:.2f}",
        'experience_formula': f"Experience Pressure = max({years_in_company} - {prior_experience}, 0) = {experience_pressure:.2f}",
        'heart_rate_formula': f"Heart Rate Stress = (({resting_heart_rate} - {min_hr}) / ({max_hr} - {min_hr})) * 10 = {heart_rate_stress:.2f}",
        'stress_score_formula': f"Stress Score = 0.4 * {workload_score:.2f} + 0.3 * {experience_pressure:.2f} + 0.3 * {heart_rate_stress:.2f} = {stress_score:.2f}",
    }


def create_workload_score(df, years_column='years_in_the_company'):
    """
    Create Workload_Score feature:
    Workload_Score = (years_in_the_company / max(years_in_the_company)) * 10
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    years_column : str
        Name of the years in company column
    
    Returns:
    --------
    pd.DataFrame
        Dataset with Workload_Score feature
    """
    if years_column in df.columns:
        max_years = df[years_column].max()
        df['Workload_Score'] = (df[years_column] / max_years) * 10
        print(f"✓ Created 'Workload_Score' feature")
    else:
        print(f"✗ Column '{years_column}' not found")
    
    return df


def create_experience_pressure(df, years_col='years_in_the_company', 
                               prior_col='prior_years_experience'):
    """
    Create Experience_Pressure feature:
    Experience_Pressure = max(years_in_company - prior_years_experience, 0)
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    years_col : str
        Name of the years in company column
    prior_col : str
        Name of the prior years experience column
    
    Returns:
    --------
    pd.DataFrame
        Dataset with Experience_Pressure feature
    """
    if years_col in df.columns and prior_col in df.columns:
        df['Experience_Pressure'] = (df[years_col] - df[prior_col]).apply(lambda x: max(x, 0))
        print(f"✓ Created 'Experience_Pressure' feature")
    else:
        print(f"✗ Required columns not found")
    
    return df


def create_heart_rate_stress(df, hr_column='Resting_Heart_Rate'):
    """
    Create HeartRate_Stress feature:
    HeartRate_Stress = ((Resting_Heart_Rate - min_hr) / (max_hr - min_hr)) * 10
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    hr_column : str
        Name of the heart rate column
    
    Returns:
    --------
    pd.DataFrame
        Dataset with HeartRate_Stress feature
    """
    if hr_column in df.columns:
        min_hr = df[hr_column].min()
        max_hr = df[hr_column].max()
        
        if max_hr == min_hr:
            df['HeartRate_Stress'] = 0
        else:
            df['HeartRate_Stress'] = ((df[hr_column] - min_hr) / (max_hr - min_hr)) * 10
        
        print(f"✓ Created 'HeartRate_Stress' feature")
    else:
        print(f"✗ Column '{hr_column}' not found")
    
    return df


def create_stress_score(df):
    """
    Create Stress_Score feature:
    Stress_Score = 0.4*Workload_Score + 0.3*Experience_Pressure + 0.3*HeartRate_Stress
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset with required features
    
    Returns:
    --------
    pd.DataFrame
        Dataset with Stress_Score feature
    """
    required_features = ['Workload_Score', 'Experience_Pressure', 'HeartRate_Stress']
    if all(feature in df.columns for feature in required_features):
        df['Stress_Score'] = (
            0.40 * df['Workload_Score'] +
            0.30 * df['Experience_Pressure'] +
            0.30 * df['HeartRate_Stress']
        )
        print(f"✓ Created 'Stress_Score' feature")
    else:
        print(f"✗ Required features missing for Stress_Score calculation")
    
    return df


def create_stress_level(df, score_column='Stress_Score'):
    """
    Create Stress_Level categorical feature based on Stress_Score:
    - Low if score < 3
    - Medium if score < 6
    - High otherwise
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset with Stress_Score
    score_column : str
        Name of the stress score column
    
    Returns:
    --------
    pd.DataFrame
        Dataset with Stress_Level feature
    """
    if score_column in df.columns:
        def assign_stress_level(score):
            if score < 3.0:
                return 0  # Low
            elif score < 6.0:
                return 1  # Medium
            else:
                return 2  # High
        
        df['Stress_Level'] = df[score_column].apply(assign_stress_level)
        print(f"✓ Created 'Stress_Level' feature (0=Low, 1=Medium, 2=High)")
    else:
        print(f"✗ Column '{score_column}' not found")
    
    return df


def engineer_features(df):
    """
    Complete feature engineering pipeline.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The preprocessed dataset
    
    Returns:
    --------
    pd.DataFrame
        Dataset with engineered features
    """
    print("\n" + "=" * 70)
    print("FEATURE ENGINEERING")
    print("=" * 70 + "\n")
    
    # Create individual features
    df = create_workload_score(df)
    df = create_experience_pressure(df)
    df = create_heart_rate_stress(df)
    df = create_stress_score(df)
    df = create_stress_level(df)
    
    print(f"\n✓ Feature engineering completed!")
    print(f"  Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
    
    return df
