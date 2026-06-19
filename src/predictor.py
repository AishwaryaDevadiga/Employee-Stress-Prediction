"""
Prediction Module
Provides functions for manual stress prediction.
"""

import numpy as np
import joblib


class ManualPredictor:
    """
    Manual predictor for employee stress levels using trained model.
    """
    
    def __init__(self, model_path, feature_names=None):
        """
        Initialize the predictor with a trained model.
        
        Parameters:
        -----------
        model_path : str
            Path to the saved model file
        feature_names : list
            List of feature names used in training
        """
        self.model = joblib.load(model_path)
        self.feature_names = feature_names
        self.stress_levels = {0: 'Low', 1: 'Medium', 2: 'High'}
        print(f"✓ Model loaded from {model_path}")
    
    def predict_stress_level(self, features):
        """
        Predict stress level for given features.
        
        Parameters:
        -----------
        features : np.ndarray or list
            Feature vector for prediction
        
        Returns:
        --------
        int
            Predicted stress level (0=Low, 1=Medium, 2=High)
        """
        features_array = np.array(features).reshape(1, -1)
        prediction = self.model.predict(features_array)[0]
        return prediction
    
    def predict_with_probability(self, features):
        """
        Predict stress level with probability/confidence.
        
        Parameters:
        -----------
        features : np.ndarray or list
            Feature vector for prediction
        
        Returns:
        --------
        dict
            Dictionary with prediction and confidence
        """
        features_array = np.array(features).reshape(1, -1)
        prediction = self.model.predict(features_array)[0]
        
        # Try to get probability (works with some models)
        result = {
            'prediction': prediction,
            'stress_level': self.stress_levels[prediction]
        }
        
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(features_array)[0]
            result['confidence'] = max(probabilities)
            result['probabilities'] = {
                self.stress_levels[i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
        
        return result
    
    def interactive_prediction(self):
        """
        Interactive prediction interface for user input.
        """
        print("\n" + "=" * 70)
        print("INTERACTIVE STRESS PREDICTION")
        print("=" * 70)
        print("\nEnter employee details for stress prediction:")
        
        features = []
        if self.feature_names:
            for feature in self.feature_names:
                while True:
                    try:
                        value = float(input(f"  {feature}: "))
                        features.append(value)
                        break
                    except ValueError:
                        print("  ✗ Invalid input. Please enter a number.")
        else:
            print("✗ Feature names not provided. Cannot run interactive prediction.")
            return None
        
        result = self.predict_with_probability(features)
        
        print(f"\n{'=' * 70}")
        print(f"PREDICTION RESULT")
        print(f"{'=' * 70}")
        print(f"Stress Level: {result['stress_level'].upper()}")
        
        if 'confidence' in result:
            print(f"Confidence: {result['confidence']:.4f}")
            print(f"Probability Distribution:")
            for level, prob in result['probabilities'].items():
                print(f"  {level}: {prob:.4f}")
        
        print(f"{'=' * 70}\n")
        
        return result


def batch_predict(model_path, X_data, feature_names=None):
    """
    Predict stress levels for multiple samples.
    
    Parameters:
    -----------
    model_path : str
        Path to the saved model
    X_data : np.ndarray or pd.DataFrame
        Features for prediction
    feature_names : list
        List of feature names
    
    Returns:
    --------
    np.ndarray
        Predicted stress levels
    """
    model = joblib.load(model_path)
    predictions = model.predict(X_data)
    return predictions


def create_prediction_example():
    """
    Create an example prediction function documentation.
    
    Returns:
    --------
    str
        Example usage documentation
    """
    example = """
    Example: Manual Stress Prediction
    ===================================
    
    from src.predictor import ManualPredictor
    
    # Load the trained model
    predictor = ManualPredictor('models/best_stress_model.pkl')
    
    # Example 1: Simple prediction
    features = [5.2, 3.1, 0.8, 4.5, 6.2, 2.1]  # Example feature values
    prediction = predictor.predict_stress_level(features)
    print(f"Stress Level: {predictor.stress_levels[prediction]}")
    
    # Example 2: Prediction with confidence
    result = predictor.predict_with_probability(features)
    print(f"Stress Level: {result['stress_level']}")
    print(f"Confidence: {result.get('confidence', 'N/A')}")
    
    # Example 3: Interactive prediction
    predictor.interactive_prediction()
    
    # Example 4: Batch prediction
    predictions = batch_predict('models/best_stress_model.pkl', X_test_data)
    """
    return example
