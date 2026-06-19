"""
Data Loader Wrapper Class
Provides OOP interface for data loading functions.
"""

import pandas as pd
import numpy as np
import os
from data_loader import load_dataset, explore_dataset


class DataLoader:
    """Object-oriented interface for data loading."""
    
    def __init__(self, data_path='dataset/company_employee_details4999.csv'):
        """
        Initialize DataLoader.
        
        Parameters:
        -----------
        data_path : str
            Path to the dataset CSV file
        """
        self.data_path = data_path
        self.df = None
    
    def load_data(self):
        """
        Load the employee dataset.
        
        Returns:
        --------
        pd.DataFrame
            Loaded dataset
        """
        try:
            self.df = load_dataset(self.data_path)
            return self.df
        except FileNotFoundError:
            print(f"✗ Dataset file not found at {self.data_path}")
            return None
    
    def explore_dataset(self):
        """
        Perform exploratory data analysis.
        
        Returns:
        --------
        pd.DataFrame
            Loaded dataset
        """
        if self.df is None:
            print("Load dataset first using load_data()")
            return None
        
        explore_dataset(self.df)
        return self.df
