import subprocess
import sys

def install_packages():
    packages = ["Pillow", "keyboard", "threaded", "pynput"]
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Ensure Python is added to PATH.")
            print(e)
            return False
    return True

if __name__ == "__main__":
    print("Starting package installation...")
    success = install_packages()
    if success:
        print("All packages installed successfully.")
    else:
        print("Some packages failed to install.")
    input("Press Enter to exit...")
