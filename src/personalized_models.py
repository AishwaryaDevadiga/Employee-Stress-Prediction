"""
Gender-Specific Models Module
Trains separate ML models for male and female employees.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os


class GenderSpecificPredictor:
    """Train gender-specific stress prediction models."""
    
    def __init__(self):
        """Initialize the predictor."""
        self.male_data = None
        self.female_data = None
        self.male_models = {}
        self.female_models = {}
        self.male_results = {}
        self.female_results = {}
    
    def load_processed_data(self, filepath):
        """
        Load processed data and split by gender.
        
        Parameters:
        -----------
        filepath : str
            Path to processed data CSV
        """
        df = pd.read_csv(filepath)
        
        # Split by gender (Gender column: 0=Male, 1=Female)
        self.male_data = df[df['Gender'] == 0].copy()
        self.female_data = df[df['Gender'] == 1].copy()
        
        print(f"✓ Data loaded: {len(df)} total employees")
        print(f"  Male employees: {len(self.male_data)}")
        print(f"  Female employees: {len(self.female_data)}")
    
    def train_models_for_gender(self, gender_data, gender_label):
        """
        Train all models for a specific gender.
        
        Parameters:
        -----------
        gender_data : pd.DataFrame
            Dataset for specific gender
        gender_label : str
            'male' or 'female'
        
        Returns:
        --------
        dict
            Training results
        """
        if len(gender_data) == 0:
            print(f"✗ No data for {gender_label} employees")
            return {}
        
        # Prepare features and target
        X = gender_data.drop(['Stress_Level', 'employee_id', 'Gender'], axis=1)
        y = gender_data['Stress_Level']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(kernel='rbf', probability=True, random_state=42)
        }
        
        results = {}
        trained_models = {}
        
        print(f"\n  Training {gender_label} models ({len(X_train)} train, {len(X_test)} test):")
        
        for model_name, model in models.items():
            # Train
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            
            # Evaluate
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            results[model_name] = {
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1
            }
            
            trained_models[model_name] = model
            
            print(f"    {model_name:25} - Accuracy: {accuracy:.4f}")
        
        if gender_label == 'male':
            self.male_models = trained_models
            self.male_results = results
        else:
            self.female_models = trained_models
            self.female_results = results
        
        return results
    
    def train_all_gender_models(self):
        """Train models for both genders."""
        print("\n" + "="*70)
        print("TRAINING GENDER-SPECIFIC MODELS")
        print("="*70)
        
        self.train_models_for_gender(self.male_data, 'male')
        self.train_models_for_gender(self.female_data, 'female')
    
    def save_gender_models(self, output_dir='models/gender_specific'):
        """
        Save gender-specific models to disk.
        
        Parameters:
        -----------
        output_dir : str
            Directory to save models
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n✓ Saving gender-specific models to {output_dir}/")
        
        # Save male models
        for model_name, model in self.male_models.items():
            filename = f"male_{model_name.replace(' ', '_').lower()}.pkl"
            filepath = os.path.join(output_dir, filename)
            joblib.dump(model, filepath)
            print(f"  {filename}")
        
        # Save female models
        for model_name, model in self.female_models.items():
            filename = f"female_{model_name.replace(' ', '_').lower()}.pkl"
            filepath = os.path.join(output_dir, filename)
            joblib.dump(model, filepath)
            print(f"  {filename}")
    
    def print_comparison(self):
        """Print performance comparison between genders."""
        print("\n" + "-"*70)
        print("GENDER-SPECIFIC MODEL COMPARISON")
        print("-"*70)
        
        print("\nMALE EMPLOYEES:")
        print("Model                 Accuracy    Precision    Recall      F1-Score")
        print("-" * 70)
        for model_name, metrics in self.male_results.items():
            print(f"{model_name:20} {metrics['Accuracy']:.4f}      {metrics['Precision']:.4f}        "
                  f"{metrics['Recall']:.4f}      {metrics['F1-Score']:.4f}")
        
        print("\nFEMALE EMPLOYEES:")
        print("Model                 Accuracy    Precision    Recall      F1-Score")
        print("-" * 70)
        for model_name, metrics in self.female_results.items():
            print(f"{model_name:20} {metrics['Accuracy']:.4f}      {metrics['Precision']:.4f}        "
                  f"{metrics['Recall']:.4f}      {metrics['F1-Score']:.4f}")
    
    def save_summary_report(self, filepath='gender_models_summary.txt'):
        """
        Save summary report to file.
        
        Parameters:
        -----------
        filepath : str
            Output file path
        """
        with open(filepath, 'w') as f:
            f.write("="*70 + "\n")
            f.write("GENDER-SPECIFIC MODEL TRAINING REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write("MALE EMPLOYEES\n")
            f.write("-"*70 + "\n")
            f.write(f"Total: {len(self.male_data)}\n\n")
            f.write("Model Performance:\n")
            for model_name, metrics in self.male_results.items():
                f.write(f"  {model_name}:\n")
                f.write(f"    Accuracy:  {metrics['Accuracy']:.4f}\n")
                f.write(f"    Precision: {metrics['Precision']:.4f}\n")
                f.write(f"    Recall:    {metrics['Recall']:.4f}\n")
                f.write(f"    F1-Score:  {metrics['F1-Score']:.4f}\n\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("FEMALE EMPLOYEES\n")
            f.write("-"*70 + "\n")
            f.write(f"Total: {len(self.female_data)}\n\n")
            f.write("Model Performance:\n")
            for model_name, metrics in self.female_results.items():
                f.write(f"  {model_name}:\n")
                f.write(f"    Accuracy:  {metrics['Accuracy']:.4f}\n")
                f.write(f"    Precision: {metrics['Precision']:.4f}\n")
                f.write(f"    Recall:    {metrics['Recall']:.4f}\n")
                f.write(f"    F1-Score:  {metrics['F1-Score']:.4f}\n\n")
        
        print(f"✓ Summary report saved to {filepath}")
