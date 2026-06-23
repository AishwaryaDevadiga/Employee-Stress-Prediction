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
        import os
        import pandas as pd
        max_years = 50.0
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, 'outputs', 'processed_data.csv')
            if os.path.exists(data_path):
                df_temp = pd.read_csv(data_path)
                if 'years_in_the_company' in df_temp.columns:
                    max_years = df_temp['years_in_the_company'].max()
        except Exception:
            pass

        workload = (self.years_in_company / max_years) * 10
        exp = max(self.years_in_company - self.prior_experience, 0.0)
        hr_s = ((self.resting_heart_rate - 60) / 60) * 10
        raw = 0.30 * workload + 0.20 * exp + 0.50 * hr_s

        if self.predicted_stress == "Low":
            return min(max(raw, 0.0), 3.5)
        elif self.predicted_stress == "Medium":
            return min(max(raw, 3.6), 6.5)
        else:
            return min(max(raw, 6.6), 10.0)
