import sys
import pkg_resources
import subprocess
import os

def check_python_version():
    print(f"Python version: {sys.version}")
    if sys.version_info >= (3, 8):
        print("✓ Python version OK")
    else:
        print("✗ Python 3.8+ required")

def check_pip():
    try:
        import pip
        print(f"✓ pip installed (version {pip.__version__})")
    except ImportError:
        print("✗ pip not installed")

def check_venv():
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print("✓ Running in virtual environment")
    else:
        print("✗ Not running in virtual environment")

def check_dependencies():
    required = [
        'flask',
        'flask-cors',
        'tensorflow',
        'opencv-python',
        'numpy',
        'python-dotenv',
        'pymongo',
        'pydicom',
        'pillow',
        'pytest'
    ]
    
    print("\nChecking required packages:")
    for package in required:
        try:
            dist = pkg_resources.get_distribution(package)
            print(f"✓ {package} ({dist.version})")
        except pkg_resources.DistributionNotFound:
            print(f"✗ {package} not found")

def check_directories():
    required_dirs = [
        'data/uploads',
        'model/weights',
    ]
    
    print("\nChecking required directories:")
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path} exists")
        else:
            print(f"✗ {dir_path} missing")
            try:
                os.makedirs(dir_path)
                print(f"  → Created {dir_path}")
            except Exception as e:
                print(f"  → Failed to create {dir_path}: {str(e)}")

def main():
    print("Environment Validation\n" + "="*21 + "\n")
    check_python_version()
    check_pip()
    check_venv()
    check_dependencies()
    check_directories()

if __name__ == "__main__":
    main()