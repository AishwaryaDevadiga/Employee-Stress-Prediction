from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='User') # 'User' or 'Admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    years_in_company = db.Column(db.Float, nullable=False)
    prior_experience = db.Column(db.Float, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    annual_bonus = db.Column(db.Float, nullable=False)
    resting_heart_rate = db.Column(db.Integer, nullable=False)
    predicted_stress = db.Column(db.String(20), nullable=False) # 'Low', 'Medium', 'High'
    confidence_score = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to user
    user = db.relationship('User', backref=db.backref('predictions', cascade='all, delete-orphan'))

    @property
    def calculated_score(self):
        try:
            import sys
            import os
            # Ensure src is in import path to read feature_engineering
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from src.feature_engineering import get_dataset_extremes
            max_years, min_hr, max_hr = get_dataset_extremes()
        except Exception:
            max_years, min_hr, max_hr = 9.0, 55.0, 92.2

        workload = (self.years_in_company / max_years) * 10
        exp = max(self.years_in_company - self.prior_experience, 0.0)
        hr_s = ((self.resting_heart_rate - min_hr) / (max_hr - min_hr)) * 10
        raw = 0.40 * workload + 0.30 * exp + 0.30 * hr_s

        if self.predicted_stress == "Low":
            return min(max(raw, 0.0), 2.99)
        elif self.predicted_stress == "Medium":
            return min(max(raw, 3.0), 5.99)
        else:
            return min(max(raw, 6.0), 10.0)
