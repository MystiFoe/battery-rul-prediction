import os
import sys
import shutil
import subprocess

def create_executable():
    """Create an executable file using PyInstaller."""
    # Command to build the executable
    cmd = [
        "pyinstaller",
        "--name=Battery Health Predictor",
        "--icon=ui/assets/battery_icon.ico",
        "--windowed",
        "--add-data=ui/assets;ui/assets",
        "--add-data=models/trained_model.pkl;models",
        "--add-data=models/scaler.pkl;models",
        "app.py"
    ]
    print("Building executable...")
    try:
        subprocess.run(" ".join(cmd), shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error during build process:", e)
        sys.exit(1)
    # Copy data file to the dist directory
    data_src = os.path.join("data", "Battery_Data_Cleaned.csv")
    data_dst_dir = os.path.join("dist", "Battery Health Predictor", "data")
    if os.path.exists(data_src):
        print("Copying data file...")
        os.makedirs(data_dst_dir, exist_ok=True)
        shutil.copy2(data_src, data_dst_dir)
    print("Build completed! Executable is in the 'dist' folder.")

if __name__ == "__main__":
    create_executable()
