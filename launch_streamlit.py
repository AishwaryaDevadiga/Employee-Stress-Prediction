"""
Quick Launcher for Employee Stress Prediction System (Streamlit)

This script makes it easy to launch the Streamlit application.

Usage:
    python launch_streamlit.py
    
Or from terminal:
    streamlit run app.py
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit application."""
    
    print("\n" + "="*60)
    print("🏢 EMPLOYEE STRESS PREDICTION SYSTEM")
    print("="*60)
    print("🚀 Launching Streamlit Application...\n")
    
    # Get project root
    project_root = Path(__file__).parent
    app_file = project_root / "app.py"
    
    # Check if app.py exists
    if not app_file.exists():
        print("❌ ERROR: app.py not found!")
        print(f"Looking for: {app_file}")
        sys.exit(1)
    
    print(f"📂 Project Root: {project_root}")
    print(f"📄 App File: {app_file}\n")
    
    # Check if train.py has been run (models exist)
    model_path = project_root / "models" / "best_general_model.pkl"
    if not model_path.exists():
        print("⚠️  WARNING: Trained model not found!")
        print(f"   Path: {model_path}")
        print("\n   Would you like to train the model first? (y/n): ", end="")
        
        response = input().strip().lower()
        if response == 'y':
            print("\n🔄 Running model training...")
            train_file = project_root / "train.py"
            if train_file.exists():
                subprocess.run([sys.executable, str(train_file)])
                print("\n✅ Training complete!\n")
            else:
                print("❌ train.py not found!")
                sys.exit(1)
        else:
            print("⏭️  Proceeding without training...\n")
    
    # Launch Streamlit
    print("📊 Opening Streamlit App at: http://localhost:8501\n")
    print("🔐 Demo Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n   OR")
    print("\n   Username: hr")
    print("   Password: hr123")
    print("\n" + "="*60)
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Run Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(app_file),
            "--logger.level=info"
        ])
    except KeyboardInterrupt:
        print("\n\n✋ Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error launching app: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Streamlit is installed: pip install streamlit")
        print("2. Make sure you're in the project directory")
        print("3. Run: streamlit run app.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
