import sqlite3
import hashlib
import os
import pandas as pd
from datetime import datetime, timedelta

DB_PATH = 'streamlit_rbac.db'

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_connection():
    """Return a database connection."""
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize the database schema and seed default values if needed."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL, -- 'Administrator' or 'Employee/User'
        gender TEXT NOT NULL, -- 'Male' or 'Female'
        age INTEGER NOT NULL,
        company TEXT NOT NULL,
        department TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create predictions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        company TEXT NOT NULL,
        department TEXT NOT NULL,
        years_in_company REAL NOT NULL,
        prior_experience REAL NOT NULL,
        salary REAL NOT NULL,
        annual_bonus REAL NOT NULL,
        resting_heart_rate INTEGER NOT NULL,
        predicted_stress TEXT NOT NULL, -- 'Low', 'Medium', 'High'
        confidence_score REAL NOT NULL,
        stress_score REAL NOT NULL,
        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

    # Check if admin user exists, if not seed it
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO users (name, username, password, role, gender, age, company, department)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Admin User",
            "admin",
            hash_password("admin123"),
            "Administrator",
            "Male",
            35,
            "Corporate",
            "Executive"
        ))
        conn.commit()

    # Check if test employee user exists, if not seed it
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'employee'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO users (name, username, password, role, gender, age, company, department)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "John Doe",
            "employee",
            hash_password("password123"),
            "Employee/User",
            "Male",
            30,
            "Glasses",
            "BigData"
        ))
        conn.commit()

    # Check if predictions table is empty, if so seed historical data from outputs/processed_data.csv
    cursor.execute("SELECT COUNT(*) FROM predictions")
    if cursor.fetchone()[0] == 0:
        processed_data_path = 'outputs/processed_data.csv'
        if os.path.exists(processed_data_path):
            try:
                df = pd.read_csv(processed_data_path)
                # Seed timestamps spread over the last 30 days
                n_records = len(df)
                start_time = datetime.now() - timedelta(days=30)
                
                rows_to_insert = []
                for i, row in df.iterrows():
                    # Reconstruct gender
                    gender_code = row.get('Gender', 0)
                    gender_str = 'Female' if gender_code == 1 else 'Male'
                    
                    # Reconstruct company
                    if row.get('company_Glasses', 0) == 1:
                        company_str = 'Glasses'
                    elif row.get('company_Pear', 0) == 1:
                        company_str = 'Pear'
                    else:
                        company_str = 'Cheerper'
                        
                    # Reconstruct department
                    if row.get('department_BigData', 0) == 1:
                        dept_str = 'BigData'
                    elif row.get('department_Design', 0) == 1:
                        dept_str = 'Design'
                    elif row.get('department_Sales', 0) == 1:
                        dept_str = 'Sales'
                    elif row.get('department_Search Engine', 0) == 1:
                        dept_str = 'Search Engine'
                    elif row.get('department_Support', 0) == 1:
                        dept_str = 'Support'
                    else:
                        dept_str = 'AI'
                    
                    # Map stress level back to string
                    level_raw = row.get('Stress_Level', 0)
                    if level_raw in [0, '0', 'Low']:
                        level_str = 'Low'
                    elif level_raw in [1, '1', 'Medium']:
                        level_str = 'Medium'
                    else:
                        level_str = 'High'
                        
                    # Generate a timestamp spread over 30 days
                    row_time = start_time + timedelta(seconds=i * (30 * 86400 / n_records))
                    
                    rows_to_insert.append((
                        f"historical_emp_{row.get('employee_id', i)}",
                        int(row.get('age', 30)),
                        gender_str,
                        company_str,
                        dept_str,
                        float(row.get('years_in_the_company', 2.0)),
                        float(row.get('prior_years_experience', 1.0)),
                        float(row.get('salary', 50000.0)),
                        float(row.get('annual_bonus', 5000.0)),
                        int(row.get('Resting_Heart_Rate', 72)),
                        level_str,
                        95.0, # Dummy confidence
                        float(row.get('Stress_Score', 3.0)),
                        row_time.strftime('%Y-%m-%d %H:%M:%S')
                    ))
                
                cursor.executemany("""
                INSERT INTO predictions (
                    username, age, gender, company, department, 
                    years_in_company, prior_experience, salary, annual_bonus, 
                    resting_heart_rate, predicted_stress, confidence_score, stress_score, prediction_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, rows_to_insert)
                conn.commit()
            except Exception as e:
                print(f"Error seeding historical data: {e}")
                
    conn.close()

def register_user(name, username, password, gender, age, company, department):
    """Register a new employee. Returns True if successful, False if username exists."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Check if username exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            return False
            
        cursor.execute("""
        INSERT INTO users (name, username, password, role, gender, age, company, department)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            username,
            hash_password(password),
            "Employee/User",
            gender,
            int(age),
            company,
            department
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Registration error: {e}")
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    """Authenticate credentials. Returns user detail dict or None."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT name, username, role, gender, age, company, department FROM users
        WHERE username = ? AND password = ?
        """, (username, hash_password(password)))
        row = cursor.fetchone()
        if row:
            return {
                "name": row[0],
                "username": row[1],
                "role": row[2],
                "gender": row[3],
                "age": row[4],
                "company": row[5],
                "department": row[6]
            }
        return None
    except Exception as e:
        print(f"Auth error: {e}")
        return None
    finally:
        conn.close()

def get_user_profile(username):
    """Return user details."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT name, username, role, gender, age, company, department FROM users
        WHERE username = ?
        """, (username,))
        row = cursor.fetchone()
        if row:
            return {
                "name": row[0],
                "username": row[1],
                "role": row[2],
                "gender": row[3],
                "age": row[4],
                "company": row[5],
                "department": row[6]
            }
        return None
    finally:
        conn.close()

def save_prediction(username, age, gender, company, department, years_company, prior_exp, salary, bonus, heart_rate, predicted_stress, confidence_score, stress_score):
    """Save prediction log to database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO predictions (
            username, age, gender, company, department, 
            years_in_company, prior_experience, salary, annual_bonus, 
            resting_heart_rate, predicted_stress, confidence_score, stress_score, prediction_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            int(age),
            gender,
            company,
            department,
            float(years_company),
            float(prior_exp),
            float(salary),
            float(bonus),
            int(heart_rate),
            predicted_stress,
            float(confidence_score),
            float(stress_score),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return False
    finally:
        conn.close()

def get_predictions(username=None):
    """Retrieve predictions. If username is given, retrieve only for that user."""
    init_db()
    conn = get_connection()
    try:
        if username:
            query = "SELECT * FROM predictions WHERE username = ? ORDER BY prediction_date DESC"
            df = pd.read_sql_query(query, conn, params=(username,))
        else:
            query = "SELECT * FROM predictions ORDER BY prediction_date DESC"
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()

def delete_prediction(pred_id):
    """Delete single prediction by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM predictions WHERE id = ?", (pred_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting prediction: {e}")
        return False
    finally:
        conn.close()

def delete_user_and_predictions(username):
    """Delete a user account and all their predictions."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        cursor.execute("DELETE FROM predictions WHERE username = ?", (username,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        conn.close()

def get_all_users():
    """Return all registered users."""
    init_db()
    conn = get_connection()
    try:
        query = "SELECT name, username, role, gender, age, company, department, created_at FROM users ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()
