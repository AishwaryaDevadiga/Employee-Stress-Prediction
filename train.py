"""
Model Training Script
Trains and saves all ML models for employee stress prediction.
Run this script to train and save models before starting the dashboard.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import joblib
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_loader_class import DataLoader
from data_preprocessor_class import DataPreprocessor
from feature_engineer_class import FeatureEngineer
from model_trainer import StressPredictor
from gender_specific_models import GenderSpecificPredictor


def create_directories():
    """Create necessary directories if they don't exist."""
    dirs = ['models', 'outputs', 'outputs/plots', 'outputs/reports']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✓ Directories created/verified")


def train_general_models():
    """Train general stress prediction models for all employees."""
    print("\n" + "="*70)
    print("TRAINING GENERAL MODELS (All Employees)")
    print("="*70)
    
    # Load data
    loader = DataLoader('dataset/company_employee_details4999.csv')
    df = loader.load_data()
    
    if df is None:
        print("✗ Failed to load dataset")
        return False
    
    # Preprocess
    print("\n📊 Preprocessing data...")
    preprocessor = DataPreprocessor()
    df = preprocessor.handle_missing_values(df)
    df = preprocessor.remove_duplicates(df)
    df = preprocessor.encode_gender(df)
    df = preprocessor.one_hot_encode(df)
    
    # Feature engineering
    print("\n🔧 Engineering features...")
    engineer = FeatureEngineer()
    df = engineer.create_all_features(df)
    
    # Save processed data
    df.to_csv('outputs/processed_data.csv', index=False)
    print(f"✓ Processed data saved (shape: {df.shape})")
    
    # Train models
    print("\n🤖 Training models...")
    predictor = StressPredictor()
    predictor.prepare_data(df)
    predictor.train_all_models()
    
    # Evaluate
    print("\n📈 Evaluating models...")
    results = predictor.evaluate_models()
    
    # Save results
    results_df = pd.DataFrame(results).T
    
    # Debug: Print dataframe columns
    print(f"\n📊 Results dataframe columns: {list(results_df.columns)}")
    print(f"📊 Results dataframe shape: {results_df.shape}")
    
    results_df.to_csv('outputs/reports/model_results.csv')
    print(f"\n✓ Model results saved to outputs/reports/model_results.csv")
    
    # Save best model - use the best model already identified by StressPredictor
    if hasattr(predictor, 'best_model_name') and predictor.best_model_name:
        best_model_name = predictor.best_model_name
        best_model = predictor.best_model
        print(f"\n✓ Best model identified: {best_model_name}")
    else:
        # Fallback: Find best model from results using accuracy column
        accuracy_col = None
        if 'accuracy' in results_df.columns:
            accuracy_col = 'accuracy'
        elif 'Accuracy' in results_df.columns:
            accuracy_col = 'Accuracy'
        
        if accuracy_col:
            best_model_name = results_df[accuracy_col].idxmax()
            best_model = predictor.models[best_model_name]
            best_accuracy = results_df.loc[best_model_name, accuracy_col]
            print(f"\n✓ Best model selected: {best_model_name} (Accuracy: {best_accuracy:.4f})")
        else:
            print(f"✗ Error: Could not find accuracy column. Available columns: {list(results_df.columns)}")
            return False
    
    joblib.dump(best_model, 'models/best_general_model.pkl')
    print(f"✓ Best model saved: {best_model_name}")
    
    # Cross-validation
    print("\n🔄 Performing 5-fold cross-validation...")
    predictor.cross_validate()
    
    return True


def train_gender_models():
    """Train gender-specific stress prediction models."""
    print("\n" + "="*70)
    print("TRAINING GENDER-SPECIFIC MODELS")
    print("="*70)
    
    # Load processed data
    try:
        df = pd.read_csv('outputs/processed_data.csv')
        print("✓ Processed data loaded")
    except FileNotFoundError:
        print("✗ Processed data not found. Train general models first.")
        return False
    
    # Train gender-specific models
    print("\n🎯 Training gender-specific models...")
    gender_predictor = GenderSpecificPredictor()
    gender_predictor.load_processed_data('outputs/processed_data.csv')
    gender_predictor.train_all_gender_models()
    gender_predictor.save_gender_models()
    
    # Print comparison
    print("\n" + "-"*70)
    gender_predictor.print_comparison()
    
    # Save summary
    gender_predictor.save_summary_report('outputs/reports/gender_models_summary.txt')
    
    return True


def main():
    """Main training pipeline."""
    print("\n" + "="*70)
    print("EMPLOYEE STRESS PREDICTION SYSTEM - MODEL TRAINING")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create directories
    create_directories()
    
    # Train general models
    if not train_general_models():
        print("✗ Failed to train general models")
        return False
    
    # Train gender-specific models
    if not train_gender_models():
        print("⚠ Warning: Failed to train gender-specific models")
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\n📊 Models saved to: models/")
    print("📁 Reports saved to: outputs/reports/")
    print("\n▶️  Next step: Run 'streamlit run dashboard.py'")
    print("="*70 + "\n")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
