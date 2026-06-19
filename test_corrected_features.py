import joblib
import numpy as np

# Load the model
model = joblib.load('models/best_stress_model.pkl')

# Test Low Stress (young person with low years in company, low heart rate)
# age=25, yearsCompany=2, priorExp=3, salary=50000, basicSalary=5000, 
# gender=0 (male), heartRate=70, company=0
ageWhenJoined = 25 - 2
workloadScore = (2 / 10) * 10  # 2
experiencePressure = max(2 - 3, 0)  # 0
heartRateStress = ((70 - 40) / (200 - 40)) * 10  # 1.875

test1 = np.array([[
    1,  # employee_id
    25,  # age
    ageWhenJoined,  # age_when_joined
    2,  # years_in_company
    50000,  # salary
    5000,  # annual_bonus
    3,  # prior_experience
    0,  # Gender (male)
    70,  # heart_rate
    1,  # company_Cheerper
    0,  # company_Glasses
    0,  # company_Pear
    0, 0, 0, 0, 0, 0,  # departments
    workloadScore,
    experiencePressure,
    heartRateStress
]])

pred1 = model.predict(test1)[0]
prob1 = model.predict_proba(test1)[0]
print(f'Test 1 (Low stress expected):')
print(f'  Prediction: {"Low" if pred1 == 0 else "Medium" if pred1 == 1 else "High"} ({pred1})')
print(f'  Probabilities: Low={prob1[0]:.3f}, Medium={prob1[1]:.3f}, High={prob1[2]:.3f}')

# Test High Stress (older person with many years, high heart rate)
# age=45, yearsCompany=8, priorExp=5, salary=80000, basicSalary=8000,
# gender=1 (female), heartRate=95, company=2
ageWhenJoined2 = 45 - 8
workloadScore2 = (8 / 10) * 10  # 8
experiencePressure2 = max(8 - 5, 0)  # 3
heartRateStress2 = ((95 - 40) / (200 - 40)) * 10  # 3.44

test2 = np.array([[
    1,  # employee_id
    45,  # age
    ageWhenJoined2,  # age_when_joined
    8,  # years_in_company
    80000,  # salary
    8000,  # annual_bonus
    5,  # prior_experience
    1,  # Gender (female)
    95,  # heart_rate
    0,  # company_Cheerper
    0,  # company_Glasses
    1,  # company_Pear
    0, 0, 0, 0, 0, 0,  # departments
    workloadScore2,
    experiencePressure2,
    heartRateStress2
]])

pred2 = model.predict(test2)[0]
prob2 = model.predict_proba(test2)[0]
print(f'\nTest 2 (High stress expected):')
print(f'  Prediction: {"Low" if pred2 == 0 else "Medium" if pred2 == 1 else "High"} ({pred2})')
print(f'  Probabilities: Low={prob2[0]:.3f}, Medium={prob2[1]:.3f}, High={prob2[2]:.3f}')

# Test Medium Stress
# age=35, yearsCompany=5, priorExp=4, salary=65000, basicSalary=6500,
# gender=0 (male), heartRate=80, company=1
ageWhenJoined3 = 35 - 5
workloadScore3 = (5 / 10) * 10  # 5
experiencePressure3 = max(5 - 4, 0)  # 1
heartRateStress3 = ((80 - 40) / (200 - 40)) * 10  # 2.5

test3 = np.array([[
    1,  # employee_id
    35,  # age
    ageWhenJoined3,  # age_when_joined
    5,  # years_in_company
    65000,  # salary
    6500,  # annual_bonus
    4,  # prior_experience
    0,  # Gender (male)
    80,  # heart_rate
    0,  # company_Cheerper
    1,  # company_Glasses
    0,  # company_Pear
    0, 0, 0, 0, 0, 0,  # departments
    workloadScore3,
    experiencePressure3,
    heartRateStress3
]])

pred3 = model.predict(test3)[0]
prob3 = model.predict_proba(test3)[0]
print(f'\nTest 3 (Medium stress expected):')
print(f'  Prediction: {"Low" if pred3 == 0 else "Medium" if pred3 == 1 else "High"} ({pred3})')
print(f'  Probabilities: Low={prob3[0]:.3f}, Medium={prob3[1]:.3f}, High={prob3[2]:.3f}')
