"""
Quick Launch Script for HR Analytics Platform
Ensures setup is correct and launches the professional platform
"""

import os
import sys
import subprocess
import platform

def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_header():
    """Print startup header."""
    clear_screen()
    print("=" * 70)
    print("🏢 HR ANALYTICS PLATFORM - Professional Edition")
    print("=" * 70)
    print()

def print_menu():
    """Print main menu."""
    print("What would you like to do?")
    print()
    print("1. 🚀 Launch HR Platform (hr_platform.py)")
    print("2. 🏋️ Train Models (train.py)")
    print("3. ✓ Verify Setup (setup_verify.py)")
    print("4. 📚 Open Documentation")
    print("5. 🚪 Exit")
    print()

def launch_platform():
    """Launch the HR platform."""
    print("\n🚀 Launching HR Analytics Platform...")
    print("Opening at: http://localhost:8501")
    print()
    print("To stop the server, press Ctrl+C")
    print()
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'hr_platform.py'])
    except KeyboardInterrupt:
        print("\n\n✋ Platform stopped by user")
    except Exception as e:
        print(f"❌ Error launching platform: {e}")

def train_models():
    """Train models."""
    print("\n🏋️ Training ML Models...")
    print()
    
    try:
        subprocess.run([sys.executable, 'train.py'])
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"❌ Error training models: {e}")
        input("\nPress Enter to continue...")

def verify_setup():
    """Verify setup."""
    print("\n✓ Verifying Setup...")
    print()
    
    try:
        subprocess.run([sys.executable, 'setup_verify.py'])
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
        input("\nPress Enter to continue...")

def open_documentation():
    """Open documentation."""
    doc_file = "HR_PLATFORM_GUIDE.md"
    
    if os.path.exists(doc_file):
        print(f"\n📚 Opening {doc_file}...")
        
        if platform.system() == 'Windows':
            os.startfile(doc_file)
        elif platform.system() == 'Darwin':
            os.system(f'open {doc_file}')
        else:
            os.system(f'xdg-open {doc_file}')
        
        print("Documentation opened in default editor")
    else:
        print(f"❌ {doc_file} not found")
    
    input("\nPress Enter to continue...")

def main():
    """Main menu loop."""
    while True:
        print_header()
        
        print("Quick Links:")
        print("📂 Platform File: hr_platform.py")
        print("📂 Training File: train.py")
        print("📂 Documentation: HR_PLATFORM_GUIDE.md")
        print()
        print("Login Credentials:")
        print("👤 admin / admin123 (Administrator)")
        print("👥 hr / hr123 (HR Manager)")
        print("👨‍💼 manager / manager123 (Manager)")
        print()
        print("-" * 70)
        
        print_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                launch_platform()
            elif choice == '2':
                train_models()
            elif choice == '3':
                verify_setup()
            elif choice == '4':
                open_documentation()
            elif choice == '5':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()
