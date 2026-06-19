"""
Train Gender-Specific Models
Script to train separate models for male and female employees.
"""

import sys
from src.gender_specific_models import train_gender_specific_models


def main():
    """Execute gender-specific model training."""
    
    print("\n" + "=" * 70)
    print("TRAINING GENDER-SPECIFIC STRESS PREDICTION MODELS")
    print("=" * 70)
    
    try:
        # Train gender-specific models
        predictor = train_gender_specific_models('outputs/processed_data.csv')
        
        print("\n" + "=" * 70)
        print("GENDER-SPECIFIC MODEL TRAINING COMPLETED!")
        print("=" * 70)
        print("\nGenerated Files:")
        print("  ✓ models/gender_specific/male_decision_tree.pkl")
        print("  ✓ models/gender_specific/male_random_forest.pkl")
        print("  ✓ models/gender_specific/male_logistic_regression.pkl")
        print("  ✓ models/gender_specific/male_svm.pkl")
        print("  ✓ models/gender_specific/female_decision_tree.pkl")
        print("  ✓ models/gender_specific/female_random_forest.pkl")
        print("  ✓ models/gender_specific/female_logistic_regression.pkl")
        print("  ✓ models/gender_specific/female_svm.pkl")
        print("  ✓ outputs/results/gender_specific_summary.txt")
        print("=" * 70 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease ensure:")
        print("  1. The processed dataset exists at: outputs/processed_data.csv")
        print("  2. Run main.py first to generate the processed data")
    except Exception as e:
        print(f"\n✗ Unexpected error: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
