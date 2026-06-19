"""
Employee Stress Prediction - Main Pipeline
Complete machine learning pipeline for predicting employee stress levels.
"""

import os
import sys
import pandas as pd
import numpy as np

# Import custom modules
from src.data_loader import load_dataset, explore_dataset
from src.preprocessing import preprocess_data
from src.feature_engineering import engineer_features
from src.model_trainer import StressPredictor
from src.visualization import (
    plot_accuracy_comparison, 
    plot_confusion_matrices,
    plot_feature_importance,
    plot_stress_distribution,
    save_classification_reports
)


def create_directories():
    """Create necessary output directories."""
    directories = ['models', 'outputs/plots', 'outputs/results']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ Output directories created/verified")


def main():
    """
    Execute the complete machine learning pipeline.
    """
    
    print("\n" + "=" * 70)
    print("EMPLOYEE STRESS PREDICTION - ML PIPELINE")
    print("=" * 70)
    
    # Step 1: Create output directories
    print("\n[Step 1/11] Creating output directories...")
    create_directories()
    
    # Step 2: Load dataset
    print("\n[Step 2/11] Loading dataset...")
    dataset_path = "dataset/company_employee_details4999.csv"
    df = load_dataset(dataset_path)
    
    # Step 3: Exploratory Data Analysis
    print("\n[Step 3/11] Exploratory Data Analysis...")
    explore_dataset(df)
    
    # Step 4: Data Preprocessing
    print("\n[Step 4/11] Data Preprocessing...")
    df = preprocess_data(df)
    
    # Step 5: Feature Engineering
    print("\n[Step 5/11] Feature Engineering...")
    df = engineer_features(df)
    
    # Step 6: Save processed dataset
    processed_path = "outputs/processed_data.csv"
    df.to_csv(processed_path, index=False)
    print(f"✓ Processed dataset saved to {processed_path}")
    
    # Step 7: Prepare data for modeling
    print("\n[Step 7/11] Preparing data for modeling...")
    predictor = StressPredictor()
    predictor.prepare_data(df)
    
    # Step 8: Train all models
    print("\n[Step 8/11] Training models...")
    predictor.train_all_models()
    
    # Step 9: Evaluate models
    print("\n[Step 9/11] Evaluating models...")
    predictor.evaluate_models()
    
    # Step 10: Cross-validation
    print("\n[Step 10/11] Performing 5-fold cross-validation...")
    predictor.cross_validate(cv_folds=5)
    
    # Step 11: Generate visualizations and save results
    print("\n[Step 11/11] Generating visualizations and saving results...")
    
    # Save best model
    model_path = "models/best_stress_model.pkl"
    predictor.save_best_model(model_path)
    
    # Accuracy comparison plot
    accuracies = predictor.get_accuracy_comparison()
    plot_accuracy_comparison(accuracies)
    
    # Confusion matrices
    plot_confusion_matrices(predictor.results)
    
    # Feature importance
    feature_importance_df = predictor.get_feature_importance('Random Forest')
    if feature_importance_df is not None:
        plot_feature_importance(feature_importance_df)
    
    # Stress distribution
    plot_stress_distribution(df)
    
    # Save classification reports
    save_classification_reports(predictor.results)
    
    # Save summary report
    summary_path = "outputs/results/model_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("EMPLOYEE STRESS PREDICTION - MODEL SUMMARY\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("BEST MODEL:\n")
        f.write(f"  Name: {predictor.best_model_name}\n")
        f.write(f"  Accuracy: {predictor.results[predictor.best_model_name]['accuracy']:.4f}\n")
        f.write(f"  Precision: {predictor.results[predictor.best_model_name]['precision']:.4f}\n")
        f.write(f"  Recall: {predictor.results[predictor.best_model_name]['recall']:.4f}\n")
        f.write(f"  F1-Score: {predictor.results[predictor.best_model_name]['f1_score']:.4f}\n\n")
        
        f.write("ALL MODELS PERFORMANCE:\n")
        for model_name, metrics in predictor.results.items():
            f.write(f"\n  {model_name}:\n")
            f.write(f"    Accuracy: {metrics['accuracy']:.4f}\n")
            f.write(f"    Precision: {metrics['precision']:.4f}\n")
            f.write(f"    Recall: {metrics['recall']:.4f}\n")
            f.write(f"    F1-Score: {metrics['f1_score']:.4f}\n")
        
        f.write("\n\nMODEL SAVED AT:\n")
        f.write(f"  {model_path}\n")
    
    print(f"✓ Model summary saved to {summary_path}")
    
    # Final completion message
    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nGenerated Outputs:")
    print(f"  ✓ Best Model: {model_path}")
    print(f"  ✓ Processed Data: {processed_path}")
    print(f"  ✓ Plots: outputs/plots/")
    print(f"  ✓ Reports: outputs/results/")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease ensure:")
        print("  1. The dataset file exists at: dataset/company_employee_details4999.csv")
        print("  2. You are running this script from the project root directory")
    except Exception as e:
        print(f"\n✗ Unexpected error: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        import traceback
        traceback.print_exc()
