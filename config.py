import os
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent

# Data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "Battery_Data_Cleaned.csv")

# Model paths
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_FILE = os.path.join(MODEL_DIR, "trained_model.pkl")

# Application settings
APP_TITLE = "Battery Health Prediction System"
APP_VERSION = "1.0.0"
APP_ICON = os.path.join(BASE_DIR, "ui", "assets", "battery_icon.ico")

# UI settings
UI_THEME = "dark"  # or "light"
UI_PRIMARY_COLOR = "#3498db"  # blue
UI_SECONDARY_COLOR = "#2ecc71"  # green
UI_DANGER_COLOR = "#e74c3c"  # red
UI_WARNING_COLOR = "#f39c12"  # yellow
UI_FONT = "Segoe UI"

# RUL calculation parameters
MAX_EXPECTED_RUL = 1000  # maximum expected remaining useful life
RUL_THRESHOLD_CRITICAL = 150  # critical RUL threshold
RUL_THRESHOLD_WARNING = 400  # warning RUL threshold
SOP_MIN_THRESHOLD = 0.7  # minimum state of performance threshold

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "ui", "assets"), exist_ok=True)
