import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
import pickle
import config

def load_data(file_path=config.DATA_FILE):
    """Load battery data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def preprocess_data(df):
    """Preprocess the battery data for model training or prediction."""
    processed_df = df.copy()
    # Ensure no division by zero in Capacity
    processed_df['Capacity'] = processed_df['Capacity'].replace(0, np.nan)
    # Calculate improved degradation feature
    processed_df['degradation_feature'] = processed_df['Re'] * processed_df['Rct'] * (1 / (processed_df['Capacity'].fillna(0.01) + 0.01))
    # Calculate RUL with a more realistic formula based on degradation
    processed_df['RUL'] = config.MAX_EXPECTED_RUL / (1 + 2 * processed_df['degradation_feature'])
    # Calculate State of Performance (SOP) - normalized between 0 and 1
    processed_df['SOP'] = processed_df['Capacity'] * (1 - 0.2 * (processed_df['Re'] / processed_df['Re'].max()))
    # Normalize SOP to be between 0 and 1, avoid division by zero
    min_sop = processed_df['SOP'].min()
    max_sop = processed_df['SOP'].max()
    if max_sop - min_sop != 0:
        processed_df['SOP'] = (processed_df['SOP'] - min_sop) / (max_sop - min_sop)
    else:
        processed_df['SOP'] = 0.0
    return processed_df

def prepare_features(df, for_training=True):
    """Prepare features for model training or prediction."""
    feature_cols = ['type', 'ambient_temperature', 'battery_id', 'test_id', 'Capacity', 'Re', 'Rct']
    # Ensure all required columns are present
    for col in feature_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in input data")
    if for_training:
        X = df[feature_cols]
        y_rul = df['RUL']
        y_sop = df['SOP']
        return X, y_rul, y_sop
    else:
        return df[feature_cols]

def scale_features(X_train, X_test=None):
    """Scale features using StandardScaler."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled, scaler
    return X_train_scaled, scaler

def save_scaler(scaler, file_path=None):
    """Save the scaler to a file."""
    if file_path is None:
        file_path = os.path.join(config.MODEL_DIR, "scaler.pkl")
    with open(file_path, 'wb') as f:
        pickle.dump(scaler, f)

def load_scaler(file_path=None):
    """Load the scaler from a file."""
    if file_path is None:
        file_path = os.path.join(config.MODEL_DIR, "scaler.pkl")
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def prepare_new_data(new_data):
    """Process new data for prediction."""
    required_cols = ['type', 'ambient_temperature', 'battery_id', 'test_id', 'Capacity', 'Re', 'Rct']
    for col in required_cols:
        if col not in new_data.columns:
            raise ValueError(f"Missing required column: {col}")
    processed_data = preprocess_data(new_data)
    X = prepare_features(processed_data, for_training=False)
    scaler = load_scaler()
    X_scaled = scaler.transform(X)
    return X_scaled, processed_data
