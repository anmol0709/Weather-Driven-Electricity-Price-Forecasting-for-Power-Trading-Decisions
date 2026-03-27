# Weather-Driven-Electricity-Price-Forecasting-for-Power-Trading-Decisions
Forecast electricity market clearing prices with a Streamlit-based UI that combines weather and market signals.
Model inference uses a pre-trained LightGBM model and standard scaler; data preparation is directly supported for single and batch prediction.

## Features

- **Real-time Price Prediction**: Get instant electricity price forecasts based on weather and market conditions
- **Batch Processing**: Upload CSV files to process multiple time periods at once
- **Interactive Visualizations**: View price trends with interactive Plotly charts
- **Export Results**: Download predictions in CSV format for further analysis
- **Comprehensive Documentation**: Built-in guides and feature explanations

## Project Structure

```
Weather-Driven-Electricity-Price-Forecasting-for-Power-Trading-Decisions/
│
├── src/                               Source code
│   └── app.py                         Main Streamlit web interface
│
├── models/                            Pre-trained ML models
│   ├── lgbm_model.joblib              Trained LightGBM model (required)
│   └── scaler.joblib                  Feature scaler (required)
│
├── data/                              Data files
│   ├── examples/
│   │   └── example_batch_data.csv     Sample batch prediction data
│   └── training/                      Training datasets
│
├── notebooks/                         Jupyter notebooks
│   └── ElectrcityPriceForecast.ipynb  Original analysis notebook
│
├── deployment/                        Deployment configuration
│   ├── Dockerfile                     Docker container image
│   ├── docker-compose.yml             Docker Compose configuration
│   └── .streamlit/                    Streamlit configuration
│
├── docs/                              Documentation
│   ├── README.md                      This file
│   ├── QUICK_REFERENCE.md             Quick reference guide
│   ├── GETTING_STARTED.md             Setup instructions
│   ├── ARCHITECTURE.md                System architecture
│   ├── DEPLOYMENT_GUIDE.md            Production deployment guide
│   ├── Frontend_Interface_README.md   Complete feature documentation
│   └── INTERFACE_SUMMARY.md           Interface summary
│
├── requirements.txt                   Python dependencies
├── run_project.sh                     Helper script for running the project
└── .git/                              Git repository
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application directly
streamlit run src/app.py
```

Or use the helper script:

```bash
# make executable first if needed
chmod +x run_project.sh

./run_project.sh check      # Verify required files
./run_project.sh install    # Set up virtual environment
./run_project.sh start      # Launch the app
```

The application will open at `http://localhost:8501`

## Usage

### Single Price Prediction

1. Navigate to the "Single Prediction" tab
2. Enter date and time
3. Provide weather conditions (temperature, humidity, wind speed, dew point)
4. Enter market data (volume, bid surplus, final schedule, lagged price)
5. Click "Predict Price" to generate forecast

The application displays the predicted price in ₹/MWh along with interpretation of the price level.

### Batch Predictions

1. Navigate to the "Batch Prediction" tab
2. Upload a CSV file with the required columns
3. Review the preview
4. Click "Predict Batch Prices"
5. Download results as CSV

Required CSV columns:
- hour, day_of_week, month
- temp, dwpt, rhum, wspd
- market_volume, bid_surplus, final_schedule, price_lag_24h

### Information

The "Information" tab provides:
- Feature descriptions and their significance
- Trading interpretation guidelines
- Model performance characteristics
- CSV format specifications

## Technical Specifications

### Technology Stack

- **Frontend**: Streamlit 1.28+ (interactive web framework)
- **ML Model**: LightGBM (gradient boosting regressor)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (interactive charts)
- **Deployment**: Docker, Docker Compose
- **Python**: 3.8+

### Model Details

```
Model Type:      LightGBM Regressor
Training Data:   IEX market data (Feb 2024 - present)
Features:        15 engineered variables
Target:          Market Clearing Price (₹/MWh)
Accuracy:        R² > 0.7 (varies by season)
Prediction Unit: 15-minute intervals
```

### Input Features (15 Total)

**Weather (5 features):**
- Temperature (°C)
- Temperature squared (for nonlinear relationships)
- Dew Point (°C)
- Relative Humidity (%)
- Wind Speed (m/s)

**Market (4 features):**
- Market Volume (MW)
- Bid Surplus (MW)
- Final Schedule (MW)
- Price 24 Hours Ago (₹/MWh)

**Temporal (6 features):**
- Hour of Day (0-23)
- Day of Week (0=Monday, 6=Sunday)
- Month (1-12)
- Day of Year (1-365)
- Week of Year (1-52)
- Quarter (1-4)

## Deployment

### Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

Access the application at `http://localhost:8501`

### Docker

```bash
docker-compose up --build
```

Access the application at `http://localhost:8501`

### Cloud Platforms

**Streamlit Cloud (Free)**
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Deploy in 2 clicks

**Other Options:**
- AWS: ECS, Lambda, EC2
- Google Cloud: Cloud Run
- Azure: Container Instances, App Service
- Heroku: Heroku Dynos

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

## Price Range Interpretation

| Price Range | Condition | Trading Signal |
|---|---|---|
| ₹0-2,000/MWh | Low (Oversupply) | Buy opportunity |
| ₹2,000-4,000/MWh | Medium (Normal) | Monitor conditions |
| ₹4,000-8,000/MWh | High (Tight supply) | Sell opportunity |
| ₹8,000-10,000/MWh | Critical (Scarcity) | Market stress alert |

## Model Accuracy and Limitations

### Strengths

- Works well for normal market conditions (R² > 0.7)
- Captures weather-demand correlations effectively
- Provides reliable forecasts during regular trading periods
- Summer forecasts typically more accurate than winter

### Limitations

- Cannot predict policy or regulatory changes
- Requires accurate weather input for valid predictions
- Limited effectiveness during unprecedented market events
- Historical patterns may not capture future market dynamics

### Best Practices

- Use real or forecast weather data (not arbitrary values)
- Verify market inputs are current
- Compare predictions with actual prices for validation
- Account for known market interventions manually
- Use predictions as one input in ensemble forecasting

## Troubleshooting

### Issue: ModuleNotFoundError

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Models not found

Verify that `lgbm_model.joblib` and `scaler.joblib` exist in the project directory, in the same location as `app.py`.

### Issue: Port already in use

Run the application on a different port:
```bash
streamlit run app.py --server.port 8080
```

### Issue: Slow performance with large batch files

- Split CSV files into smaller chunks (fewer than 1000 rows each)
- Check available system memory
- Close other applications consuming resources

## Use Cases

### Daily Trading
- Use morning forecast to plan daily trading strategy
- Identify expected high and low price periods
- Update predictions mid-day as new data becomes available

### Weekly Planning
- Upload 7-day weather forecast with market assumptions
- Generate bulk predictions for planning period
- Share CSV results with trading team
- Execute planned trades according to forecast

### Market Analysis
- Track prediction accuracy against actual prices
- Analyze weather-price correlations
- Generate weekly reports
- Identify seasonal patterns

### Risk Management
- Monitor for extreme weather alerts
- Prepare for potential price spikes
- Assess scarcity probabilities
- Coordinate with trading desk

## Documentation

Refer to the following for detailed information:

- **QUICK_REFERENCE.md**: Quick lookup guide for common tasks
- **GETTING_STARTED.md**: Step-by-step setup instructions
- **Frontend_Interface_README.md**: Comprehensive feature documentation
- **DEPLOYMENT_GUIDE.md**: Production deployment procedures
- **ARCHITECTURE.md**: System design and data flow

## Verification Checklist

Before running the application, verify:

- Python 3.8+ is installed
- `app.py` exists in the project directory
- `lgbm_model.joblib` exists (required)
- `scaler.joblib` exists (required)
- `requirements.txt` is present
- Dependencies are installed: `pip install -r requirements.txt`

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB for dependencies and models
- **Network**: Internet connection for initial setup (optional after)

## Performance Characteristics

**Single Prediction:**
- Input processing: 50-100ms
- Model inference: 10-50ms
- Total response time: 150-300ms

**Batch Prediction (1000 rows):**
- File processing: 1-2s
- Model inference: 1-2s
- Result aggregation: 1-2s
- Total time: 8-12 seconds

## Related Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [India Energy Exchange (IEX)](https://www.iexindia.com/)

## Version Information

- **Application**: 1.0
- **Framework**: Streamlit 1.28+
- **Python**: 3.8+
- **Last Updated**: March 2026

## License

This project follows the license specified in the parent Weather-Driven Electricity Price Forecasting project.

---

For questions or issues, refer to the appropriate documentation file in the project directory.
