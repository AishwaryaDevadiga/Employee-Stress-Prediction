# Employee Stress Prediction API Documentation

## Overview

The Employee Stress Prediction API provides REST endpoints for predicting employee stress levels using machine learning models. The API supports general models and gender-specific models for more tailored predictions.

## Features

- **Single Predictions** - Predict stress level for one employee
- **Batch Predictions** - Predict stress levels for multiple employees
- **Gender-Specific Models** - Separate models trained for male and female employees
- **Model Comparison** - Compare predictions from different models
- **Health Monitoring** - Check API status and loaded models

## Base URL

```
http://localhost:5000
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train Models (if not already done)

```bash
# Train the main model
python main.py

# Train gender-specific models
python train_gender_models.py
```

### 3. Start the API Server

```bash
python app.py
```

The server will start at `http://localhost:5000` and display available endpoints.

## API Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running and which models are loaded.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-06-17T10:40:00.123456",
  "message": "Employee Stress Prediction API is running",
  "models_loaded": {
    "general": true,
    "male_specific": true,
    "female_specific": true
  }
}
```

---

### 2. Model Information

**GET** `/model-info`

Get information about available models and stress level definitions.

**Response:**
```json
{
  "api_version": "1.0",
  "timestamp": "2024-06-17T10:40:00.123456",
  "available_models": {
    "general": "Decision Tree (99.4% accuracy)",
    "male_specific": "Decision Tree (gender-specific)",
    "female_specific": "Decision Tree (gender-specific)"
  },
  "stress_levels": {
    "0": "Low (score < 3)",
    "1": "Medium (score 3-6)",
    "2": "High (score >= 6)"
  }
}
```

---

### 3. Single Prediction

**POST** `/predict`

Make a stress prediction for a single employee.

**Request:**
```json
{
  "features": [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0],
  "use_gender_specific": false,
  "gender": "male"
}
```

**Parameters:**
- `features` (list, required): List of 21 feature values for the employee
- `use_gender_specific` (bool, optional): Use gender-specific model (default: false)
- `gender` (string, optional): "male" or "female" (required if use_gender_specific=true)

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-06-17T10:40:00.123456",
  "prediction": {
    "stress_level": "Medium",
    "stress_level_code": 1,
    "confidence": 0.95,
    "probability_distribution": {
      "Low": 0.02,
      "Medium": 0.95,
      "High": 0.03
    }
  },
  "model_used": "General",
  "input_features_count": 23
}
```

---

### 4. Batch Prediction

**POST** `/batch-predict`

Make predictions for multiple employees at once.

**Request:**
```json
{
  "samples": [
    [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0],
    [1, 35, 38, 8, 80000, 10000, 5, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 8.0, 3, 3.5, 6.0],
    [0, 30, 32, 5, 60000, 8000, 3, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 5.0, 2, 4.0, 5.0]
  ],
  "use_gender_specific": false,
  "gender": "male"
}
```

**Parameters:**
- `samples` (list of lists, required): Multiple feature vectors
- `use_gender_specific` (bool, optional): Use gender-specific model
- `gender` (string, optional): "male" or "female"

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-06-17T10:40:00.123456",
  "predictions": [
    {
      "stress_level": "Medium",
      "code": 1
    },
    {
      "stress_level": "High",
      "code": 2
    },
    {
      "stress_level": "Low",
      "code": 0
    }
  ],
  "total_samples": 3
}
```

---

### 5. Compare Models

**POST** `/compare-genders`

Get predictions from all available models for comparison.

**Request:**
```json
{
  "features": [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0]
}
```

**Parameters:**
- `features` (list, required): Employee feature vector (21 features)

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-06-17T10:40:00.123456",
  "predictions": {
    "general": {
      "stress_level": "Medium",
      "code": 1
    },
    "male_specific": {
      "stress_level": "Medium",
      "code": 1
    },
    "female_specific": {
      "stress_level": "Low",
      "code": 0
    }
  },
  "input_features_count": 23
}
```

---

## Usage Examples

### Python with Requests

```python
import requests

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Single prediction
payload = {
    'features': [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0]
}
response = requests.post('http://localhost:5000/predict', json=payload)
result = response.json()
print(f"Stress Level: {result['prediction']['stress_level']}")
print(f"Confidence: {result['prediction']['confidence']:.2%}")
```

### Using the API Client

```python
from api_examples import APIClient

client = APIClient()

# Get health status
health = client.health_check()

# Make a prediction
features = [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0, 2.73, 6.0]
result = client.predict(features)

# Batch prediction
samples = [[...], [...], [...]]
batch_result = client.batch_predict(samples)
```

### cURL

```bash
# Health check
curl http://localhost:5000/health

# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0, 25, 27, 3, 50000, 5000, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3.33, 2, 5.0, 6.0]}'
```

---

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

### 400 Bad Request
Missing required parameters or invalid data format.

```json
{
  "error": "Missing 'features' in request body",
  "status": "failed"
}
```

### 503 Service Unavailable
Required model not loaded.

```json
{
  "error": "Male-specific model not available",
  "status": "failed"
}
```

### 500 Internal Server Error
Server-side error during prediction.

```json
{
  "error": "Prediction error: [error details]",
  "status": "failed"
}
```

---

## Features Required for Prediction

The API requires 21 features in the following order:

1. Gender (0=Male, 1=Female)
2. Age
3. Age when joined
4. Years in company
5. Salary
6. Annual bonus
7. Prior years experience
8-14. One-hot encoded company features (7 binary features)
15. Employee ID encoded
16. Workload Score
17. Experience Pressure
18. Heart Rate Stress
19-21. Additional engineered features

---

## API Configuration

### Environment Variables

You can set the following environment variables before starting the API:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export API_PORT=5000
export API_HOST=0.0.0.0
```

### Running in Production

For production deployment:

```bash
# Use Gunicorn (install: pip install gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Use Waitress (install: pip install waitress)
waitress-serve --port=5000 app:app
```

---

## Performance & Limits

- **Batch Size**: Recommended maximum 1,000 samples per batch request
- **Timeout**: Requests timeout after 30 seconds
- **Rate Limiting**: Not implemented (can be added with Flask-Limiter)

---

## Support & Troubleshooting

### API won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Use a different port
python app.py --port=5001
```

### Models not loading
```bash
# Ensure models exist
# Run: python main.py
# Run: python train_gender_models.py
```

### Connection refused
```bash
# Make sure API server is running
python app.py

# Check if you can access it
curl http://localhost:5000/health
```

---

## Version History

- **v1.0** (June 2024) - Initial release with core endpoints

---

## License & Contact

For questions or issues, contact the development team.
