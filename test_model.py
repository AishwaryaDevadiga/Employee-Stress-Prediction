import joblib
import numpy as np

# Load the model
model = joblib.load('models/best_stress_model.pkl')

# Test with different inputs
# Low stress test (young, low years in company, low HR)
test1 = np.array([[0, 25, 2, 3, 50000, 5000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 70, 2, 70, 1]])
pred1 = model.predict(test1)[0]
print(f'Test 1 (Low expected): {"Low" if pred1 == 0 else "Medium" if pred1 == 1 else "High"} (pred={pred1})')

# High stress test (older, many years, high HR)
test2 = np.array([[1, 45, 8, 5, 80000, 8000, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 95, 8, 95, 1]])
pred2 = model.predict(test2)[0]
print(f'Test 2 (High expected): {"Low" if pred2 == 0 else "Medium" if pred2 == 1 else "High"} (pred={pred2})')

print(f'\nModel classes: {model.classes_}')
print(f'Expected features: 21')

# Check if we can get probabilities
prob1 = model.predict_proba(test1)[0]
print(f'\nTest 1 probabilities: Low={prob1[0]:.2f}, Medium={prob1[1]:.2f}, High={prob1[2]:.2f}')

prob2 = model.predict_proba(test2)[0]
print(f'Test 2 probabilities: Low={prob2[0]:.2f}, Medium={prob2[1]:.2f}, High={prob2[2]:.2f}')
