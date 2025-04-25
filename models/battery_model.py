import numpy as np
import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import config
from utils.data_processing import load_data, preprocess_data, prepare_features, scale_features, save_scaler

class BatteryHealthModel:
    def __init__(self):
        self.rul_model = None
        self.sop_model = None
        self.scaler = None
        
    def train(self, data=None, test_size=0.2, random_state=42):
        """Train the battery health prediction models."""
        try:
            # Load data if not provided
            if data is None:
                data = load_data()
                
            if data is None or data.empty:
                raise ValueError("No data available for training")
                
            # Preprocess data
            processed_data = preprocess_data(data)
            
            # Prepare features and targets
            X, y_rul, y_sop = prepare_features(processed_data)
            
            # Split data
            X_train, X_test, y_rul_train, y_rul_test, y_sop_train, y_sop_test = train_test_split(
                X, y_rul, y_sop, test_size=test_size, random_state=random_state
            )
            
            # Scale features
            X_train_scaled, X_test_scaled, self.scaler = scale_features(X_train, X_test)
            
            # Handle NaN values in training data
            train_df = pd.DataFrame(X_train_scaled)
            train_df['target'] = y_rul_train
            train_df = train_df.dropna()
            X_train_scaled = train_df.drop('target', axis=1).values
            y_rul_train = train_df['target'].values
            
            # Before fitting, drop rows with NaNs in X_train_scaled, y_rul_train, or y_sop_train
            train_df = pd.DataFrame(X_train_scaled)
            train_df['y_rul'] = y_rul_train
            train_df['y_sop'] = y_sop_train
            train_df = train_df.dropna()
            X_train_scaled = train_df.drop(['y_rul', 'y_sop'], axis=1).values
            y_rul_train = train_df['y_rul'].values
            y_sop_train = train_df['y_sop'].values

            # Remove rows with NaN in X_test_scaled, y_rul_test, or y_sop_test
            test_df = pd.DataFrame(X_test_scaled)
            test_df['y_rul'] = y_rul_test
            test_df['y_sop'] = y_sop_test
            test_df = test_df.dropna()
            X_test_scaled = test_df.drop(['y_rul', 'y_sop'], axis=1).values
            y_rul_test = test_df['y_rul'].values
            y_sop_test = test_df['y_sop'].values
            
            # Train RUL model - Random Forest performed best in the analysis
            print("Training RUL prediction model...")
            self.rul_model = RandomForestRegressor(
                n_estimators=100, 
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state
            )
            self.rul_model.fit(X_train_scaled, y_rul_train)
            
            # Train SOP model
            print("Training SOP prediction model...")
            self.sop_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state
            )
            self.sop_model.fit(X_train_scaled, y_sop_train)
            
            # Evaluate models
            rul_pred = self.rul_model.predict(X_test_scaled)
            sop_pred = self.sop_model.predict(X_test_scaled)
            
            # RUL metrics
            rul_mse = mean_squared_error(y_rul_test, rul_pred)
            rul_mae = mean_absolute_error(y_rul_test, rul_pred)
            rul_r2 = r2_score(y_rul_test, rul_pred)
            
            # SOP metrics
            sop_mse = mean_squared_error(y_sop_test, sop_pred)
            sop_mae = mean_absolute_error(y_sop_test, sop_pred)
            sop_r2 = r2_score(y_sop_test, sop_pred)
            
            print("RUL Model Evaluation:")
            print(f"MSE: {rul_mse:.6f}")
            print(f"MAE: {rul_mae:.6f}")
            print(f"R2: {rul_r2:.6f}")
            
            print("\nSOP Model Evaluation:")
            print(f"MSE: {sop_mse:.6f}")
            print(f"MAE: {sop_mae:.6f}")
            print(f"R2: {sop_r2:.6f}")
            
            # Save the scaler
            save_scaler(self.scaler)
            
            return {
                'rul_metrics': {'mse': rul_mse, 'mae': rul_mae, 'r2': rul_r2},
                'sop_metrics': {'mse': sop_mse, 'mae': sop_mae, 'r2': sop_r2}
            }
            
        except Exception as e:
            print(f"Error training model: {e}")
            raise
    
    def predict(self, X_scaled):
        """Make predictions using trained models."""
        if self.rul_model is None or self.sop_model is None:
            raise ValueError("Models not trained. Call train() first or load existing models.")
            
        rul_pred = self.rul_model.predict(X_scaled)
        sop_pred = self.sop_model.predict(X_scaled)
        
        return rul_pred, sop_pred
    
    def get_health_status(self, rul, sop):
        """Get battery health status based on RUL and SOP."""
        if rul <= config.RUL_THRESHOLD_CRITICAL or sop < config.SOP_MIN_THRESHOLD:
            return ("Critical", "Immediate replacement recommended", config.UI_DANGER_COLOR)
        elif rul <= config.RUL_THRESHOLD_WARNING:
            return ("Warning", "Monitor closely and plan for replacement", config.UI_WARNING_COLOR)
        else:
            return ("Good", "Battery is in good condition", config.UI_SECONDARY_COLOR)
    
    def save_models(self, file_path=config.MODEL_FILE):
        """Save trained models to file."""
        if self.rul_model is None or self.sop_model is None:
            raise ValueError("No trained models to save")
            
        models = {
            'rul_model': self.rul_model,
            'sop_model': self.sop_model
        }
        
        with open(file_path, 'wb') as f:
            pickle.dump(models, f)
        
        print(f"Models saved to {file_path}")
    
    def load_models(self, file_path=config.MODEL_FILE):
        """Load trained models from file."""
        try:
            with open(file_path, 'rb') as f:
                models = pickle.load(f)
                
            self.rul_model = models['rul_model']
            self.sop_model = models['sop_model']
            
            print(f"Models loaded from {file_path}")
        except Exception as e:
            print(f"Error loading models: {e}")
            raise
    
    def plot_feature_importance(self, save_path=None):
        """Plot feature importance from the trained models."""
        if self.rul_model is None or self.sop_model is None:
            raise ValueError("Models not trained. Call train() first or load existing models.")
            
        # Get feature names
        features = ['type', 'ambient_temperature', 'battery_id', 'test_id', 'Capacity', 'Re', 'Rct']
        
        # Get feature importances
        rul_importances = self.rul_model.feature_importances_
        sop_importances = self.sop_model.feature_importances_
        
        # Create DataFrame for plotting
        importance_df = pd.DataFrame({
            'Feature': features,
            'RUL Importance': rul_importances,
            'SOP Importance': sop_importances
        })
        
        # Sort by RUL importance
        importance_df = importance_df.sort_values('RUL Importance', ascending=False)
        
        # Create plot
        plt.figure(figsize=(10, 6))
        
        # Plot RUL importance
        plt.subplot(1, 2, 1)
        sns.barplot(x='RUL Importance', y='Feature', data=importance_df, color=config.UI_PRIMARY_COLOR)
        plt.title('RUL Feature Importance')
        plt.tight_layout()
        
        # Plot SOP importance
        plt.subplot(1, 2, 2)
        sns.barplot(x='SOP Importance', y='Feature', data=importance_df, color=config.UI_SECONDARY_COLOR)
        plt.title('SOP Feature Importance')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            
        return plt.gcf()

def train_and_save_model():
    """Utility function to train and save model."""
    model = BatteryHealthModel()
    model.train()
    model.save_models()
    return model

if __name__ == "__main__":
    # Execute if script is run directly
    train_and_save_model()
