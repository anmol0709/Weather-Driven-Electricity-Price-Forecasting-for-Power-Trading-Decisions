import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Electricity Price Forecaster",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .prediction-result {
        background-color: #e8f5e9;
        padding: 2rem;
        border-radius: 0.5rem;
        border: 2px solid #4caf50;
        text-align: center;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)

REQUIRED_BATCH_COLUMNS = [
    'hour', 'day_of_week', 'month', 'temp', 'dwpt', 'rhum', 'wspd',
    'market_volume', 'bid_surplus', 'final_schedule', 'price_lag_24h'
]

FEATURES_TO_SCALE = [
    'market_volume', 'bid_surplus', 'final_schedule', 'price_lag_24h',
    'temp', 'temp_sq', 'dwpt', 'rhum', 'wspd'
]

FULL_MODEL_COLUMNS = [
    'market_volume', 'bid_surplus', 'final_schedule', 'price_lag_24h',
    'temp', 'temp_sq', 'dwpt', 'rhum', 'wspd',
    'hour', 'day_of_week', 'month', 'Hour', 'Month', 'day_of_year', 'week_of_year', 'quarter'
]

@st.cache_resource
def load_model_and_scaler():
    try:
        # Get the path to models directory relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, '..', 'models', 'lgbm_model.joblib')
        scaler_path = os.path.join(script_dir, '..', 'models', 'scaler.joblib')
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except FileNotFoundError as e:
        st.error(f"Models not found! Please ensure lgbm_model.joblib and scaler.joblib are in the models/ directory. Error: {e}")
        return None, None

# Title and description
st.title("⚡ Weather-Driven Electricity Price Forecasting")


def compute_temporal_features(selected_datetime: datetime) -> dict:
    return {
        'hour': selected_datetime.hour,
        'day_of_week': selected_datetime.weekday(),
        'month': selected_datetime.month,
        'Hour': selected_datetime.hour,
        'Month': selected_datetime.month,
        'day_of_year': selected_datetime.timetuple().tm_yday,
        'week_of_year': selected_datetime.isocalendar()[1],
        'quarter': (selected_datetime.month - 1) // 3 + 1
    }


def prepare_input_dataframe(inputs: dict) -> pd.DataFrame:
    df = pd.DataFrame([inputs])
    df['temp_sq'] = df['temp'] ** 2
    return df[FULL_MODEL_COLUMNS]


def interpret_price_range(value: float) -> tuple[str, str]:
    if value < 2000:
        return "🟢 Low (Favorable for buyers)", "green"
    if value < 4000:
        return "🟡 Medium (Normal market)", "orange"
    if value < 8000:
        return "🔴 High (Unfavorable for buyers)", "red"
    return "⚫ Scarcity State (Price ceiling)", "purple"


st.markdown("""
    ### Power Trading Decision Support System
    Predict electricity market prices based on weather conditions and market microstructure data
    from India's Energy Exchange (IEX).
""")

# Load model
model, scaler = load_model_and_scaler()

if model is None or scaler is None:
    st.stop()

# Create tabs for different input modes
tab1, tab2, tab3 = st.tabs(["📊 Single Prediction", "📈 Batch Prediction", "ℹ️ Information"])

with tab1:
    st.header("Single Price Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Date & Time Features")
        
        # Date and time input
        prediction_date = st.date_input(
            "Select Date",
            value=datetime.now(),
            help="Date for prediction"
        )
        
        prediction_hour = st.slider(
            "Select Hour (0-23)",
            min_value=0,
            max_value=23,
            value=12,
            step=1,
            help="Hour of the day in 24-hour format"
        )
        
        # Calculate temporal features centrally via helper
        dt = datetime.combine(prediction_date, datetime.min.time()).replace(hour=prediction_hour)
        temporal_features = compute_temporal_features(dt)

        st.info(
            f"**Selected Time:** {dt.strftime('%Y-%m-%d %H:%M')} | "
            f"Day of Week: {temporal_features['day_of_week']} | "
            f"Week: {temporal_features['week_of_year']} | "
            f"Quarter: {temporal_features['quarter']}"
        )

        # Unpack for streamline input dictionary creation
        day_of_week = temporal_features['day_of_week']
        month = temporal_features['month']
        day_of_year = temporal_features['day_of_year']
        week_of_year = temporal_features['week_of_year']
        quarter = temporal_features['quarter']

    with col2:
        st.subheader("🌡️ Weather Features")
        
        temperature = st.slider(
            "Temperature (°C)",
            min_value=-15.0,
            max_value=50.0,
            value=25.0,
            step=0.5,
            help="Ambient temperature in Celsius"
        )
        
        dew_point = st.slider(
            "Dew Point (°C)",
            min_value=-20.0,
            max_value=35.0,
            value=15.0,
            step=0.5,
            help="Dew point temperature"
        )
        
        humidity = st.slider(
            "Relative Humidity (%)",
            min_value=0,
            max_value=100,
            value=60,
            step=1,
            help="Relative humidity, capped at 100%"
        )
        
        wind_speed = st.slider(
            "Wind Speed (m/s)",
            min_value=0.0,
            max_value=15.0,
            value=3.0,
            step=0.1,
            help="Wind speed in meters per second"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("💹 Market Features")
        
        market_volume = st.number_input(
            "Market Volume (MW)",
            min_value=0.0,
            value=1000.0,
            step=10.0,
            help="Market clearing volume"
        )
        
        bid_surplus = st.number_input(
            "Bid Surplus (MW)",
            min_value=-5000.0,
            max_value=5000.0,
            value=0.0,
            step=10.0,
            help="Difference between Sell Bid and Purchase Bid"
        )
    
    with col4:
        st.subheader("📋 Additional Features")
        
        final_schedule = st.number_input(
            "Final Schedule (MW)",
            min_value=0.0,
            value=950.0,
            step=10.0,
            help="Final scheduled volume"
        )
        
        price_lag_24h = st.number_input(
            "Price 24 Hours Ago (₹/MWh)",
            min_value=0.0,
            value=3000.0,
            step=100.0,
            help="Market clearing price from 24 hours ago"
        )
    
    # Prepare data for prediction with shared helper and avoid duplicate temp_sq
    input_inputs = {
        'market_volume': market_volume,
        'bid_surplus': bid_surplus,
        'final_schedule': final_schedule,
        'price_lag_24h': price_lag_24h,
        'temp': temperature,
        'dwpt': dew_point,
        'rhum': humidity,
        'wspd': wind_speed,
        **temporal_features
    }

    input_data = prepare_input_dataframe(input_inputs)

    # Make prediction
    if st.button("🔮 Predict Price", use_container_width=True, type="primary"):
        input_data_scaled = input_data.copy()
        input_data_scaled[FEATURES_TO_SCALE] = scaler.transform(input_data[FEATURES_TO_SCALE])
        predicted_price = model.predict(input_data_scaled)[0]
        
        # Display results
        st.markdown("---")
        
        # Prediction result box
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown(f"""
                <div class="prediction-result">
                    <h3>Predicted Price</h3>
                    <h1 style="color: #4caf50;">₹ {predicted_price:,.2f} / MWh</h1>
                </div>
            """, unsafe_allow_html=True)
        
        with col_res2:
            # Price range interpretation
            if predicted_price < 2000:
                price_range = "🟢 Low (Favorable for buyers)"
                color = "green"
            elif predicted_price < 4000:
                price_range = "🟡 Medium (Normal market)"
                color = "orange"
            elif predicted_price < 8000:
                price_range = "🔴 High (Unfavorable for buyers)"
                color = "red"
            else:
                price_range = "⚫ Scarcity State (Price ceiling)"
                color = "purple"
            
            st.markdown(f"""
                <div class="metric-card" style="border-left-color: {color};">
                    <h4>Price Range Interpretation</h4>
                    <p style="font-size: 18px; font-weight: bold;">{price_range}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Display input summary
        st.subheader("📊 Input Summary")
        summary_df = pd.DataFrame({
            'Feature': ['Temperature', 'Humidity', 'Wind Speed', 'Market Volume', 'Day of Week', 'Hour'],
            'Value': [f"{temperature}°C", f"{humidity}%", f"{wind_speed} m/s", f"{market_volume} MW", 
                     f"{day_of_week} (0=Mon)", f"{prediction_hour}:00"]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

with tab2:
    st.header("Batch Prediction (Multiple Time Periods)")
    
    st.info("Upload a CSV file with hourly weather and market data to get predictions for multiple time periods.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="CSV with columns: hour, day_of_week, month, temperature, humidity, dew_point, wind_speed, market_volume, bid_surplus, final_schedule, price_lag_24h")
    
    if uploaded_file is not None:
        try:
            batch_data = pd.read_csv(uploaded_file)
            
            st.write("Preview of uploaded data:")
            st.dataframe(batch_data.head(10), use_container_width=True)
            
            # Ensure required columns exist
            required_cols = ['hour', 'day_of_week', 'month', 'temp', 'dwpt', 'rhum', 'wspd', 
                           'market_volume', 'bid_surplus', 'final_schedule', 'price_lag_24h']
            
            # Check if all required columns are present (case-insensitive)
            batch_data.columns = batch_data.columns.str.lower().str.strip()
            required_cols = [col.lower() for col in required_cols]
            
            missing_cols = [col for col in required_cols if col not in batch_data.columns]
            
            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
            else:
                if st.button("🔮 Predict Batch Prices", use_container_width=True, type="primary"):
                    # Prepare batch data
                    batch_df = batch_data[required_cols].copy()
                    
                    # Calculate derived features and ensure all columns
                    full_cols = ['market_volume', 'bid_surplus', 'final_schedule', 'price_lag_24h',
                               'temp', 'temp_sq', 'dwpt', 'rhum', 'wspd', 'hour', 'day_of_week',
                               'month', 'Hour', 'Month', 'day_of_year', 'week_of_year', 'quarter']
                    
                    # Add missing columns with reasonable defaults if needed
                    if 'temp_sq' not in batch_df.columns:
                        batch_df['temp_sq'] = batch_df['temp'] ** 2
                    if 'Hour' not in batch_df.columns and 'hour' in batch_df.columns:
                        batch_df['Hour'] = batch_df['hour']
                    if 'Month' not in batch_df.columns and 'month' in batch_df.columns:
                        batch_df['Month'] = batch_df['month']
                    if 'day_of_year' not in batch_df.columns:
                        batch_df['day_of_year'] = 1  # Default
                    if 'week_of_year' not in batch_df.columns:
                        batch_df['week_of_year'] = 1  # Default
                    if 'quarter' not in batch_df.columns:
                        batch_df['quarter'] = 1  # Default
                    
                    # Reorder columns
                    batch_df = batch_df[full_cols]
                    
                    # Scale features
                    batch_scaled = batch_df.copy()
                    batch_scaled[FEATURES_TO_SCALE] = scaler.transform(batch_df[FEATURES_TO_SCALE])
                    
                    # Make predictions
                    batch_predictions = model.predict(batch_scaled)
                    
                    # Add predictions to dataframe
                    result_df = batch_data.copy()
                    result_df['Predicted_Price_(Rs/MWh)'] = batch_predictions
                    
                    # Statistics
                    st.subheader("📈 Prediction Statistics")
                    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                    
                    with col_stat1:
                        st.metric("Average Price", f"₹ {batch_predictions.mean():,.2f}")
                    with col_stat2:
                        st.metric("Max Price", f"₹ {batch_predictions.max():,.2f}")
                    with col_stat3:
                        st.metric("Min Price", f"₹ {batch_predictions.min():,.2f}")
                    with col_stat4:
                        st.metric("Std Dev", f"₹ {batch_predictions.std():,.2f}")
                    
                    # Display results
                    st.subheader("🔍 Detailed Results")
                    st.dataframe(result_df, use_container_width=True)
                    
                    # Download results
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Plot price predictions
                    if 'hour' in batch_data.columns:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=batch_data.index,
                            y=batch_predictions,
                            mode='lines+markers',
                            name='Predicted Price',
                            line=dict(color='#1f77b4', width=2),
                            marker=dict(size=6)
                        ))
                        fig.update_layout(
                            title='Price Predictions Over Time',
                            xaxis_title='Sample Index',
                            yaxis_title='Price (₹/MWh)',
                            hovermode='x unified',
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

with tab3:
    st.header("ℹ️ About This Forecasting System")
    
    st.markdown("""
    ### Project Overview
    This application forecasts electricity market prices for India's Energy Exchange (IEX) 
    using a combination of:
    - **Weather Data**: Temperature, humidity, dew point, wind speed
    - **Market Microstructure**: Trading volume, bid-ask dynamics
    - **Temporal Features**: Hour, day of week, seasonal patterns
    
    ### Model Details
    - **Model Type**: LightGBM (Light Gradient Boosting Machine)
    - **Input Features**: 15 engineered features
    - **Target Variable**: Market Clearing Price (MCP) in ₹/MWh
    - **Data Period**: February 2024 onwards
    
    ### Key Features
    
    1. **Weather Integration**
       - Uses temperature, humidity, dew point, and wind speed as features
       - Temperature squared captures nonlinear demand impact
       - Humidity and wind speed capture environmental demand effects
    
    2. **Market Features**
       - Bid surplus: Difference between sell and purchase bids
       - Market volume: Total cleared volume in MW
       - Lagged price (24h): Captures daily patterns
    
    3. **Temporal Decomposition**
       - Hour of day, day of week, month
       - Day/week/quarter of year
       - Captures recurring demand patterns
    
    ### Understanding Price Ranges
    - **₹0-2,000/MWh**: Low prices (buyer favorable)
    - **₹2,000-4,000/MWh**: Normal market conditions
    - **₹4,000-8,000/MWh**: High prices (seller favorable)
    - **₹8,000-10,000/MWh**: Scarcity events
    - **₹10,000/MWh**: Price ceiling (regulatory limit)
    
    ### Features Explained
    
    **Weather Variables:**
    - Temperature: Primary demand driver (cooling/heating)
    - Dew Point: Moisture content affecting thermal comfort
    - Humidity: Relative moisture percentage
    - Wind Speed: Renewable generation potential
    
    **Market Variables:**
    - Market Volume: Total MW cleared at given price
    - Bid Surplus: imbalance between supply and demand bids
    - Final Schedule: Committed volume from previous auctions
    - Price Lag 24h: Previous day same-hour price (strong cyclic pattern)
    
    ### Trading Implications
    - **High predictions**: Potential scarcity, buy opportunities
    - **Low predictions**: Oversupply, sell opportunities
    - **High volatility periods**: Early morning, evening peak hours
    - **Weather sensitivity**: High summer and winter impacts
    
    ### Limitations
    - Model trained on historical IEX data (Feb 2024 onwards)
    - Does not account for policy changes or market interventions
    - Weather forecasts required for true future predictions
    - 15-minute rolling predictions recommended for near-term forecasting
    """)
    
    st.markdown("---")
    
    st.subheader("Required Input Columns for Batch Prediction")
    
    columns_info = pd.DataFrame({
        'Column Name': [
            'hour', 'day_of_week', 'month', 'temp', 'dwpt', 'rhum', 'wspd',
            'market_volume', 'bid_surplus', 'final_schedule', 'price_lag_24h'
        ],
        'Description': [
            'Hour of day (0-23)',
            'Day of week (0=Monday, 6=Sunday)',
            'Month (1-12)',
            'Temperature in °C',
            'Dew point in °C',
            'Relative humidity (%)',
            'Wind speed (m/s)',
            'Market volume in MW',
            'Bid surplus in MW',
            'Final schedule in MW',
            'Price from 24 hours ago (₹/MWh)'
        ],
        'Data Type': ['Integer', 'Integer', 'Integer', 'Float', 'Float', 'Float', 'Float',
                     'Float', 'Float', 'Float', 'Float']
    })
    
    st.dataframe(columns_info, use_container_width=True, hide_index=True)
    
    st.info("""
    **Example CSV Format:**
    ```
    hour,day_of_week,month,temp,dwpt,rhum,wspd,market_volume,bid_surplus,final_schedule,price_lag_24h
    9,2,5,28.5,18.2,65,2.3,1200,150.5,1100,3200
    10,2,5,29.1,18.8,63,2.1,1250,120.3,1150,3150
    ```
    """)
