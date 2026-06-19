"""
Data Loading Module
Handles loading and basic exploration of the employee dataset.
"""

import pandas as pd
import numpy as np


def load_dataset(file_path):
    """
    Load the CSV dataset from the specified file path.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataset
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Dataset loaded successfully from {file_path}")
        print(f"  Shape: {df.shape[0]} rows, {df.shape[1]} columns\n")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File not found at {file_path}")
        raise
    except Exception as e:
        print(f"✗ Error loading file: {str(e)}")
        raise


def explore_dataset(df):
    """
    Perform initial exploratory data analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to explore
    """
    print("=" * 70)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 70)
    
    print("\n1. DATASET SHAPE:")
    print(f"   Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    print("\n2. COLUMN NAMES AND DATA TYPES:")
    print(df.dtypes)
    
    print("\n3. FIRST 5 ROWS:")
    print(df.head())
    
    print("\n4. DATASET INFO:")
    print(df.info())
    
    print("\n5. STATISTICAL SUMMARY:")
    print(df.describe())
    
    print("\n6. MISSING VALUES:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   No missing values found! ✓")
    else:
        print(missing[missing > 0])
    
    print("\n7. DUPLICATE ROWS:")
    duplicates = df.duplicated().sum()
    print(f"   Total duplicates: {duplicates}")
    
    print("=" * 70 + "\n")
