"""
Prediction Module
Make individual and batch predictions using trained models.
"""

import pandas as pd
import numpy as np
import joblib
import os


class ManualPredictor:
    """Make manual stress predictions for individual employees."""
    
    def __init__(self, model_path='models/best_general_model.pkl'):
        """
        Initialize predictor with trained model.
        
        Parameters:
        -----------
        model_path : str
            Path to trained model pickle file
        """
        self.model = None
        self.load_model(model_path)
    
    def load_model(self, model_path):
        """
        Load trained model from disk.
        
        Parameters:
        -----------
        model_path : str
            Path to model file
        """
        try:
            self.model = joblib.load(model_path)
            print(f"✓ Model loaded from {model_path}")
        except FileNotFoundError:
            print(f"✗ Model not found at {model_path}")
            self.model = None
    
    def predict_stress_level(self, features):
        """
        Predict stress level for given features.
        
        Parameters:
        -----------
        features : array-like
            Feature vector (21 dimensions)
        
        Returns:
        --------
        int
            Stress level (0=Low, 1=Medium, 2=High)
        """
        if self.model is None:
            return None
        
        prediction = self.model.predict([features])[0]
        return int(prediction)
    
    def predict_with_probability(self, features):
        """
        Predict stress level with confidence probabilities.
        
        Parameters:
        -----------
        features : array-like
            Feature vector (21 dimensions)
        
        Returns:
        --------
        dict
            Prediction and probabilities
        """
        if self.model is None:
            return None
        
        prediction = self.model.predict([features])[0]
        probabilities = self.model.predict_proba([features])[0]
        
        return {
            'prediction': int(prediction),
            'probability': float(probabilities[int(prediction)]),
            'all_probabilities': {
                'low': float(probabilities[0]),
                'medium': float(probabilities[1]),
                'high': float(probabilities[2])
            }
        }
    
    def interactive_prediction(self):
        """Interactive loop for manual predictions."""
        print("\n" + "="*70)
        print("INTERACTIVE STRESS PREDICTION")
        print("="*70)
        
        stress_levels = ['Low', 'Medium', 'High']
        
        while True:
            try:
                print("\nEnter employee information (or 'quit' to exit):")
                
                # Get inputs
                user_input = input("Employee ID (or 'quit'): ").strip()
                if user_input.lower() == 'quit':
                    break
                
                # Collect 21 feature values
                features = []
                feature_names = [
                    'employee_id', 'age', 'age_when_joined', 'years_in_company',
                    'salary', 'bonus', 'prior_experience', 'gender', 'heart_rate',
                    'company_cheerper', 'company_glasses', 'company_pear',
                    'dept_ai', 'dept_bigdata', 'dept_design', 'dept_sales',
                    'dept_searchengine', 'dept_support',
                    'workload_score', 'experience_pressure', 'heart_rate_stress'
                ]
                
                for fname in feature_names:
                    val = float(input(f"  {fname}: "))
                    features.append(val)
                
                # Predict
                result = self.predict_with_probability(features)
                
                if result:
                    level = stress_levels[result['prediction']]
                    prob = result['probability'] * 100
                    
                    print(f"\n✓ Prediction: {level} Stress (Confidence: {prob:.1f}%)")
                    print(f"  All probabilities:")
                    print(f"    Low:    {result['all_probabilities']['low']*100:.1f}%")
                    print(f"    Medium: {result['all_probabilities']['medium']*100:.1f}%")
                    print(f"    High:   {result['all_probabilities']['high']*100:.1f}%")
            
            except ValueError:
                print("✗ Invalid input. Please enter numeric values.")
            except Exception as e:
                print(f"✗ Error: {e}")


class BatchPredictor:
    """Make batch predictions for multiple employees."""
    
    def __init__(self, model_path='models/best_general_model.pkl'):
        """
        Initialize batch predictor.
        
        Parameters:
        -----------
        model_path : str
            Path to trained model
        """
        self.model = None
        self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load trained model."""
        try:
            self.model = joblib.load(model_path)
            print(f"✓ Model loaded from {model_path}")
        except FileNotFoundError:
            print(f"✗ Model not found at {model_path}")
            self.model = None
    
    def batch_predict(self, dataframe, feature_columns=None):
        """
        Predict stress levels for multiple employees.
        
        Parameters:
        -----------
        dataframe : pd.DataFrame
            DataFrame with employee data
        feature_columns : list
            Column names to use as features
        
        Returns:
        --------
        pd.DataFrame
            Original data with predictions
        """
        if self.model is None:
            return None
        
        if feature_columns is None:
            # Use all numeric columns
            feature_columns = dataframe.select_dtypes(include=[np.number]).columns.tolist()
        
        X = dataframe[feature_columns].values
        
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        result_df = dataframe.copy()
        result_df['Stress_Level'] = predictions
        result_df['Stress_Category'] = predictions.map({0: 'Low', 1: 'Medium', 2: 'High'})
        result_df['Confidence'] = np.max(probabilities, axis=1)
        
        return result_df
    
    def predict_from_csv(self, input_path, output_path, feature_columns=None):
        """
        Predict from CSV file and save results.
        
        Parameters:
        -----------
        input_path : str
            Input CSV file path
        output_path : str
            Output CSV file path
        feature_columns : list
            Columns to use as features
        """
        try:
            df = pd.read_csv(input_path)
            predictions = self.batch_predict(df, feature_columns)
            
            if predictions is not None:
                predictions.to_csv(output_path, index=False)
                print(f"✓ Predictions saved to {output_path}")
                print(f"  Total predictions: {len(predictions)}")
                print(f"  Stress distribution:")
                print(f"    Low:    {len(predictions[predictions['Stress_Level']==0])}")
                print(f"    Medium: {len(predictions[predictions['Stress_Level']==1])}")
                print(f"    High:   {len(predictions[predictions['Stress_Level']==2])}")
                
                return predictions
        
        except FileNotFoundError:
            print(f"✗ Input file not found: {input_path}")
        except Exception as e:
            print(f"✗ Error during batch prediction: {e}")
        
        return None


class GenderSpecificPredictor:
    """Make predictions using gender-specific models."""
    
    def __init__(self, model_dir='models/gender_specific'):
        """
        Initialize gender-specific predictor.
        
        Parameters:
        -----------
        model_dir : str
            Directory containing gender-specific models
        """
        self.male_models = {}
        self.female_models = {}
        self.load_gender_models(model_dir)
    
    def load_gender_models(self, model_dir):
        """Load all gender-specific models."""
        if not os.path.exists(model_dir):
            print(f"✗ Model directory not found: {model_dir}")
            return
        
        for filename in os.listdir(model_dir):
            if filename.endswith('.pkl'):
                filepath = os.path.join(model_dir, filename)
                model = joblib.load(filepath)
                
                if 'male' in filename:
                    self.male_models[filename] = model
                elif 'female' in filename:
                    self.female_models[filename] = model
        
        print(f"✓ Loaded {len(self.male_models)} male models")
        print(f"✓ Loaded {len(self.female_models)} female models")
    
    def predict_for_gender(self, features, gender='male', model_name='decision_tree'):
        """
        Predict using gender-specific model.
        
        Parameters:
        -----------
        features : array-like
            Feature vector (20 dimensions, without gender)
        gender : str
            'male' or 'female'
        model_name : str
            Name of model to use
        
        Returns:
        --------
        dict
            Prediction and probabilities
        """
        models = self.male_models if gender == 'male' else self.female_models
        
        # Find model by name
        model = None
        for key, m in models.items():
            if model_name.lower() in key.lower():
                model = m
                break
        
        if model is None:
            return None
        
        prediction = model.predict([features])[0]
        probabilities = model.predict_proba([features])[0]
        
        return {
            'prediction': int(prediction),
            'probability': float(probabilities[int(prediction)]),
            'all_probabilities': {
                'low': float(probabilities[0]),
                'medium': float(probabilities[1]),
                'high': float(probabilities[2])
            }
        }
