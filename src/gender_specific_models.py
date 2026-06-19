"""
Gender-Specific Model Training Module
Trains separate models for male and female employees.
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class GenderSpecificPredictor:
    """
    Train and evaluate gender-specific stress prediction models.
    """
    
    def __init__(self):
        """Initialize the gender-specific predictor."""
        self.models = {}  # {'Male': {model_name: model}, 'Female': {...}}
        self.results = {}  # {'Male': {metrics}, 'Female': {...}}
        self.data = {}    # {'Male': df, 'Female': df}
    
    def load_processed_data(self, filepath):
        """
        Load the processed dataset and split by gender.
        
        Parameters:
        -----------
        filepath : str
            Path to the processed CSV file
        """
        df = pd.read_csv(filepath)
        
        # Split by gender (0=Male, 1=Female)
        self.data['Male'] = df[df['Gender'] == 0].copy()
        self.data['Female'] = df[df['Gender'] == 1].copy()
        
        print("\n" + "=" * 70)
        print("GENDER-SPECIFIC DATA LOADING")
        print("=" * 70)
        print(f"\nMale employees: {len(self.data['Male'])} samples")
        print(f"Female employees: {len(self.data['Female'])} samples")
        
        # Display stress distribution for each gender
        for gender in ['Male', 'Female']:
            stress_dist = self.data[gender]['Stress_Level'].value_counts().sort_index()
            print(f"\n{gender} Stress Level Distribution:")
            for level, count in stress_dist.items():
                level_name = ['Low', 'Medium', 'High'][level]
                print(f"  {level_name}: {count} ({count/len(self.data[gender])*100:.1f}%)")
    
    def train_models_for_gender(self, gender, test_size=0.20, random_state=42):
        """
        Train all models for a specific gender.
        
        Parameters:
        -----------
        gender : str
            'Male' or 'Female'
        test_size : float
            Test set proportion
        random_state : int
            Random seed
        """
        if gender not in self.data:
            print(f"✗ Gender '{gender}' data not found")
            return
        
        df = self.data[gender]
        
        # Prepare features and target
        y = df['Stress_Level']
        X = df.drop(columns=['Stress_Level', 'Stress_Score', 'Gender'])
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"\n{'=' * 70}")
        print(f"TRAINING {gender.upper()} MODELS")
        print(f"{'=' * 70}")
        print(f"\nTraining set: {len(X_train)}, Test set: {len(X_test)}\n")
        
        # Initialize models dictionary for this gender
        self.models[gender] = {}
        self.results[gender] = {}
        
        # Train Decision Tree
        print("Training Decision Tree...")
        dt_model = DecisionTreeClassifier(random_state=random_state)
        dt_model.fit(X_train, y_train)
        y_pred = dt_model.predict(X_test)
        
        self.models[gender]['Decision Tree'] = dt_model
        self.results[gender]['Decision Tree'] = {
            'model': dt_model,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'X_test': X_test,
            'y_test': y_test
        }
        print(f"  ✓ Decision Tree - Accuracy: {self.results[gender]['Decision Tree']['accuracy']:.4f}")
        
        # Train Random Forest
        print("Training Random Forest...")
        rf_model = RandomForestClassifier(n_estimators=100, random_state=random_state)
        rf_model.fit(X_train, y_train)
        y_pred = rf_model.predict(X_test)
        
        self.models[gender]['Random Forest'] = rf_model
        self.results[gender]['Random Forest'] = {
            'model': rf_model,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'X_test': X_test,
            'y_test': y_test
        }
        print(f"  ✓ Random Forest - Accuracy: {self.results[gender]['Random Forest']['accuracy']:.4f}")
        
        # Train Logistic Regression
        print("Training Logistic Regression...")
        lr_model = LogisticRegression(random_state=random_state, max_iter=2000)
        lr_model.fit(X_train, y_train)
        y_pred = lr_model.predict(X_test)
        
        self.models[gender]['Logistic Regression'] = lr_model
        self.results[gender]['Logistic Regression'] = {
            'model': lr_model,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'X_test': X_test,
            'y_test': y_test
        }
        print(f"  ✓ Logistic Regression - Accuracy: {self.results[gender]['Logistic Regression']['accuracy']:.4f}")
        
        # Train SVM
        print("Training SVM...")
        svm_model = SVC(kernel='rbf', random_state=random_state)
        svm_model.fit(X_train, y_train)
        y_pred = svm_model.predict(X_test)
        
        self.models[gender]['SVM'] = svm_model
        self.results[gender]['SVM'] = {
            'model': svm_model,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'X_test': X_test,
            'y_test': y_test
        }
        print(f"  ✓ SVM - Accuracy: {self.results[gender]['SVM']['accuracy']:.4f}")
    
    def train_all_gender_models(self):
        """Train models for all genders."""
        for gender in ['Male', 'Female']:
            self.train_models_for_gender(gender)
    
    def print_comparison(self):
        """Print comparison of gender-specific models."""
        print("\n" + "=" * 70)
        print("GENDER-SPECIFIC MODEL COMPARISON")
        print("=" * 70)
        
        for gender in ['Male', 'Female']:
            print(f"\n{gender} Employees:")
            print(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
            print("-" * 73)
            
            for model_name, metrics in self.results[gender].items():
                print(f"{model_name:<25} {metrics['accuracy']:<12.4f} "
                      f"{metrics['precision']:<12.4f} {metrics['recall']:<12.4f} "
                      f"{metrics['f1_score']:<12.4f}")
    
    def save_gender_models(self, output_dir='models/gender_specific'):
        """
        Save gender-specific models.
        
        Parameters:
        -----------
        output_dir : str
            Directory to save models
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n{'=' * 70}")
        print("SAVING GENDER-SPECIFIC MODELS")
        print(f"{'=' * 70}\n")
        
        for gender, models_dict in self.models.items():
            for model_name, model in models_dict.items():
                filename = f"{output_dir}/{gender.lower()}_{model_name.replace(' ', '_')}.pkl"
                joblib.dump(model, filename)
                print(f"✓ Saved {gender} {model_name}: {filename}")
    
    def save_summary_report(self, output_path='outputs/results/gender_specific_summary.txt'):
        """
        Save gender-specific model summary report.
        
        Parameters:
        -----------
        output_path : str
            Path to save the report
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("GENDER-SPECIFIC MODEL SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            for gender in ['Male', 'Female']:
                f.write(f"\n{gender.upper()} EMPLOYEES\n")
                f.write("-" * 70 + "\n")
                f.write(f"Sample Size: {len(self.data[gender])}\n\n")
                
                f.write(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}\n")
                f.write("-" * 73 + "\n")
                
                for model_name, metrics in self.results[gender].items():
                    f.write(f"{model_name:<25} {metrics['accuracy']:<12.4f} "
                           f"{metrics['precision']:<12.4f} {metrics['recall']:<12.4f} "
                           f"{metrics['f1_score']:<12.4f}\n")
                
                # Best model
                best_model = max(self.results[gender], 
                               key=lambda x: self.results[gender][x]['accuracy'])
                f.write(f"\nBest Model: {best_model} "
                       f"(Accuracy: {self.results[gender][best_model]['accuracy']:.4f})\n")
        
        print(f"✓ Summary report saved to {output_path}")


def train_gender_specific_models(processed_data_path='outputs/processed_data.csv'):
    """
    Main function to train gender-specific models.
    
    Parameters:
    -----------
    processed_data_path : str
        Path to the processed dataset
    """
    predictor = GenderSpecificPredictor()
    
    # Load data
    predictor.load_processed_data(processed_data_path)
    
    # Train models for both genders
    predictor.train_all_gender_models()
    
    # Print comparison
    predictor.print_comparison()
    
    # Save models
    predictor.save_gender_models()
    
    # Save report
    predictor.save_summary_report()
    
    return predictor
