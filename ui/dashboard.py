import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
from ui.input_panel import InputPanel
from ui.result_panel import ResultPanel
from models.battery_model import BatteryHealthModel
from utils.data_processing import preprocess_data, prepare_new_data

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title(config.APP_TITLE)
        self.geometry("1200x800")
        self.minsize(900, 600)
        self.configure(bg="#e6f2ff")  # Light blue background
        
        # Set icon if available
        if os.path.exists(config.APP_ICON):
            self.iconbitmap(config.APP_ICON)
            
        # Configure styles
        self.configure_styles()
        
        # Initialize model
        self.model = BatteryHealthModel()
        self.load_model()
            
        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create header
        self.create_header(main_frame)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=10)
        
        # Create tabs
        self.input_panel = InputPanel(notebook, self.process_data)
        self.result_panel = ResultPanel(notebook)
        
        notebook.add(self.input_panel, text="Input Data")
        notebook.add(self.result_panel, text="Results")
        
        # Create footer
        self.create_footer(main_frame)
        
        # Add this line to create the status_label if it doesn't exist
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()
        
    def configure_styles(self):
        """Configure custom styles for the application."""
        style = ttk.Style()
        
        # Check if the theme is available, else use default theme
        try:
            style.theme_use(config.UI_THEME)
        except tk.TclError:
            available_themes = style.theme_names()
            if "clam" in available_themes:
                style.theme_use("clam")
                
        # Configure colors and fonts
        style.configure("TLabel", font=(config.UI_FONT, 10))
        style.configure("TButton", font=(config.UI_FONT, 10))
        style.configure("TEntry", font=(config.UI_FONT, 10))
        style.configure("TNotebook", background="#f0f0f0", tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab", padding=[10, 5], font=(config.UI_FONT, 10))
        
        # Configure frame padding
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", font=(config.UI_FONT, 11, "bold"))
        
    def create_header(self, parent):
        """Create header section with title and logo."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title label
        title_label = ttk.Label(
            header_frame, 
            text=config.APP_TITLE, 
            font=(config.UI_FONT, 20, "bold")
        )
        title_label.pack(side="left", padx=5)
        
        # Version label
        version_label = ttk.Label(
            header_frame, 
            text=f"v{config.APP_VERSION}", 
            font=(config.UI_FONT, 10)
        )
        version_label.pack(side="left", padx=5, pady=8)
        
        # About button
        about_button = ttk.Button(header_frame, text="About", command=self.show_about)
        about_button.pack(side="right", padx=5)
        
    def create_footer(self, parent):
        """Create footer section with status bar."""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill="x", pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(
            footer_frame, 
            text="Ready", 
            font=(config.UI_FONT, 9)
        )
        self.status_label.pack(side="left", padx=5)
        
        # Model info label
        if hasattr(self, 'model') and self.model is not None:
            model_label = ttk.Label(
                footer_frame, 
                text="Model: Random Forest", 
                font=(config.UI_FONT, 9)
            )
            model_label.pack(side="right", padx=5)
        
    def load_model(self):
        """Load the pre-trained model."""
        try:
            self.model.load_models()
            self.update_status("Model loaded successfully")
        except Exception as e:
            messagebox.showwarning(
                "Model Loading Error", 
                f"Failed to load model: {str(e)}\n\nA new model will be trained."
            )
            
            # Try to train a new model
            try:
                self.update_status("Training new model...")
                
                # Check if data file exists
                if not os.path.exists(config.DATA_FILE):
                    raise FileNotFoundError(f"Data file not found: {config.DATA_FILE}")
                    
                # Load and preprocess data
                data = pd.read_csv(config.DATA_FILE)
                
                # Train model
                self.model.train(data)
                self.model.save_models()
                
                self.update_status("New model trained and saved successfully")
                
            except Exception as train_error:
                messagebox.showerror(
                    "Training Error", 
                    f"Failed to train new model: {str(train_error)}\n\nThe application may not work properly."
                )
                self.update_status("Error: Model not available")
                
    def process_data(self, data):
        """Process input data and run prediction."""
        try:
            self.update_status("Processing data...")
            # Prepare data for prediction (preprocessing is done inside prepare_new_data)
            X_scaled, processed_data = prepare_new_data(data)
            # Run prediction
            rul_pred, sop_pred = self.model.predict(X_scaled)
            # Get the mean prediction if multiple rows
            rul_mean = np.mean(rul_pred)
            sop_mean = np.mean(sop_pred)
            # Get health status
            status = self.model.get_health_status(rul_mean, sop_mean)
            # Prepare results dictionary
            results = {
                'input_data': data,
                'processed_data': processed_data,
                'rul': rul_mean,
                'sop': sop_mean,
                'status': status
            }
            # Update results panel
            self.result_panel.update_results(results)
            self.update_status("Prediction complete")
            self.show_results(results)
        except Exception as e:
            messagebox.showerror("Prediction Error", f"Failed to process data: {str(e)}")
            self.update_status("Error during prediction")
            
    def update_status(self, message):
        """Update the status bar message."""
        if hasattr(self, "status_label"):
            self.status_label.config(text=message)
        self.update()  # Update the UI
        
    def show_about(self):
        """Show about dialog."""
        about_text = f"""
        {config.APP_TITLE} v{config.APP_VERSION}
        
        A professional application for battery health prediction.
        
        This system predicts:
        - Remaining Useful Life (RUL)
        - State of Performance (SOP)
        
        Based on battery characteristics such as:
        - Capacity
        - Internal resistances
        - Operating conditions
        
        © 2025 Battery Diagnostics
        """
        
        messagebox.showinfo("About", about_text)
        
    def show_results(self, results):
        """Show results in the results panel and update the graph."""
        # Hide input frame and show results frame
        self.input_panel.pack_forget()
        self.result_panel.pack(fill="both", expand=True, padx=30, pady=20)

        # Update results widgets
        self.result_panel.update_results(results)

        # Update graph
        self.ax.clear()
        self.ax.plot(results['processed_data']['cycle'], results['processed_data']['health'], color="#007acc", marker='o', label="Battery Health")
        self.ax.set_title("Battery Health Over Time", fontsize=14, color="#003366")
        self.ax.set_xlabel("Cycle", fontsize=12)
        self.ax.set_ylabel("Health (%)", fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()

        # Add explanatory text
        self.graph_text.config(
            text="The graph above shows the predicted battery health over cycles. "
                 "A downward trend may indicate battery degradation. "
                 "Interpret the results in the context of your battery's usage."
        )

    def on_reset(self):
        """Clear all input fields and reset UI."""
        self.input_panel.clear_fields()
        self.status_label.config(text="")
        self.result_panel.pack_forget()
        self.input_panel.pack(pady=10)
