import os
import sys
import tkinter as tk
from tkinter import messagebox
import traceback

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import application modules
import config
from ui.dashboard import Dashboard
from models.battery_model import train_and_save_model

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import pandas
        import numpy
        import matplotlib.pyplot
        import tkinter
        from tkinter import ttk
        from sklearn.ensemble import RandomForestRegressor
        return True
    except ImportError as e:
        print(f"Missing dependency: {str(e)}")
        return False

def check_data():
    """Check if the data file exists."""
    if not os.path.exists(config.DATA_FILE):
        print(f"Warning: Data file not found at {config.DATA_FILE}")
        return False
    return True

def check_model():
    """Check if the model file exists."""
    if not os.path.exists(config.MODEL_FILE):
        print(f"Warning: Model file not found at {config.MODEL_FILE}")
        return False
    return True

def setup_environment():
    """Setup the application environment."""
    # Create necessary directories
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports"), exist_ok=True)
    
    # If data or model files don't exist, show warnings
    data_exists = check_data()
    model_exists = check_model()
    
    if not data_exists:
        print("Please place the Battery_Data_Cleaned.csv file in the data directory before running the application.")
    
    if not model_exists and data_exists:
        print("Training a new model as no existing model was found...")
        try:
            train_and_save_model()
            print("Model trained and saved successfully.")
        except Exception as e:
            print(f"Error training model: {str(e)}")
            traceback.print_exc()

def main():
    """Main application entry point."""
    # Check dependencies
    if not check_dependencies():
        print("Error: Missing dependencies. Please install required packages.")
        return
    
    # Setup environment
    setup_environment()
    
    # Start the application
    try:
        app = Dashboard()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        traceback.print_exc()
        
        # If running in tkinter environment, show error dialog
        try:
            messagebox.showerror(
                "Application Error", 
                f"An error occurred while starting the application: {str(e)}\n\nPlease check the console for details."
            )
        except:
            pass
        sys.exit(1)  # Ensure the process exits after error

if __name__ == "__main__":
    main()
