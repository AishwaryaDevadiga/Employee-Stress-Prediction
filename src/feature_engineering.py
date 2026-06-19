"""
Feature Engineering Module
Creates engineered features for stress prediction.
"""

import pandas as pd
import numpy as np


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
            0.4 * df['Workload_Score'] +
            0.3 * df['Experience_Pressure'] +
            0.3 * df['HeartRate_Stress']
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
            if score < 3:
                return 0  # Low
            elif score < 6:
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
