import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import config
import os
from datetime import datetime

class ResultPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        self.parent = parent
        self.prediction_results = None
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the results panel UI components."""
        # Main heading
        ttk.Label(self, text="Battery Health Analysis Results", font=(config.UI_FONT, 16, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 20))
        
        # Results summary frame
        self.summary_frame = ttk.LabelFrame(self, text="Health Status", padding="10")
        self.summary_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        # Status indicators
        self.status_label = ttk.Label(self.summary_frame, text="--", font=(config.UI_FONT, 14, "bold"))
        self.status_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        self.recommendation_label = ttk.Label(self.summary_frame, text="--")
        self.recommendation_label.grid(row=1, column=0, sticky="w")
        
        # Metrics frame
        metrics_frame = ttk.LabelFrame(self, text="Prediction Results", padding="10")
        metrics_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        
        # RUL and SOP values
        ttk.Label(metrics_frame, text="Remaining Useful Life (RUL):").grid(row=0, column=0, sticky="w", pady=5)
        self.rul_label = ttk.Label(metrics_frame, text="--", font=(config.UI_FONT, 12, "bold"))
        self.rul_label.grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Label(metrics_frame, text="State of Performance (SOP):").grid(row=1, column=0, sticky="w", pady=5)
        self.sop_label = ttk.Label(metrics_frame, text="--", font=(config.UI_FONT, 12, "bold"))
        self.sop_label.grid(row=1, column=1, sticky="w", pady=5)
        
        # Battery information frame
        info_frame = ttk.LabelFrame(self, text="Battery Information", padding="10")
        info_frame.grid(row=2, column=1, sticky="nsew", pady=(0, 10), padx=10)
        
        # Battery info
        ttk.Label(info_frame, text="Battery ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.battery_id_label = ttk.Label(info_frame, text="--")
        self.battery_id_label.grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Capacity:").grid(row=1, column=0, sticky="w", pady=5)
        self.capacity_label = ttk.Label(info_frame, text="--")
        self.capacity_label.grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(info_frame, text="Temperature:").grid(row=2, column=0, sticky="w", pady=5)
        self.temp_label = ttk.Label(info_frame, text="--")
        self.temp_label.grid(row=2, column=1, sticky="w", pady=5)
        
        # Visualization frame
        self.viz_frame = ttk.LabelFrame(self, text="Visualization", padding="10")
        self.viz_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Placeholder for charts
        self.chart_frame = ttk.Frame(self.viz_frame)
        self.chart_frame.pack(fill="both", expand=True)
        
        # Export button
        export_btn = ttk.Button(self, text="Export Results", command=self.export_results)
        export_btn.grid(row=4, column=0, sticky="w", pady=(10, 0))
        
        # Clear button
        clear_btn = ttk.Button(self, text="Clear Results", command=self.clear_results)
        clear_btn.grid(row=4, column=1, sticky="e", pady=(10, 0))
        
        # Make the grid expandable
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)
        
    def update_results(self, results):
        """Update the results panel with new prediction results."""
        self.prediction_results = results
        
        # Update status
        status, recommendation, color = results['status']
        self.status_label.config(text=status, foreground=color)
        self.recommendation_label.config(text=recommendation)
        
        # Update metrics
        rul_value = results['rul']
        sop_value = results['sop']
        
        self.rul_label.config(text=f"{rul_value:.1f} units")
        self.sop_label.config(text=f"{sop_value:.2f} ({sop_value*100:.1f}%)")
        
        # Update battery info
        input_data = results['input_data']
        self.battery_id_label.config(text=str(input_data['battery_id'].iloc[0]))
        self.capacity_label.config(text=f"{input_data['Capacity'].iloc[0]:.3f} Ah")
        self.temp_label.config(text=f"{input_data['ambient_temperature'].iloc[0]} °C")
        
        # Create visualizations
        self.create_visualizations(results)
        
    def create_visualizations(self, results):
        """Create visualizations based on prediction results."""
        # Clear existing charts
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # Create figure with two subplots
        fig = plt.figure(figsize=(10, 5))
        
        # RUL Gauge chart
        ax1 = fig.add_subplot(121)
        self.create_gauge_chart(ax1, results['rul'], "Remaining Useful Life", config.MAX_EXPECTED_RUL)
        
        # SOP Gauge chart
        ax2 = fig.add_subplot(122)
        self.create_gauge_chart(ax2, results['sop'], "State of Performance", 1.0, is_percentage=True)
        
        # Embed the charts in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def create_gauge_chart(self, ax, value, title, max_value, is_percentage=False):
        """Create a gauge chart for displaying metrics."""
        # Define colors for different regions
        colors = ['#e74c3c', '#f39c12', '#2ecc71']
        # Define thresholds for colors
        if is_percentage:
            thresholds = [0.3, 0.7, 1.0]
            value_norm = value
        else:
            thresholds = [config.RUL_THRESHOLD_CRITICAL, config.RUL_THRESHOLD_WARNING, max_value]
            value_norm = value / max_value if max_value else 0
        # Plot the gauge background using arcs
        start_angles = [0.1 * np.pi, (0.1 + 0.8 * thresholds[0] / max_value) * np.pi if not is_percentage else (0.1 + 0.8 * thresholds[0]) * np.pi,
                        (0.1 + 0.8 * thresholds[1] / max_value) * np.pi if not is_percentage else (0.1 + 0.8 * thresholds[1]) * np.pi,
                        0.9 * np.pi]
        for i in range(3):
            theta = np.linspace(start_angles[i], start_angles[i+1], 50)
            x_arc = np.cos(theta)
            y_arc = np.sin(theta)
            ax.plot(x_arc, y_arc, color=colors[i], linewidth=15, alpha=0.7)
        # Plot the needle
        theta_needle = (0.1 + 0.8 * value_norm) * np.pi
        x_needle = [0, 0.8 * np.cos(theta_needle)]
        y_needle = [0, 0.8 * np.sin(theta_needle)]
        ax.plot(x_needle, y_needle, color='black', linewidth=2)
        # Add a center circle
        circle = plt.Circle((0, 0), 0.05, color='black')
        ax.add_artist(circle)
        # Set the label with value
        if is_percentage:
            label_text = f"{value:.2f} ({value*100:.1f}%)"
        else:
            label_text = f"{value:.1f}"
        ax.text(0, -0.2, label_text, ha='center', va='center', fontsize=12, fontweight='bold')
        # Set title
        ax.text(0, 0.6, title, ha='center', va='center', fontsize=12)
        # Set axes properties
        ax.set_xlim(-1, 1)
        ax.set_ylim(-0.5, 1)
        ax.axis('off')
        
    def export_results(self):
        """Export the results to a CSV file."""
        if not self.prediction_results:
            messagebox.showinfo("Export", "No results to export")
            return
            
        try:
            # Create export directory if it doesn't exist
            export_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            # Create a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"battery_health_prediction_{timestamp}.csv"
            filepath = os.path.join(export_dir, filename)
            
            # Create export dataframe
            input_data = self.prediction_results['input_data']
            
            export_data = {
                'Battery ID': input_data['battery_id'].values,
                'Test ID': input_data['test_id'].values,
                'Capacity': input_data['Capacity'].values,
                'Electrolyte Resistance (Re)': input_data['Re'].values,
                'Charge Transfer Resistance (Rct)': input_data['Rct'].values,
                'Ambient Temperature': input_data['ambient_temperature'].values,
                'Predicted RUL': [self.prediction_results['rul']] * len(input_data),
                'Predicted SOP': [self.prediction_results['sop']] * len(input_data),
                'Health Status': [self.prediction_results['status'][0]] * len(input_data),
                'Recommendation': [self.prediction_results['status'][1]] * len(input_data),
                'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(input_data)
            }
            
            export_df = pd.DataFrame(export_data)
            export_df.to_csv(filepath, index=False)
            
            messagebox.showinfo("Export Successful", f"Results exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")
            
    def clear_results(self):
        """Clear all results."""
        # Reset status
        self.status_label.config(text="--", foreground="black")
        self.recommendation_label.config(text="--")
        
        # Reset metrics
        self.rul_label.config(text="--")
        self.sop_label.config(text="--")
        
        # Reset battery info
        self.battery_id_label.config(text="--")
        self.capacity_label.config(text="--")
        self.temp_label.config(text="--")
        
        # Clear charts
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # Reset prediction results
        self.prediction_results = None
