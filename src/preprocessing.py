"""
Data Preprocessing Module
Handles data cleaning, encoding, and transformation.
"""

import pandas as pd
import numpy as np


def handle_missing_values(df, strategy='drop'):
    """
    Handle missing values in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset with potential missing values
    strategy : str
        'drop' to remove rows with missing values, 'mean' to fill with mean
    
    Returns:
    --------
    pd.DataFrame
        Dataset with missing values handled
    """
    if df.isnull().sum().sum() > 0:
        if strategy == 'drop':
            df = df.dropna()
            print(f"✓ Removed rows with missing values")
        elif strategy == 'mean':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            print(f"✓ Filled numeric missing values with mean")
    
    return df


def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset with potential duplicates
    
    Returns:
    --------
    pd.DataFrame
        Dataset without duplicates
    """
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed = initial_rows - len(df)
    
    if removed > 0:
        print(f"✓ Removed {removed} duplicate rows")
    else:
        print(f"✓ No duplicates found")
    
    return df


def encode_gender(df, gender_column='Gender'):
    """
    Encode Gender column: Male = 0, Female = 1
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    gender_column : str
        Name of the gender column
    
    Returns:
    --------
    pd.DataFrame
        Dataset with encoded gender
    """
    if gender_column in df.columns:
        df[gender_column] = df[gender_column].map({'Male': 0, 'Female': 1})
        print(f"✓ Gender encoded: Male=0, Female=1")
    else:
        print(f"✗ Column '{gender_column}' not found in dataset")
    
    return df


def one_hot_encode(df, columns_to_encode=None):
    """
    One-hot encode specified categorical columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    columns_to_encode : list, optional
        List of column names to one-hot encode.
        If not provided, defaults to ['company', 'department']
    
    Returns:
    --------
    pd.DataFrame
        Dataset with one-hot encoded columns
    """
    if columns_to_encode is None:
        columns_to_encode = ['company', 'department']
    
    for column in columns_to_encode:
        if column in df.columns:
            # One-hot encode with drop_first=True and drop the original column
            encoded = pd.get_dummies(df[column], prefix=column, drop_first=True)
            df = pd.concat([df, encoded], axis=1)
            df = df.drop(column, axis=1)
            print(f"✓ One-hot encoded '{column}' column (drop_first=True)")
        else:
            print(f"✗ Column '{column}' not found in dataset")
    
    return df


def preprocess_data(df):
    """
    Complete preprocessing pipeline.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The raw dataset
    
    Returns:
    --------
    pd.DataFrame
        Preprocessed dataset
    """
    print("\n" + "=" * 70)
    print("DATA PREPROCESSING")
    print("=" * 70 + "\n")
    
    # Handle missing values
    df = handle_missing_values(df, strategy='drop')
    
    # Remove duplicates
    df = remove_duplicates(df)
    
    # Encode gender
    df = encode_gender(df, gender_column='Gender')
    
    # One-hot encode categorical variables
    columns_to_encode = ['company', 'department']
    df = one_hot_encode(df, columns_to_encode)
    
    print(f"\n✓ Preprocessing completed!")
    print(f"  Final dataset shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
    
    return df
