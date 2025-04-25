import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import os
import config

class InputPanel(ttk.Frame):
    def __init__(self, parent, callback):
        super().__init__(parent, padding="10")
        self.parent = parent
        self.callback = callback
        self.file_path = None
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the input panel UI components."""
        # Main heading
        ttk.Label(self, text="Battery Data Input", font=(config.UI_FONT, 16, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Input method frame
        input_frame = ttk.LabelFrame(self, text="Input Method", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Input method selection
        self.input_method = tk.StringVar(value="manual")
        ttk.Radiobutton(input_frame, text="Manual Input", variable=self.input_method, value="manual", command=self.toggle_input_method).grid(row=0, column=0, sticky="w", padx=(0, 20))
        ttk.Radiobutton(input_frame, text="File Upload", variable=self.input_method, value="file", command=self.toggle_input_method).grid(row=0, column=1, sticky="w")
        
        # Manual input frame
        self.manual_frame = ttk.Frame(self, padding="10")
        self.manual_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # File upload frame
        self.file_frame = ttk.Frame(self, padding="10")
        self.file_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.file_frame.grid_remove()  # Initially hidden
        
        # Set up manual input fields
        self.setup_manual_input()
        
        # Set up file upload
        self.setup_file_upload()
        
        # Buttons frame
        button_frame = ttk.Frame(self, padding="10")
        button_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        # Reset button
        ttk.Button(button_frame, text="Reset", command=self.reset_form).grid(row=0, column=0, padx=(0, 10))
        
        # Submit button
        self.submit_btn = ttk.Button(button_frame, text="Run Prediction", command=self.submit)
        self.submit_btn.grid(row=0, column=1)
        
        # Make the grid expandable
        self.columnconfigure(0, weight=1)
        
    def setup_manual_input(self):
        """Set up manual input fields."""
        # Define input fields
        fields = [
            {"name": "type", "label": "Operation Type (-1, 0, 1)", "default": "0", "row": 0},
            {"name": "ambient_temperature", "label": "Ambient Temperature (°C)", "default": "24", "row": 1},
            {"name": "battery_id", "label": "Battery ID", "default": "1", "row": 2},
            {"name": "test_id", "label": "Test ID", "default": "1", "row": 3},
            {"name": "Capacity", "label": "Battery Capacity (Ah)", "default": "0.9", "row": 4},
            {"name": "Re", "label": "Electrolyte Resistance (Ohm)", "default": "0.05", "row": 5},
            {"name": "Rct", "label": "Charge Transfer Resistance (Ohm)", "default": "0.15", "row": 6}
        ]
        
        self.input_vars = {}
        
        # Create input fields
        for field in fields:
            ttk.Label(self.manual_frame, text=field["label"]).grid(row=field["row"], column=0, sticky="w", pady=5)
            self.input_vars[field["name"]] = tk.StringVar(value=field["default"])
            entry = ttk.Entry(self.manual_frame, textvariable=self.input_vars[field["name"]], width=20)
            entry.grid(row=field["row"], column=1, sticky="ew", pady=5)
            
            # Add input validation for numeric fields
            entry.bind("<FocusOut>", lambda e, name=field["name"]: self.validate_numeric(name))
        
    def setup_file_upload(self):
        """Set up file upload components."""
        ttk.Label(self.file_frame, text="Upload CSV File:").grid(row=0, column=0, sticky="w", pady=5)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(self.file_frame, textvariable=self.file_path_var, width=40)
        file_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(0, 10))
        
        browse_btn = ttk.Button(self.file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=2, pady=5)
        
        # Preview label
        ttk.Label(self.file_frame, text="File Preview:").grid(row=1, column=0, sticky="nw", pady=5)
        
        # Preview text area
        self.preview_text = tk.Text(self.file_frame, height=10, width=50)
        self.preview_text.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5)
        self.preview_text.config(state="disabled")
        
    def toggle_input_method(self):
        """Toggle between manual input and file upload."""
        if self.input_method.get() == "manual":
            self.file_frame.grid_remove()
            self.manual_frame.grid()
        else:
            self.manual_frame.grid_remove()
            self.file_frame.grid()
            
    def browse_file(self):
        """Open file browser to select CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.file_path = file_path
            self.file_path_var.set(file_path)
            self.load_file_preview()
            
    def load_file_preview(self):
        """Load and display preview of the selected file."""
        try:
            df = pd.read_csv(self.file_path)
            
            # Validate columns
            required_cols = ['type', 'ambient_temperature', 'battery_id', 'test_id', 'Capacity', 'Re', 'Rct']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                messagebox.showerror("Error", f"Missing required columns: {', '.join(missing_cols)}")
                self.file_path = None
                self.file_path_var.set("")
                return
                
            # Show preview of the data
            preview = df.head(5).to_string()
            self.preview_text.config(state="normal")
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, preview)
            self.preview_text.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            self.file_path = None
            self.file_path_var.set("")
            
    def validate_numeric(self, field_name):
        """Validate that the input is numeric."""
        try:
            value = self.input_vars[field_name].get()
            if value:
                float(value)  # Try to convert to float
        except ValueError:
            messagebox.showerror("Input Error", f"'{field_name}' must be a numeric value")
            self.input_vars[field_name].set("")  # Clear the invalid input
            
    def get_manual_input_data(self):
        """Get data from manual input fields."""
        data = {}
        
        for field, var in self.input_vars.items():
            try:
                value = var.get()
                # Convert type and IDs to integers
                if field in ['type', 'battery_id', 'test_id']:
                    data[field] = int(value)
                # Convert temperatures to integers
                elif field == 'ambient_temperature':
                    data[field] = int(float(value))
                # Convert other fields to floats
                else:
                    data[field] = float(value)
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid value for {field}")
                return None
                
        # Create a DataFrame with the input data
        df = pd.DataFrame([data])
        return df
        
    def reset_form(self):
        """Reset all form fields."""
        # Reset manual input fields to their default values
        default_values = {
            "type": "0",
            "ambient_temperature": "24",
            "battery_id": "1",
            "test_id": "1",
            "Capacity": "0.9",
            "Re": "0.05",
            "Rct": "0.15"
        }
        for field, var in self.input_vars.items():
            var.set(default_values.get(field, ""))
        # Reset file upload fields
        self.file_path = None
        self.file_path_var.set("")
        self.preview_text.config(state="normal")
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.config(state="disabled")
        
    def submit(self):
        """Submit the form data for prediction."""
        try:
            data = None
            
            if self.input_method.get() == "manual":
                data = self.get_manual_input_data()
            else:
                if self.file_path:
                    data = pd.read_csv(self.file_path)
                else:
                    messagebox.showerror("Error", "No file selected")
                    return
                    
            if data is not None:
                self.callback(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process data: {str(e)}")
