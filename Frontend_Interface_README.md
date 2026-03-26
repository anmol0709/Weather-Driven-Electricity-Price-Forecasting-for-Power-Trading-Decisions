# Electricity Price Forecasting - Frontend Interface

## 🎯 Overview

This is a **Streamlit web application** that provides an interactive interface for electricity price forecasting using the trained LGBM machine learning model. Users can input weather and market data to get real-time electricity price predictions for India's Energy Exchange (IEX).

## ✨ Features

### 1. **Single Price Prediction** 📊
- Input individual weather and market conditions
- Get instant price predictions
- View price range interpretations (Low/Medium/High/Scarcity)
- Interactive weather and market feature controls

### 2. **Batch Prediction** 📈
- Upload CSV files with multiple time periods
- Process bulk predictions efficiently
- Download results as CSV
- View statistical summaries (mean, min, max, std dev)
- Visualize price trends over time

### 3. **Information & Documentation** ℹ️
- Detailed project information
- Feature explanations and trading implications
- Model performance details
- CSV format specifications

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone/Navigate to the project directory:**
```bash
cd /path/to/Weather-Driven-Electricity-Price-Forecasting-for-Power-Trading-Decisions
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Single Prediction Mode

1. **Navigate to "📊 Single Prediction" tab**

2. **Input Date & Time Features:**
   - Select a date
   - Choose hour of day (0-23)
   - The app automatically calculates: day of week, month, day of year, week of year, quarter

3. **Input Weather Features:**
   - Temperature (°C): -15 to 50
   - Dew Point (°C): -20 to 35
   - Relative Humidity (%): 0-100
   - Wind Speed (m/s): 0-15

4. **Input Market Features:**
   - Market Volume (MW): Trading volume
   - Bid Surplus (MW): Sell bid - Purchase bid difference
   - Final Schedule (MW): Previous auction commitment
   - Price 24h Ago (₹/MWh): Same hour price from previous day

5. **Click "🔮 Predict Price"** to get results

6. **View Results:**
   - Predicted price in ₹/MWh
   - Price range interpretation with trading implications
   - Input summary table

### Batch Prediction Mode

1. **Navigate to "📈 Batch Prediction" tab**

2. **Prepare CSV File** with the following columns:
   ```
   hour, day_of_week, month, temp, dwpt, rhum, wspd, market_volume,
   bid_surplus, final_schedule, price_lag_24h
   ```

3. **Upload CSV File** using the file uploader

4. **Preview** uploaded data

5. **Click "🔮 Predict Batch Prices"** to process

6. **View Results:**
   - Statistical summary (Average, Max, Min, Std Dev)
   - Detailed results table
   - Price trend visualization
   - Download option

### Example CSV Format

```csv
hour,day_of_week,month,temp,dwpt,rhum,wspd,market_volume,bid_surplus,final_schedule,price_lag_24h
9,2,5,28.5,18.2,65,2.3,1200,150.5,1100,3200
10,2,5,29.1,18.8,63,2.1,1250,120.3,1150,3150
11,2,5,30.2,19.5,60,1.9,1300,100.2,1200,3250
12,2,5,31.0,20.1,58,1.7,1350,80.5,1250,3300
```

## 📊 Understanding Price Ranges

| Price Range | Interpretation | Trading Implication |
|------------|-----------------|-------------------|
| ₹0-2,000 | Low (Buyer favorable) | Good buying opportunity |
| ₹2,000-4,000 | Medium (Normal market) | Balanced conditions |
| ₹4,000-8,000 | High (Seller favorable) | Good selling opportunity |
| ₹8,000-10,000 | Scarcity events | High market stress |
| ₹10,000 | Price ceiling | Regulatory limit reached |

## 🔧 Input Features Explained

### Weather Variables
- **Temperature (temp)**: Primary demand driver for heating/cooling
- **Dew Point (dwpt)**: Moisture content affecting thermal comfort
- **Relative Humidity (rhum)**: Atmospheric moisture percentage
- **Wind Speed (wspd)**: Affects renewable energy generation

### Market Variables
- **Market Volume**: Total MW cleared at that price point
- **Bid Surplus**: Difference between sell and purchase bids (supply-demand imbalance)
- **Final Schedule**: Volume committed from previous day-ahead auction
- **Price Lag 24h**: Previous day's same-hour price (strong cyclical pattern)

### Temporal Variables
- **Hour**: Time of day (0-23) - captures intraday demand patterns
- **Day of Week**: 0=Monday to 6=Sunday - captures weekly patterns
- **Month**: 1-12 - captures seasonal effects
- **Other**: Day of year, Week of year, Quarter - for granular seasonal decomposition

## 📈 Model Details

| Attribute | Details |
|-----------|---------|
| Model Type | LightGBM (Light Gradient Boosting Machine) |
| Training Data | IEX market data from Feb 2024 onwards |
| Features | 15 engineered features |
| Target Variable | Market Clearing Price (MCP) in ₹/MWh |
| Input Variables | 15 features (weather, market, temporal) |
| Prediction Interval | 15-minute trading blocks |

## ⚙️ Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: LightGBM, Scikit-learn
- **Visualization**: Plotly
- **Model Serialization**: Joblib

## 📁 Project Structure

```
.
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── lgbm_model.joblib        # Trained LGBM model
├── scaler.joblib            # StandardScaler for feature normalization
├── Python file_FP1_Group_08.ipynb  # Original notebook with model training
├── merged_data.csv          # Historical market + weather data
├── README.md                # Project documentation
└── Frontend_Interface_README.md  # This file
```

## 🎓 How to Prepare Batch Prediction Data

### Method 1: Export from your database/system
```python
# Make sure to include these columns:
required_columns = [
    'hour', 'day_of_week', 'month', 
    'temp', 'dwpt', 'rhum', 'wspd',
    'market_volume', 'bid_surplus', 'final_schedule', 'price_lag_24h'
]
```

### Method 2: Create from weather API data
```python
import pandas as pd
from datetime import datetime

# Create batch data from weather API
batch_data = pd.DataFrame({
    'hour': [9, 10, 11, 12],
    'day_of_week': [2, 2, 2, 2],  # Wednesday
    'month': [5, 5, 5, 5],  # May
    'temp': [28.5, 29.1, 30.2, 31.0],
    'dwpt': [18.2, 18.8, 19.5, 20.1],
    'rhum': [65, 63, 60, 58],
    'wspd': [2.3, 2.1, 1.9, 1.7],
    'market_volume': [1200, 1250, 1300, 1350],
    'bid_surplus': [150.5, 120.3, 100.2, 80.5],
    'final_schedule': [1100, 1150, 1200, 1250],
    'price_lag_24h': [3200, 3150, 3250, 3300]
})

batch_data.to_csv('predictions_input.csv', index=False)
```

## 🐳 Docker Deployment (Optional)

To deploy as a Docker container:

1. **Create Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY lgbm_model.joblib .
COPY scaler.joblib .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and run:**
```bash
docker build -t electricity-forecaster .
docker run -p 8501:8501 electricity-forecaster
```

## 🔍 Troubleshooting

### "Models not found" error
- Ensure `lgbm_model.joblib` and `scaler.joblib` are in the same directory as `app.py`
- Verify files were created from notebook training cells

### CSV upload errors
- Check that all required column names are present
- Ensure numeric columns contain valid numbers (no text)
- Use lowercase column names or verify exact column names

### Slow predictions
- Reduce batch size (split large CSV into smaller files)
- Check system memory availability
- Consider running on a machine with GPU support

## 📧 Model Performance Notes

- **Accuracy**: Varies by market conditions
- **Best for**: Short-term (15-minute to hourly) forecasts
- **Limitations**: 
  - Does not account for policy changes
  - Requires accurate weather forecasts for future predictions
  - May underperform during extreme market events
  - Performance varies significantly between seasons

## 🤝 Integration with Trading Systems

### Real-time Integration Example:
```python
# Load model and scaler
import joblib
model = joblib.load('lgbm_model.joblib')
scaler = joblib.load('scaler.joblib')

# Get current weather and market data
current_data = fetch_current_data()  # Your data source

# Make prediction
prediction = model.predict(scaler.transform(current_data))

# Use for trading decisions
if prediction < 2000:
    execute_buy_order(prediction)
elif prediction > 6000:
    execute_sell_order(prediction)
```

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [IEX Market Data](https://www.iexindia.com/)

## 📝 Example Scenarios

### Scenario 1: Peak Demand Period
```
Hour: 17 (5 PM - high demand peak)
Temperature: 32°C
Humidity: 45%
Wind: 1.2 m/s
Market Volume: 1500 MW
Expected: High price (₹6,000-₹8,000+)
Decision: Good selling opportunity
```

### Scenario 2: Low Demand Period
```
Hour: 3 (3 AM - low demand)
Temperature: 20°C
Humidity: 70%
Wind: 3.5 m/s
Market Volume: 600 MW
Expected: Low price (₹1,500-₹2,500)
Decision: Good buying opportunity
```

### Scenario 3: Scarcity Event
```
Hour: 18 (Peak evening)
Temperature: 35°C
Humidity: 30%
Wind: 0.5 m/s (very low)
Market Volume: 2000 MW (high demand)
Price Lag: 9500
Expected: Scarcity (₹9,000-₹10,000)
Decision: Market stress detected
```

---

**Version**: 1.0  
**Last Updated**: 2026-03-21  
**Contact**: [Your Contact Info]
