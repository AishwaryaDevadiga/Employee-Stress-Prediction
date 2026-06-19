"""
API Usage Examples
Demonstrates how to use the Employee Stress Prediction API.
"""

import requests
import json


class APIClient:
    """Client for the Employee Stress Prediction API."""
    
    def __init__(self, base_url='http://localhost:5000'):
        """Initialize the API client."""
        self.base_url = base_url
    
    def health_check(self):
        """Check API health status."""
        response = requests.get(f'{self.base_url}/health')
        return response.json()
    
    def get_model_info(self):
        """Get model information."""
        response = requests.get(f'{self.base_url}/model-info')
        return response.json()
    
    def predict(self, features, use_gender_specific=False, gender='male'):
        """
        Make a prediction.
        
        Parameters:
        -----------
        features : list
            List of feature values
        use_gender_specific : bool
            Use gender-specific model
        gender : str
            'male' or 'female'
        
        Returns:
        --------
        dict
            Prediction result
        """
        payload = {
            'features': features,
            'use_gender_specific': use_gender_specific,
            'gender': gender
        }
        response = requests.post(f'{self.base_url}/predict', json=payload)
        return response.json()
    
    def batch_predict(self, samples, use_gender_specific=False, gender='male'):
        """
        Make batch predictions.
        
        Parameters:
        -----------
        samples : list of lists
            Multiple feature vectors
        use_gender_specific : bool
            Use gender-specific model
        gender : str
            'male' or 'female'
        
        Returns:
        --------
        dict
            Batch prediction results
        """
        payload = {
            'samples': samples,
            'use_gender_specific': use_gender_specific,
            'gender': gender
        }
        response = requests.post(f'{self.base_url}/batch-predict', json=payload)
        return response.json()
    
    def compare_genders(self, features):
        """
        Compare predictions from all models.
        
        Parameters:
        -----------
        features : list
            Feature values
        
        Returns:
        --------
        dict
            Predictions from all models
        """
        payload = {'features': features}
        response = requests.post(f'{self.base_url}/compare-genders', json=payload)
        return response.json()


def print_result(title, result):
    """Pretty print API result."""
    print(f"\n{title}")
    print("=" * 70)
    print(json.dumps(result, indent=2))


# Example Usage
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("EMPLOYEE STRESS PREDICTION API - USAGE EXAMPLES")
    print("=" * 70)
    
    # Initialize client
    client = APIClient('http://localhost:5000')
    
    # Example 1: Health check
    print("\n[Example 1] Health Check")
    try:
        health = client.health_check()
        print_result("API Health Status:", health)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        print("\nNote: Make sure the API server is running!")
        print("Run: python app.py")
    
    # Example 2: Get model info
    print("\n[Example 2] Model Information")
    try:
        info = client.get_model_info()
        print_result("Model Information:", info)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Example 3: Single prediction (general model)
    print("\n[Example 3] Single Prediction (General Model)")
    try:
        # Example feature values (21 features - after removing Stress_Level and Stress_Score)
        features = [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0]
        result = client.predict(features, use_gender_specific=False)
        print_result("Single Prediction Result:", result)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Example 4: Single prediction (gender-specific)
    print("\n[Example 4] Single Prediction (Male-Specific Model)")
    try:
        # 20 features for gender-specific model (no Gender column needed)
        features = [25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0]
        result = client.predict(features, use_gender_specific=True, gender='male')
        print_result("Male-Specific Prediction:", result)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Example 5: Batch prediction
    print("\n[Example 5] Batch Prediction (Multiple Samples)")
    try:
        samples = [
            [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0],
            [1, 35, 38, 8, 80000, 10000, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 8.0, 3, 3.5, 6.0],
            [0, 30, 32, 5, 60000, 8000, 3, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 5.0, 2, 4.0, 5.0]
        ]
        result = client.batch_predict(samples)
        print_result("Batch Prediction Results:", result)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # Example 6: Compare gender models
    print("\n[Example 6] Compare All Models (General Model Only)")
    try:
        # Use 21 features for general model
        features = [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0]
        result = client.compare_genders(features)
        print_result("Model Comparison:", result)
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 70)
    print("END OF EXAMPLES")
    print("=" * 70 + "\n")
