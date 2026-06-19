"""
Model Training and Evaluation Module
Trains multiple ML models and evaluates their performance.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    confusion_matrix, classification_report, accuracy_score, 
    precision_score, recall_score, f1_score
)
import joblib


class StressPredictor:
    """
    Train and evaluate multiple ML models for stress prediction.
    """
    
    def __init__(self):
        """Initialize the predictor with empty models and results."""
        self.models = {}
        self.results = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.best_model_name = None
        self.best_model = None
    
    def prepare_data(self, df, target_column='Stress_Level', test_size=0.20, 
                     random_state=42):
        """
        Split data into train and test sets with stratification.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The complete dataset
        target_column : str
            Name of the target variable
        test_size : float
            Proportion of test set
        random_state : int
            Random seed for reproducibility
        """
        # Separate features and target
        y = df[target_column]
        X = df.drop(columns=[target_column, 'Stress_Score'])
        
        # Train-test split with stratification
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=random_state,
            stratify=y
        )
        
        print(f"\n✓ Data split completed!")
        print(f"  Training set size: {len(self.X_train)}")
        print(f"  Test set size: {len(self.X_test)}")
    
    def train_logistic_regression(self):
        """Train Logistic Regression model."""
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(self.X_train, self.y_train)
        self.models['Logistic Regression'] = model
        print("✓ Trained Logistic Regression")
    
    def train_decision_tree(self):
        """Train Decision Tree model."""
        model = DecisionTreeClassifier(random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['Decision Tree'] = model
        print("✓ Trained Decision Tree")
    
    def train_random_forest(self):
        """Train Random Forest model."""
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = model
        print("✓ Trained Random Forest")
    
    def train_svm(self):
        """Train Support Vector Machine model."""
        model = SVC(kernel='rbf', random_state=42)
        model.fit(self.X_train, self.y_train)
        self.models['SVM'] = model
        print("✓ Trained SVM")
    
    def train_all_models(self):
        """Train all models."""
        print("\n" + "=" * 70)
        print("MODEL TRAINING")
        print("=" * 70)
        print("\nTraining models...")
        
        self.train_logistic_regression()
        self.train_decision_tree()
        self.train_random_forest()
        self.train_svm()
        
        print(f"\n✓ All models trained successfully!")
    
    def evaluate_models(self):
        """Evaluate all models and store results."""
        print("\n" + "=" * 70)
        print("MODEL EVALUATION")
        print("=" * 70 + "\n")
        
        for model_name, model in self.models.items():
            # Make predictions
            y_pred = model.predict(self.X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(self.y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(self.y_test, y_pred, average='weighted', zero_division=0)
            
            # Store results
            self.results[model_name] = {
                'model': model,
                'predictions': y_pred,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'confusion_matrix': confusion_matrix(self.y_test, y_pred),
                'classification_report': classification_report(self.y_test, y_pred, zero_division=0)
            }
            
            # Print results
            print(f"\n{model_name}:")
            print(f"  Accuracy:  {accuracy:.4f}")
            print(f"  Precision: {precision:.4f}")
            print(f"  Recall:    {recall:.4f}")
            print(f"  F1-Score:  {f1:.4f}")
        
        # Find best model
        self.best_model_name = max(self.results, key=lambda x: self.results[x]['accuracy'])
        self.best_model = self.results[self.best_model_name]['model']
        
        print(f"\n{'=' * 70}")
        print(f"✓ Best Model: {self.best_model_name} "
              f"(Accuracy: {self.results[self.best_model_name]['accuracy']:.4f})")
        print(f"{'=' * 70}\n")
    
    def cross_validate(self, cv_folds=5):
        """
        Perform 5-fold cross-validation on all models.
        
        Parameters:
        -----------
        cv_folds : int
            Number of folds for cross-validation
        """
        print("\n" + "=" * 70)
        print(f"CROSS-VALIDATION ({cv_folds}-FOLD)")
        print("=" * 70 + "\n")
        
        for model_name, model in self.models.items():
            cv_scores = cross_val_score(model, self.X_train, self.y_train, 
                                       cv=cv_folds, scoring='accuracy')
            
            print(f"{model_name}:")
            print(f"  Fold Scores: {[f'{score:.4f}' for score in cv_scores]}")
            print(f"  Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})\n")
    
    def get_accuracy_comparison(self):
        """
        Get accuracy comparison of all models.
        
        Returns:
        --------
        dict
            Dictionary with model names and their accuracies
        """
        return {name: self.results[name]['accuracy'] for name in self.results}
    
    def get_feature_importance(self, model_name='Random Forest'):
        """
        Get feature importance from tree-based models.
        
        Parameters:
        -----------
        model_name : str
            Name of the model
        
        Returns:
        --------
        pd.DataFrame
            Feature importance dataframe
        """
        if model_name not in self.models:
            print(f"✗ Model '{model_name}' not found")
            return None
        
        model = self.models[model_name]
        
        # Check if model has feature_importances_
        if not hasattr(model, 'feature_importances_'):
            print(f"✗ Model '{model_name}' does not support feature importance")
            return None
        
        importance_df = pd.DataFrame({
            'Feature': self.X_train.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        return importance_df
    
    def save_best_model(self, filepath):
        """
        Save the best model using joblib.
        
        Parameters:
        -----------
        filepath : str
            Path to save the model
        """
        joblib.dump(self.best_model, filepath)
        print(f"✓ Best model '{self.best_model_name}' saved to {filepath}")
    
    def get_confusion_matrix(self, model_name):
        """
        Get confusion matrix for a model.
        
        Parameters:
        -----------
        model_name : str
            Name of the model
        
        Returns:
        --------
        np.ndarray
            Confusion matrix
        """
        if model_name in self.results:
            return self.results[model_name]['confusion_matrix']
        return None
    
    def get_classification_report(self, model_name):
        """
        Get classification report for a model.
        
        Parameters:
        -----------
        model_name : str
            Name of the model
        
        Returns:
        --------
        str
            Classification report
        """
        if model_name in self.results:
            return self.results[model_name]['classification_report']
        return None
