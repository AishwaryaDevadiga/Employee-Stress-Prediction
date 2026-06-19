"""
Setup Verification Script
Checks if all dependencies and files are properly configured.
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.7 or higher."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK\n")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Required: 3.7+\n")
        return False


def check_packages():
    """Check if required packages are installed."""
    print("🔍 Checking required packages...")
    packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'plotly': 'plotly',
        'joblib': 'joblib',
        'streamlit': 'streamlit'
    }
    
    missing = []
    for import_name, install_name in packages.items():
        try:
            importlib.import_module(import_name)
            print(f"✅ {install_name:20} - installed")
        except ImportError:
            print(f"❌ {install_name:20} - MISSING")
            missing.append(install_name)
    
    print()
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"\nInstall with: pip install {' '.join(missing)}")
        return False
    else:
        print("✅ All packages installed\n")
        return True


def check_directories():
    """Check and create necessary directories."""
    print("🔍 Checking directories...")
    directories = [
        'dataset',
        'models',
        'models/gender_specific',
        'outputs',
        'outputs/plots',
        'outputs/reports',
        'src'
    ]
    
    for d in directories:
        if os.path.exists(d):
            print(f"✅ {d:30} - exists")
        else:
            os.makedirs(d, exist_ok=True)
            print(f"✅ {d:30} - created")
    
    print()
    return True


def check_data_files():
    """Check if dataset exists."""
    print("🔍 Checking data files...")
    
    # Check for dataset
    possible_paths = [
        'dataset/company_employee_details4999.csv',
        'dataset/company_employee_details5000.csv',
        '../dataset/company_employee_details4999.csv',
        '../dataset/company_employee_details5000.csv'
    ]
    
    found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Dataset found: {path}")
            found = True
            break
    
    if not found:
        print(f"❌ Dataset NOT found in expected locations:")
        for path in possible_paths:
            print(f"   - {path}")
        print(f"\nPlease ensure the dataset CSV file exists in the 'dataset/' folder")
        return False
    
    print()
    return True


def check_python_files():
    """Check if all required Python modules exist."""
    print("🔍 Checking Python modules...")
    
    src_files = [
        'src/data_loader.py',
        'src/data_loader_class.py',
        'src/preprocessing.py',
        'src/data_preprocessor_class.py',
        'src/feature_engineering.py',
        'src/feature_engineer_class.py',
        'src/model_trainer.py',
        'src/gender_specific_models.py',
        'src/prediction.py',
        'src/evaluation.py',
        'src/personalized_models.py'
    ]
    
    root_files = [
        'train.py',
        'dashboard.py',
        'requirements_streamlit.txt'
    ]
    
    missing_src = []
    for f in src_files:
        if os.path.exists(f):
            print(f"✅ {f:40} - exists")
        else:
            print(f"❌ {f:40} - MISSING")
            missing_src.append(f)
    
    print()
    
    missing_root = []
    for f in root_files:
        if os.path.exists(f):
            print(f"✅ {f:40} - exists")
        else:
            print(f"❌ {f:40} - MISSING")
            missing_root.append(f)
    
    print()
    
    if missing_src or missing_root:
        return False
    return True


def main():
    """Run all checks."""
    print("\n" + "="*70)
    print("EMPLOYEE STRESS PREDICTION SYSTEM - SETUP VERIFICATION")
    print("="*70 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_packages),
        ("Directories", check_directories),
        ("Data Files", check_data_files),
        ("Python Modules", check_python_files)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error checking {name}: {e}\n")
            results.append((name, False))
    
    # Summary
    print("="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("="*70)
    
    if all_passed:
        print("\n✅ ALL CHECKS PASSED!\n")
        print("Next steps:")
        print("1. Train models:  python train.py")
        print("2. Launch dashboard: streamlit run dashboard.py\n")
        return 0
    else:
        print("\n❌ SOME CHECKS FAILED\n")
        print("Please fix the issues above and try again.\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
