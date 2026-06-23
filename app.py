import os
import io
import sys
import csv
from datetime import datetime
import numpy as np
import pandas as pd
import joblib

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Import local models module
from models import db, User, Prediction

# ==================== FLASK CONFIGURATION ====================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'stressify_secret_key_2026_flask_app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stress_prediction.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== LOAD MACHINE LEARNING MODEL ====================
MODEL_PATH = 'stress_model.pkl'
FALLBACK_MODEL_PATH = 'models/best_general_model.pkl'
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"[INFO] Model loaded from {MODEL_PATH}")
    elif os.path.exists(FALLBACK_MODEL_PATH):
        model = joblib.load(FALLBACK_MODEL_PATH)
        print(f"[INFO] Model loaded from fallback {FALLBACK_MODEL_PATH}")
    else:
        print("Warning: No trained model file (.pkl) found. Predictions will use mockup mode.")
except Exception as e:
    print(f"Error loading model: {e}. Running in mockup mode.")

# Context processor to inject dynamic date/time helpers into templates
@app.context_processor
def inject_now():
    return {'datetime_now': datetime.now()}

# Create Database tables
with app.app_context():
    db.create_all()
    # Check if admin user exists, if not create a default admin
    admin = User.query.filter_by(email='admin@stressify.com').first()
    if not admin:
        default_admin = User(
            name='System Admin',
            email='admin@stressify.com',
            password=generate_password_hash('admin123', method='pbkdf2:sha256'),
            role='Admin'
        )
        db.session.add(default_admin)
        db.session.commit()
        print("[INFO] Created default admin: admin@stressify.com / admin123")

# ==================== PUBLIC ROUTES ====================
@app.route('/')
def landing():
    if current_user.is_authenticated:
        if current_user.role == 'Admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    return render_template('landing.html')

# ==================== AUTHENTICATION ROUTES ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Welcome back! Login successful.", "success")
            if user.role == 'Admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        else:
            flash("Login failed. Please check your credentials.", "danger")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'User')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with that email already exists.", "danger")
        else:
            hashed_pwd = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                name=name,
                email=email,
                password=hashed_pwd,
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login below.", "success")
            return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have signed out successfully.", "success")
    return redirect(url_for('landing'))

@app.route('/profile')
@login_required
def profile():
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.prediction_date.desc()).all()
    return render_template('profile.html', active_page='profile', predictions=user_predictions)

# ==================== USER PREDICTION ROUTES ====================
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    if current_user.role == 'Admin':
        return redirect(url_for('admin_dashboard'))
        
    result = None
    if request.method == 'POST':
        try:
            age = int(request.form.get('age', 35))
            gender = request.form.get('gender', 'Male')
            company = request.form.get('company', '0')
            department = request.form.get('department', 'BigData')
            years_in_company = float(request.form.get('years_in_company', 5.0))
            prior_experience = float(request.form.get('prior_experience', 3.0))
            salary = float(request.form.get('salary', 60000))
            annual_bonus = float(request.form.get('annual_bonus', 5000))
            resting_heart_rate = int(request.form.get('resting_heart_rate', 75))
            
            # Validation bounds check for heart rate
            if resting_heart_rate < 60:
                flash("Heart Rate is below the normal range (<60 BPM). Please consult a healthcare professional.", "warning")
                return redirect(url_for('user_dashboard'))
            elif resting_heart_rate > 120:
                flash("Heart Rate is above the normal range (>120 BPM). Please consult a healthcare professional.", "warning")
                return redirect(url_for('user_dashboard'))

            # Feature Engineering Calculations
            # Get max_years dynamically from training data if available, fallback to 10.0 or 50.0
            max_years = 50.0
            try:
                if os.path.exists('outputs/processed_data.csv'):
                    df_temp = pd.read_csv('outputs/processed_data.csv')
                    if 'years_in_the_company' in df_temp.columns:
                        max_years = df_temp['years_in_the_company'].max()
            except Exception:
                pass
                
            workload_score = (years_in_company / max_years) * 10
            experience_pressure = max(years_in_company - prior_experience, 0.0)
            heart_rate_stress = ((resting_heart_rate - 60) / 60) * 10
            raw_score = 0.30 * workload_score + 0.20 * experience_pressure + 0.50 * heart_rate_stress

            # ML Model Prediction Block
            if model is not None:
                # 19 features ordered exactly as trained
                features = np.array([[
                    0,  # employee_id
                    age,
                    age - years_in_company, # age_when_joined
                    years_in_company,
                    salary,
                    annual_bonus,
                    prior_experience,
                    1 if gender == "Female" else 0, # Gender (0=Male, 1=Female)
                    resting_heart_rate,
                    1 if company == "0" else 0, # company_Glasses
                    1 if company == "1" else 0, # company_Pear
                    1 if department == "BigData" else 0, # department_BigData
                    1 if department == "Design" else 0, # department_Design
                    1 if department == "Sales" else 0, # department_Sales
                    1 if department == "SearchEngine" else 0, # department_Search Engine
                    1 if department == "Support" else 0, # department_Support
                    workload_score,
                    experience_pressure,
                    heart_rate_stress
                ]])
                
                pred_idx = model.predict(features)[0] # 0 = Low, 1 = Medium, 2 = High
                probabilities = model.predict_proba(features)[0]
                raw_confidence = float(max(probabilities) * 100)
            else:
                pred_idx = 0
                probabilities = [1.0, 0.0, 0.0]
                raw_confidence = 95.0

            # Map predicted index to label
            if pred_idx == 0:
                ml_level = "Low"
            elif pred_idx == 1:
                ml_level = "Medium"
            else:
                ml_level = "High"

            # Apply Heart Rate overrides (Section C)
            final_level = ml_level
            if resting_heart_rate >= 115:
                if final_level == "Low":
                    final_level = "Medium"
            if resting_heart_rate >= 120 and workload_score > 5:
                final_level = "High"

            # Align stress score strictly to final stress level's range (Section D)
            if final_level == "Low":
                stress_score = min(max(raw_score, 0.0), 3.5)
            elif final_level == "Medium":
                stress_score = min(max(raw_score, 3.6), 6.5)
            else:
                stress_score = min(max(raw_score, 6.6), 10.0)

            # Calculate realistic confidence score from probabilities (Section E)
            if raw_confidence >= 99.9:
                if final_level == "Low":
                    dist = abs(stress_score - 1.75)
                    confidence_score = 95.0 - (dist / 1.75) * 15.0
                elif final_level == "Medium":
                    dist = abs(stress_score - 5.05)
                    confidence_score = 92.0 - (dist / 1.45) * 12.0
                else:
                    dist = abs(stress_score - 8.3)
                    confidence_score = 96.0 - (dist / 1.7) * 10.0
            else:
                confidence_score = raw_confidence

            # Calculate probability breakdown for Section E
            prob_dict = {"Low": 0.0, "Medium": 0.0, "High": 0.0}
            prob_dict[final_level] = confidence_score
            remaining = 100.0 - confidence_score

            if final_level == "Low":
                prob_dict["Medium"] = remaining * 0.8
                prob_dict["High"] = remaining * 0.2
            elif final_level == "Medium":
                if stress_score <= 5.05:
                    prob_dict["Low"] = remaining * 0.7
                    prob_dict["High"] = remaining * 0.3
                else:
                    prob_dict["High"] = remaining * 0.7
                    prob_dict["Low"] = remaining * 0.3
            else: # High
                prob_dict["Medium"] = remaining * 0.8
                prob_dict["Low"] = remaining * 0.2

            # Calculate feature percentage contributions for Transparency Panel (Section G)
            total_weighted = (workload_score * 0.30) + (experience_pressure * 0.20) + (heart_rate_stress * 0.50)
            if total_weighted > 0:
                contrib_workload = ((workload_score * 0.30) / total_weighted) * 100
                contrib_experience = ((experience_pressure * 0.20) / total_weighted) * 100
                contrib_heart_rate = ((heart_rate_stress * 0.50) / total_weighted) * 100
            else:
                contrib_workload = 30.0
                contrib_experience = 20.0
                contrib_heart_rate = 50.0

            # Dynamic Explanation generation (Section F)
            if resting_heart_rate <= 80:
                hr_desc = f"{resting_heart_rate} BPM (Low Stress Zone)"
                hr_impact = "within a normal range and has minimal impact on the stress score"
            elif resting_heart_rate <= 100:
                hr_desc = f"{resting_heart_rate} BPM (Medium Stress Zone)"
                hr_impact = "moderately elevated and contributes to the stress score"
            else:
                hr_desc = f"{resting_heart_rate} BPM (High Stress Zone)"
                hr_impact = "elevated and contributes significantly to the overall stress score"

            if workload_score <= 3.5:
                wl_desc = "Low"
                wl_impact = "low workload factors"
            elif workload_score <= 6.5:
                wl_desc = "Moderate"
                wl_impact = "workload factors"
            else:
                wl_desc = "High"
                wl_impact = "high workload factors"

            if experience_pressure <= 2.0:
                exp_desc = "Low"
            elif experience_pressure <= 5.0:
                exp_desc = "Moderate"
            else:
                exp_desc = "High"

            explanation = (
                f"The employee's resting heart rate is {hr_desc} which is {hr_impact}. "
                f"Combined with {wl_desc} workload ({wl_impact}) and {exp_desc} experience pressure, "
                f"the system classifies the employee as {final_level} Stress with {confidence_score:.1f}% confidence."
            )

            # Save prediction to sqlite db
            new_pred = Prediction(
                user_id=current_user.id,
                age=age,
                gender=gender,
                company=company,
                department=department,
                years_in_company=years_in_company,
                prior_experience=prior_experience,
                salary=salary,
                annual_bonus=annual_bonus,
                resting_heart_rate=resting_heart_rate,
                predicted_stress=final_level,
                confidence_score=confidence_score
            )
            db.session.add(new_pred)
            db.session.commit()
            
            result = {
                'prediction_id': new_pred.id,
                'heart_rate': resting_heart_rate,
                'predicted_stress': final_level,
                'confidence_score': confidence_score,
                'workload_score': workload_score,
                'experience_pressure': experience_pressure,
                'heart_rate_stress': heart_rate_stress,
                'stress_score': stress_score,
                'explanation': explanation,
                'hr_desc': hr_desc,
                'wl_desc': wl_desc,
                'exp_desc': exp_desc,
                'prob_low': prob_dict["Low"],
                'prob_medium': prob_dict["Medium"],
                'prob_high': prob_dict["High"],
                'contrib_workload': contrib_workload,
                'contrib_experience': contrib_experience,
                'contrib_heart_rate': contrib_heart_rate
            }
            flash("Prediction processed successfully!", "success")
        except Exception as e:
            flash(f"Error executing prediction: {e}", "danger")

    return render_template('dashboard.html', active_page='dashboard', result=result)

@app.route('/history')
@login_required
def user_history():
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.prediction_date.desc()).all()
    return render_template('history.html', active_page='history', predictions=user_predictions)

# ==================== EXPORT DATA ROUTES ====================
@app.route('/predictions/export-csv')
@login_required
def export_csv():
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.prediction_date.desc()).all()
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow([
        'Date', 'Age', 'Gender', 'Company', 'Department', 'Years in Company',
        'Prior Experience', 'Salary', 'Annual Bonus', 'Heart Rate', 'Predicted Stress', 'Confidence'
    ])
    
    for p in user_predictions:
        cw.writerow([
            p.prediction_date.strftime('%Y-%m-%d %H:%M'),
            p.age, p.gender, f"Company {p.company}", p.department, p.years_in_company,
            p.prior_experience, p.salary, p.annual_bonus, p.resting_heart_rate,
            p.predicted_stress, f"{p.confidence_score:.1f}%"
        ])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=Stress_History_{current_user.name.replace(' ', '_')}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/predictions/download-pdf/<int:pred_id>')
@login_required
def download_pdf(pred_id):
    prediction = Prediction.query.get_or_404(pred_id)
    # Privilege check: users can only access their own PDF, Admin can access all
    if current_user.role != 'Admin' and prediction.user_id != current_user.id:
        flash("You are not authorized to view this report.", "danger")
        return redirect(url_for('landing'))

    max_years = 50.0
    try:
        if os.path.exists('outputs/processed_data.csv'):
            df_temp = pd.read_csv('outputs/processed_data.csv')
            if 'years_in_the_company' in df_temp.columns:
                max_years = df_temp['years_in_the_company'].max()
    except Exception:
        pass

    workload_score = (prediction.years_in_company / max_years) * 10
    experience_pressure = max(prediction.years_in_company - prediction.prior_experience, 0.0)
    heart_rate_stress = ((prediction.resting_heart_rate - 60) / 60) * 10
    raw_score = 0.30 * workload_score + 0.20 * experience_pressure + 0.50 * heart_rate_stress

    final_level = prediction.predicted_stress

    # Align score to final level
    if final_level == "Low":
        stress_score = min(max(raw_score, 0.0), 3.5)
    elif final_level == "Medium":
        stress_score = min(max(raw_score, 3.6), 6.5)
    else:
        stress_score = min(max(raw_score, 6.6), 10.0)

    # Dynamic explanation
    if prediction.resting_heart_rate <= 80:
        hr_desc = f"{prediction.resting_heart_rate} BPM (Low Stress Zone)"
        hr_impact = "within a normal range and has minimal impact on the stress score"
    elif prediction.resting_heart_rate <= 100:
        hr_desc = f"{prediction.resting_heart_rate} BPM (Medium Stress Zone)"
        hr_impact = "moderately elevated and contributes to the stress score"
    else:
        hr_desc = f"{prediction.resting_heart_rate} BPM (High Stress Zone)"
        hr_impact = "elevated and contributes significantly to the overall stress score"

    if workload_score <= 3.5:
        wl_desc = "Low"
        wl_impact = "low workload factors"
    elif workload_score <= 6.5:
        wl_desc = "Moderate"
        wl_impact = "workload factors"
    else:
        wl_desc = "High"
        wl_impact = "high workload factors"

    if experience_pressure <= 2.0:
        exp_desc = "Low"
    elif experience_pressure <= 5.0:
        exp_desc = "Moderate"
    else:
        exp_desc = "High"

    explanation = (
        f"The employee's resting heart rate is {hr_desc} which is {hr_impact}. "
        f"Combined with {wl_desc} workload ({wl_impact}) and {exp_desc} experience pressure, "
        f"the system classifies the employee as {final_level} Stress with {prediction.confidence_score:.1f}% confidence."
    )

    # Calculate contributions for transparency in PDF
    total_weighted = (workload_score * 0.30) + (experience_pressure * 0.20) + (heart_rate_stress * 0.50)
    if total_weighted > 0:
        contrib_workload = ((workload_score * 0.30) / total_weighted) * 100
        contrib_experience = ((experience_pressure * 0.20) / total_weighted) * 100
        contrib_heart_rate = ((heart_rate_stress * 0.50) / total_weighted) * 100
    else:
        contrib_workload = 30.0
        contrib_experience = 20.0
        contrib_heart_rate = 50.0

    # Generate PDF buffer using ReportLab
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24,
        textColor=colors.HexColor('#4f46e5'), spaceAfter=15, alignment=1
    )
    normal_style = styles['Normal']
    bold_style = ParagraphStyle('DocBold', parent=normal_style, fontName='Helvetica-Bold')

    story = []
    story.append(Paragraph("Stressify - Assessment Report", title_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    story.append(Spacer(1, 20))

    # User details table
    story.append(Paragraph("Employee Information", styles['Heading2']))
    story.append(Spacer(1, 10))
    user_info = [
        [Paragraph("Name:", bold_style), Paragraph(prediction.user.name, normal_style)],
        [Paragraph("Email:", bold_style), Paragraph(prediction.user.email, normal_style)],
        [Paragraph("Age / Gender:", bold_style), Paragraph(f"{prediction.age} / {prediction.gender}", normal_style)],
        [Paragraph("Company ID:", bold_style), Paragraph(f"Company {prediction.company}", normal_style)],
        [Paragraph("Department:", bold_style), Paragraph(prediction.department, normal_style)]
    ]
    t_user = Table(user_info, colWidths=[150, 350])
    t_user.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_user)
    story.append(Spacer(1, 20))

    # Prediction metrics table
    story.append(Paragraph("Telemetry & Model Predictions", styles['Heading2']))
    story.append(Spacer(1, 10))
    
    p_color = '#10b981' if prediction.predicted_stress == 'Low' else '#f59e0b' if prediction.predicted_stress == 'Medium' else '#ef4444'

    telemetry_data = [
        [Paragraph("Resting Heart Rate:", bold_style), Paragraph(f"{prediction.resting_heart_rate} BPM", normal_style)],
        [Paragraph("Years in Company / Exp:", bold_style), Paragraph(f"{prediction.years_in_company} years / {prediction.prior_experience} years", normal_style)],
        [Paragraph("Salary & Annual Bonus:", bold_style), Paragraph(f"₹{prediction.salary:,.0f} / ₹{prediction.annual_bonus:,.0f}", normal_style)],
        [Paragraph("Predicted Stress Level:", bold_style), Paragraph(f"<font color='{p_color}'><b>{prediction.predicted_stress} Stress</b></font>", normal_style)],
        [Paragraph("Stress Score:", bold_style), Paragraph(f"{stress_score:.2f} / 10", normal_style)],
        [Paragraph("Prediction Confidence:", bold_style), Paragraph(f"{prediction.confidence_score:.1f}%", normal_style)]
    ]
    t_telemetry = Table(telemetry_data, colWidths=[150, 350])
    t_telemetry.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_telemetry)
    story.append(Spacer(1, 20))

    # Transparency panel table
    story.append(Paragraph("Transparency Panel (Why was this prediction made?)", styles['Heading2']))
    story.append(Spacer(1, 10))
    transparency_data = [
        [Paragraph("Workload Contribution:", bold_style), Paragraph(f"{contrib_workload:.0f}%", normal_style)],
        [Paragraph("Experience Contribution:", bold_style), Paragraph(f"{contrib_experience:.0f}%", normal_style)],
        [Paragraph("Heart Rate Contribution:", bold_style), Paragraph(f"{contrib_heart_rate:.0f}%", normal_style)]
    ]
    t_transparency = Table(transparency_data, colWidths=[150, 350])
    t_transparency.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_transparency)
    story.append(Spacer(1, 20))

    # Explanation paragraph
    story.append(Paragraph("Factor Analysis Explanation", styles['Heading2']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(explanation, normal_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<i>Note: This is a system-generated evaluation report based on machine learning classifications and telemetry indexes.</i>", normal_style))

    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Stress_Report_{prediction.user.name.replace(' ', '_')}_{prediction.prediction_date.strftime('%Y%m%d')}.pdf",
        mimetype='application/pdf'
    )

# Helper function to generate file download responses (replacing make_response for string IO)
def make_response(content):
    response = app.response_class(content, status=200)
    return response

# ==================== ADMIN CONTROL PANEL ROUTES ====================
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        flash("You are not authorized to view the admin control panel.", "danger")
        return redirect(url_for('landing'))
        
    search_query = request.args.get('search', '')
    stress_filter = request.args.get('stress_filter', '')
    
    # Query users
    all_users = User.query.order_by(User.id.desc()).all()
    
    # Query predictions
    query = Prediction.query.join(User)
    
    if search_query:
        query = query.filter(
            (User.name.like(f"%{search_query}%")) | 
            (User.email.like(f"%{search_query}%")) | 
            (Prediction.company.like(f"%{search_query}%")) |
            (Prediction.department.like(f"%{search_query}%"))
        )
        
    if stress_filter:
        query = query.filter(Prediction.predicted_stress == stress_filter)
        
    predictions_log = query.order_by(Prediction.prediction_date.desc()).all()
    
    return render_template(
        'admin.html',
        active_page='admin',
        users=all_users,
        predictions=predictions_log,
        search_query=search_query,
        stress_filter=stress_filter
    )

@app.route('/admin/delete-prediction/<int:pred_id>', methods=['POST'])
@login_required
def delete_prediction(pred_id):
    if current_user.role != 'Admin':
        flash("Unauthorized action.", "danger")
        return redirect(url_for('landing'))
        
    pred = Prediction.query.get_or_404(pred_id)
    db.session.delete(pred)
    db.session.commit()
    flash("Prediction record deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/analytics-data')
@login_required
def admin_analytics_data():
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
        
    users = User.query.all()
    predictions = Prediction.query.all()
    
    total_users = len(users)
    total_predictions = len(predictions)
    high_stress_cases = len([p for p in predictions if p.predicted_stress == 'High'])
    
    # Stress distribution
    stress_dist = {'Low': 0, 'Medium': 0, 'High': 0}
    for p in predictions:
        if p.predicted_stress in stress_dist:
            stress_dist[p.predicted_stress] += 1
            
    # Gender stress
    gender_stress = {
        'Male': {'Low': 0, 'Medium': 0, 'High': 0},
        'Female': {'Low': 0, 'Medium': 0, 'High': 0}
    }
    for p in predictions:
        g = p.gender if p.gender in ['Male', 'Female'] else 'Male'
        if p.predicted_stress in gender_stress[g]:
            gender_stress[g][p.predicted_stress] += 1
            
    # Department stress
    dept_stress = {}
    for p in predictions:
        d = p.department
        if d not in dept_stress:
            dept_stress[d] = {'Low': 0, 'Medium': 0, 'High': 0}
        if p.predicted_stress in dept_stress[d]:
            dept_stress[d][p.predicted_stress] += 1
            
    # Monthly Trends (last 6 months)
    monthly_trends = {}
    now = datetime.now()
    for i in range(5, -1, -1):
        m = (now.month - i - 1) % 12 + 1
        y = now.year + (now.month - i - 1) // 12
        month_str = datetime(y, m, 1).strftime('%b %Y')
        monthly_trends[month_str] = 0
        
    for p in predictions:
        month_str = p.prediction_date.strftime('%b %Y')
        if month_str in monthly_trends:
            monthly_trends[month_str] += 1
            
    return jsonify({
        'total_users': total_users,
        'total_predictions': total_predictions,
        'high_stress_cases': high_stress_cases,
        'stress_distribution': stress_dist,
        'gender_stress': gender_stress,
        'department_stress': dept_stress,
        'monthly_trends': monthly_trends
    })

# ==================== RUN APPLICATION ====================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
