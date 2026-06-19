"""
Feature Engineering Wrapper Class
Provides OOP interface for feature engineering functions.
"""

import pandas as pd
import numpy as np
from feature_engineering import (
    create_workload_score,
    create_experience_pressure,
    create_heart_rate_stress,
    create_stress_score,
    create_stress_level,
    engineer_features
)


class FeatureEngineer:
    """Object-oriented interface for feature engineering."""
    
    def __init__(self):
        """Initialize feature engineer."""
        self.df = None
    
    def create_all_features(self, df):
        """
        Create all engineered features.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Preprocessed dataset
        
        Returns:
        --------
        pd.DataFrame
            Dataset with all engineered features
        """
        self.df = engineer_features(df)
        return self.df
