# **Battery Health Prediction System**

A professional application for predicting battery health, including Remaining Useful Life (RUL) and State of Performance (SOP), with a modern Tkinter UI and export/visualization features.

---

## **Features**

- **Battery Health Analysis**: Predicts Remaining Useful Life (RUL) and State of Performance (SOP)
- **Interactive Dashboard**: User-friendly, colorful interface with visual indicators and navigation
- **Data Input Options**: Manual data entry or CSV file upload
- **Detailed Visualizations**: Clear, labeled graphs with explanatory text
- **Export Functionality**: Save predictions to CSV for further analysis
- **Health Recommendations**: Get actionable insights based on battery condition
- **Error Handling**: Handles missing data and errors gracefully

---

## **Installation**

### Option 1: Run the executable (Windows)

1. Download the latest release
2. Extract the zip file
3. Run "Battery Health Predictor.exe"

### Option 2: Install from source

1. Clone this repository:
   ```bash
   git clone https://github.com/MystiFoe/battery-rul-prediction.git
   cd battery-rul-prediction
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your `Battery_Data_Cleaned.csv` file in the `data` directory.
4. Run the application:
   ```bash
   python app.py
   ```

---

## **Usage**

1. **Input Data**: Enter battery parameters manually or upload a CSV file.
2. **Run Prediction**: Click "Predict" to analyze the battery health.
3. **View Results**: The app auto-navigates to the results page with graphs and explanations.
4. **Export Results**: Save the results for documentation or further analysis.
5. **Reset**: Use the Reset button to clear inputs and start over.

---

## **Data Format**

For CSV uploads, the file must include the following columns:
- `type`: Operation type (-1, 0, 1)
- `ambient_temperature`: Temperature in degrees Celsius
- `battery_id`: Unique identifier for the battery
- `test_id`: Test identifier
- `Capacity`: Battery capacity in Ah
- `Re`: Electrolyte resistance in Ohm
- `Rct`: Charge transfer resistance in Ohm

---

## **Model Evaluation**

The models are evaluated using:
- **Mean Squared Error (MSE)**
- **Mean Absolute Error (MAE)**
- **R-squared (R²)**

---

## **Requirements**

- Python 3.8+
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- XGBoost
- Tkinter (included with most Python installations)

---

## **How to Push Your Files to GitHub**

1. **Check your branch:**
   ```
   git branch
   ```
2. **Add your changes:**
   ```
   git add .
   ```
3. **Commit your changes:**
   ```
   git commit -m "Describe your changes"
   ```
4. **Push to GitHub:**
   ```
   git push origin main
   ```
   *(or use `master` if that's your branch name)*

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## **Contact**

For inquiries or feedback, contact the repository owner at **MystiFoe**.

---

## **Languages and Tools**

- **Languages**: Python, Jupyter Notebook
- **Libraries**: scikit-learn, pandas, NumPy, Matplotlib, XGBoost, Tkinter
