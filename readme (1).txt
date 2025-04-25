# Battery Health Prediction System

A professional application for predicting battery health, including Remaining Useful Life (RUL) and State of Performance (SOP).

## Features

- **Battery Health Analysis**: Predicts Remaining Useful Life (RUL) and State of Performance (SOP)
- **Interactive Dashboard**: User-friendly interface with visual indicators
- **Data Input Options**: Manual data entry or CSV file upload
- **Detailed Visualizations**: Gauge charts for key metrics
- **Export Functionality**: Save predictions to CSV for further analysis
- **Health Recommendations**: Get actionable insights based on battery condition

## Installation

### Option 1: Run the executable (Windows)

1. Download the latest release
2. Extract the zip file
3. Run "Battery Health Predictor.exe"

### Option 2: Install from source

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```

## Usage

1. **Input Data**: Enter battery parameters manually or upload a CSV file
2. **Run Prediction**: Click "Run Prediction" to analyze the battery health
3. **View Results**: Check the prediction results, visualizations, and recommendations
4. **Export Results**: Save the results for documentation or further analysis

## Data Format

For CSV uploads, the file must include the following columns:
- `type`: Operation type (-1, 0, 1)
- `ambient_temperature`: Temperature in degrees Celsius
- `battery_id`: Unique identifier for the battery
- `test_id`: Test identifier
- `Capacity`: Battery capacity in Ah
- `Re`: Electrolyte resistance in Ohm
- `Rct`: Charge transfer resistance in Ohm

## Building the Executable

To build the standalone executable:

```
python build.py
```

The executable will be created in the `dist` folder.

## Requirements

- Python 3.8+
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- XGBoost
- Tkinter (included with most Python installations)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
