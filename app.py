"""
Flask Web API for Employee Stress Prediction
Provides REST endpoints for stress prediction and model information.
"""

from flask import Flask, request, jsonify, send_file
import joblib
import numpy as np
import pandas as pd
import os
from datetime import datetime


app = Flask(__name__)

# Global variables for models
general_model = None
male_model = None
female_model = None
feature_names = None


def load_models():
    """Load all trained models."""
    global general_model, male_model, female_model
    
    try:
        # Load general model
        if os.path.exists('models/best_stress_model.pkl'):
            general_model = joblib.load('models/best_stress_model.pkl')
            print("✓ General model loaded")
        
        # Load gender-specific models (if available)
        male_path = 'models/gender_specific/male_decision_tree.pkl'
        female_path = 'models/gender_specific/female_decision_tree.pkl'
        
        if os.path.exists(male_path):
            male_model = joblib.load(male_path)
            print("✓ Male-specific model loaded")
        
        if os.path.exists(female_path):
            female_model = joblib.load(female_path)
            print("✓ Female-specific model loaded")
            
    except Exception as e:
        print(f"✗ Error loading models: {str(e)}")


def get_stress_level_name(level):
    """Convert numeric stress level to name."""
    levels = {0: 'Low', 1: 'Medium', 2: 'High'}
    return levels.get(level, 'Unknown')


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Returns: JSON with API status
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'message': 'Employee Stress Prediction API is running',
        'models_loaded': {
            'general': general_model is not None,
            'male_specific': male_model is not None,
            'female_specific': female_model is not None
        }
    }), 200


@app.route('/model-info', methods=['GET'])
def model_info():
    """
    Get information about available models.
    Returns: JSON with model details
    """
    return jsonify({
        'api_version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'available_models': {
            'general': 'Decision Tree (99.4% accuracy)',
            'male_specific': 'Decision Tree (gender-specific)',
            'female_specific': 'Decision Tree (gender-specific)'
        },
        'stress_levels': {
            '0': 'Low (score < 3)',
            '1': 'Medium (score 3-6)',
            '2': 'High (score >= 6)'
        },
        'required_features': 'Contact API maintainer for feature list'
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a stress prediction.
    
    Request JSON:
    {
        "features": [f1, f2, f3, ...],
        "use_gender_specific": false,
        "gender": "male" or "female"
    }
    
    Returns: JSON with prediction and confidence
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'features' not in data:
            return jsonify({
                'error': 'Missing "features" in request body',
                'status': 'failed'
            }), 400
        
        features = data.get('features', [])
        use_gender_specific = data.get('use_gender_specific', False)
        gender = data.get('gender', '').lower()
        
        # Validate features
        if not isinstance(features, list) or len(features) == 0:
            return jsonify({
                'error': 'Features must be a non-empty list of numbers',
                'status': 'failed'
            }), 400
        
        # Convert to numpy array
        features_array = np.array(features).reshape(1, -1)
        
        # Select model
        if use_gender_specific:
            if gender not in ['male', 'female']:
                return jsonify({
                    'error': 'Gender must be "male" or "female" for gender-specific prediction',
                    'status': 'failed'
                }), 400
            
            if gender == 'male' and male_model is None:
                return jsonify({
                    'error': 'Male-specific model not available',
                    'status': 'failed'
                }), 503
            
            if gender == 'female' and female_model is None:
                return jsonify({
                    'error': 'Female-specific model not available',
                    'status': 'failed'
                }), 503
            
            model = male_model if gender == 'male' else female_model
            model_type = f'{gender.capitalize()}-specific'
        else:
            if general_model is None:
                return jsonify({
                    'error': 'General model not loaded',
                    'status': 'failed'
                }), 503
            
            model = general_model
            model_type = 'General'
        
        # Make prediction
        prediction = model.predict(features_array)[0]
        stress_level = get_stress_level_name(prediction)
        
        # Get probability if available
        confidence = None
        probabilities = None
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(features_array)[0]
            confidence = float(max(probs))
            probabilities = {
                'Low': float(probs[0]),
                'Medium': float(probs[1]),
                'High': float(probs[2])
            }
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'prediction': {
                'stress_level': stress_level,
                'stress_level_code': int(prediction),
                'confidence': confidence,
                'probability_distribution': probabilities
            },
            'model_used': model_type,
            'input_features_count': len(features)
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'status': 'failed'
        }), 500


@app.route('/compare-genders', methods=['POST'])
def compare_genders():
    """
    Compare predictions for both male and female models.
    
    Request JSON:
    {
        "features": [f1, f2, f3, ...]
    }
    
    Returns: JSON with predictions from all available models
    """
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                'error': 'Missing "features" in request body',
                'status': 'failed'
            }), 400
        
        features = data.get('features', [])
        
        if not isinstance(features, list) or len(features) == 0:
            return jsonify({
                'error': 'Features must be a non-empty list of numbers',
                'status': 'failed'
            }), 400
        
        predictions = {}
        
        # General model (21 features with Gender)
        if general_model is not None:
            features_array = np.array(features).reshape(1, -1)
            gen_pred = general_model.predict(features_array)[0]
            predictions['general'] = {
                'stress_level': get_stress_level_name(gen_pred),
                'code': int(gen_pred)
            }
        
        # Gender-specific models (20 features without Gender)
        # Remove Gender column (first feature) for gender-specific models
        if len(features) >= 21:
            features_without_gender = features[1:]  # Remove Gender column (index 0)
            features_array = np.array(features_without_gender).reshape(1, -1)
            
            # Male model
            if male_model is not None:
                male_pred = male_model.predict(features_array)[0]
                predictions['male_specific'] = {
                    'stress_level': get_stress_level_name(male_pred),
                    'code': int(male_pred)
                }
            
            # Female model
            if female_model is not None:
                female_pred = female_model.predict(features_array)[0]
                predictions['female_specific'] = {
                    'stress_level': get_stress_level_name(female_pred),
                    'code': int(female_pred)
                }
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'predictions': predictions,
            'input_features_count': len(features),
            'note': 'General model uses 21 features (with Gender), gender-specific models use 20 features (without Gender)'
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Comparison error: {str(e)}',
            'status': 'failed'
        }), 500


@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Make predictions for multiple samples.
    
    Request JSON:
    {
        "samples": [[f1, f2, ...], [f1, f2, ...], ...],
        "use_gender_specific": false,
        "gender": "male" or "female"
    }
    
    Returns: JSON with predictions for all samples
    """
    try:
        data = request.get_json()
        
        if not data or 'samples' not in data:
            return jsonify({
                'error': 'Missing "samples" in request body',
                'status': 'failed'
            }), 400
        
        samples = data.get('samples', [])
        
        if not isinstance(samples, list) or len(samples) == 0:
            return jsonify({
                'error': 'Samples must be a non-empty list',
                'status': 'failed'
            }), 400
        
        # Convert to numpy array
        features_array = np.array(samples)
        
        # Select model
        use_gender_specific = data.get('use_gender_specific', False)
        gender = data.get('gender', '').lower()
        
        if use_gender_specific:
            if gender == 'male' and male_model is None:
                return jsonify({'error': 'Male-specific model not available'}), 503
            if gender == 'female' and female_model is None:
                return jsonify({'error': 'Female-specific model not available'}), 503
            
            model = male_model if gender == 'male' else female_model
        else:
            if general_model is None:
                return jsonify({'error': 'General model not loaded'}), 503
            model = general_model
        
        # Make predictions
        predictions_list = model.predict(features_array)
        
        results = []
        for pred in predictions_list:
            results.append({
                'stress_level': get_stress_level_name(pred),
                'code': int(pred)
            })
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'predictions': results,
            'total_samples': len(results)
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Batch prediction error: {str(e)}',
            'status': 'failed'
        }), 500


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Serve the web dashboard."""
    try:
        return send_file('dashboard.html')
    except FileNotFoundError:
        return jsonify({
            'error': 'Dashboard file not found. Make sure dashboard.html is in the project root.',
            'status': 'failed'
        }), 404


@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API documentation."""
    return jsonify({
        'api_name': 'Employee Stress Prediction API',
        'version': '1.0',
        'description': 'REST API for predicting employee stress levels',
        'available_endpoints': {
            'GET /': 'This endpoint',
            'GET /health': 'Check API health status',
            'GET /model-info': 'Get model information',
            'GET /dashboard': 'Open web dashboard (UI)',
            'POST /predict': 'Make a single prediction',
            'POST /batch-predict': 'Make predictions for multiple samples',
            'POST /compare-genders': 'Compare male and female model predictions'
        },
        'quick_start': 'Visit http://localhost:5000/dashboard for the web interface'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'failed',
        'available_endpoints': [
            '/health',
            '/model-info',
            '/predict',
            '/batch-predict',
            '/compare-genders'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'status': 'failed'
    }), 500


if __name__ == '__main__':
    # Load models on startup
    print("Loading models...")
    load_models()
    
    # Start the Flask app
    print("\n" + "="*50)
    print("Employee Stress Prediction API")
    print("="*50)
    print("\n🌐 Web Dashboard: http://localhost:5000/dashboard")
    print("📡 API Base URL: http://localhost:5000")
    print("\n📍 Quick Access:")
    print("  • Dashboard (UI):  http://localhost:5000/dashboard")
    print("  • API Health:      http://localhost:5000/health")
    print("  • Model Info:      http://localhost:5000/model-info")
    print("\n📚 API Endpoints:")
    print("  • POST /predict           - Single prediction")
    print("  • POST /batch-predict     - Multiple predictions")
    print("  • POST /compare-genders   - Compare models")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
