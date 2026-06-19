"""
Data Preprocessing Wrapper Class
Provides OOP interface for preprocessing functions.
"""

import pandas as pd
import numpy as np
from preprocessing import (
    handle_missing_values,
    remove_duplicates,
    encode_gender,
    one_hot_encode,
    preprocess_data
)


class DataPreprocessor:
    """Object-oriented interface for data preprocessing."""
    
    def __init__(self):
        """Initialize data preprocessor."""
        self.df = None
    
    def handle_missing_values(self, df, strategy='drop'):
        """Handle missing values."""
        return handle_missing_values(df, strategy)
    
    def remove_duplicates(self, df):
        """Remove duplicate rows."""
        return remove_duplicates(df)
    
    def encode_gender(self, df):
        """Encode gender column (Male=0, Female=1)."""
        return encode_gender(df)
    
    def one_hot_encode(self, df, columns_to_encode=None):
        """One-hot encode categorical variables.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Dataset to encode
        columns_to_encode : list, optional
            Columns to encode. Defaults to ['company', 'department']
        
        Returns:
        --------
        pd.DataFrame
            Dataset with one-hot encoded columns
        """
        return one_hot_encode(df, columns_to_encode)
    
    def preprocess_data(self, df):
        """Complete preprocessing pipeline."""
        return preprocess_data(df)
