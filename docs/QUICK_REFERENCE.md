# Quick Reference Card

## 🚀 Getting Started in 30 Seconds

```bash
pip install -r requirements.txt && streamlit run src/app.py
```

Then open: **http://localhost:8501**

---

## 📊 Interface Tabs

| Tab | Use Case | Time |
|-----|----------|------|
| 📊 Single Prediction | One price forecast | 2 min |
| 📈 Batch Prediction | Multiple forecasts | 5 min |
| ℹ️ Information | Learn features | 10 min |

---

## 🎮 Input Fields Guide

### Date & Time
```
Date: Any date (auto-calculates day of week, month)
Hour: 0-23 (midnight=0, noon=12, evening=18)
```

### Weather (Usually from weather API/forecast)
```
Temperature: °C (-15 to 50)
Dew Point: °C (-20 to 35)
Humidity: % (0-100, auto-capped)
Wind Speed: m/s (0-15, realistic: 0.5-5)
```

### Market Data (Usually from exchange data)
```
Market Volume: MW (typical: 600-2000)
Bid Surplus: MW (supply-demand, typical: -500 to +500)
Final Schedule: MW (typical: 80% of volume)
Price 24h Ago: ₹/MWh (from previous day same hour)
```

---

## 💬 Common Inputs

### Night (3 AM)
```
Hour: 3
Temp: 18°C
Humidity: 70%
Wind: 3.0 m/s
Volume: 700 MW
Expected: ~₹1,800
```

### Morning Peak (8 AM)
```
Hour: 8
Temp: 24°C
Humidity: 65%
Wind: 2.0 m/s
Volume: 1100 MW
Expected: ~₹3,200
```

### Afternoon Peak (3 PM)
```
Hour: 15
Temp: 30°C
Humidity: 55%
Wind: 1.5 m/s
Volume: 1300 MW
Expected: ~₹5,500
```

### Evening Peak (6 PM)
```
Hour: 18
Temp: 32°C
Humidity: 45%
Wind: 1.0 m/s
Volume: 1500 MW
Expected: ~₹7,500
```

---

## 📈 Price Interpretation

```
₹0-2,000    🟢 LOW      | Good for buyers  | Oversupply
₹2-4K       🟡 MEDIUM   | Normal conditions | Balanced
₹4-8K       🔴 HIGH     | Good for sellers | Supply tight
₹8-10K      ⚫ SCARCITY  | Market stress   | Emergency
```

---

## 📊 Batch CSV Format

### Required Columns:
```
hour, day_of_week, month, temp, dwpt, rhum, wspd,
market_volume, bid_surplus, final_schedule, price_lag_24h
```

### Example Row:
```
9,2,5,28.5,18.2,65,2.3,1200,150.5,1100,3200
```

**Column Meanings:**
- hour: 0-23
- day_of_week: 0=Mon, 6=Sun
- month: 1-12
- temp: °C
- dwpt: dew point °C
- rhum: humidity %
- wspd: wind m/s
- market_volume: MW
- bid_surplus: MW
- final_schedule: MW
- price_lag_24h: ₹/MWh

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Problem: "Models not found"
- Check `lgbm_model.joblib` and `scaler.joblib` exist
- Run notebook training cells if missing

### Problem: "Port already in use"
```bash
streamlit run src/app.py --server.port 8080
```

### Problem: Slow on large batch
- Split CSV into smaller files (< 1000 rows)
- Check available RAM
- Use batch prediction instead of single

---

## 📚 Where to Find Help

| Topic | Location |
|-------|----------|
| Quick start | GETTING_STARTED.md |
| All features | Frontend_Interface_README.md |
| Deployment | DEPLOYMENT_GUIDE.md |
| Example data | data/examples/example_batch_data.csv |
| Full info | Tab: ℹ️ Information |

---

## ⌨️ Keyboard Shortcuts (Browser)

```
R         Rerun app (after Cmd+S)
C         Clear cache
K         Close sidebar
V         View app source
```

---

## 🎯 Popular Use Cases

### 1. Quick Price Check
1. Set date/time/weather
2. Enter market data
3. Click Predict
4. See result in seconds

### 2. Daily Forecast
1. Prepare 24-hour CSV
2. Upload batch file
3. Download results
4. Share chart with team

### 3. Trading Signal
1. Predict hourly prices
2. Prices < 2000? Buy signal
3. Prices > 7000? Sell signal
4. Automate decisions

### 4. Market Analysis
1. Batch predict week of data
2. Visualize price trends
3. Correlate with weather
4. Plan purchases/sales

---

## 📞 Model Info

```
Model: LightGBM
Training Data: Feb 2024 - Present
Accuracy: R² > 0.7 (varies by season)
Features: 15 (weather + market + time)
Prediction: Next 15-min MCP in ₹/MWh
```

---

## 🔒 Tips for Accurate Predictions

1. ✅ Use real weather data (not arbitrary)
2. ✅ Enter accurate market data
3. ✅ Use recent price_lag_24h value
4. ✅ Check for extreme weather events
5. ✅ Verify prediction seems reasonable
6. ✅ Compare with actual prices after
7. ✅ Adjust for policy changes manually

---

## 💡 Pro Tips

- **Humidity > 80%**: Price usually goes down (cooler)
- **Wind > 4 m/s**: Price usually goes down (more wind generation)
- **4-6 PM**: Most expensive period (evening peak)
- **2-4 AM**: Cheapest period (low demand)
- **Summer months**: Higher prices (AC demand)
- **Monday-Thursday**: Higher prices than weekends
- **Temperature extremes**: Highest prices (both hot and cold)

---

## 🚀 Deployment in One Command

```bash
# Local
streamlit run src/app.py

# Docker (from project root)
docker-compose -f deployment/docker-compose.yml up --build

# Cloud (after git push)
# - Go to share.streamlit.io
# - Click "New app"
# - Select repo and deploy!
```

---

## 📊 Expected Outputs

### Single Prediction Returns:
- Exact predicted price (₹/MWh)
- Price range (Low/Med/High/Scarcity)
- Trading recommendation
- Input summary table

### Batch Prediction Returns:
- Statistics (avg, min, max, std dev)
- Full results table
- Price trend chart
- Downloadable CSV

---

## 🎓 Learning Path

1. **Beginner**: Run single prediction with examples → GETTING_STARTED.md
2. **Intermediate**: Upload batch CSV → Frontend_Interface_README.md
3. **Advanced**: Deploy to cloud → DEPLOYMENT_GUIDE.md
4. **Expert**: Integrate into trading system → See Tab 3 for API info

---

## 📌 Remember

```
🎯 Goal: Predict electricity prices accurately
💼 Use: Trading decisions, market analysis
📊 Input: Weather + market conditions
⚡ Output: Price forecast in ₹/MWh
✅ Status: Production ready!
```

---

**Created:** March 2026  
**Version:** 1.0  
**Status:** ✅ All systems go!

**Happy Forecasting! ⚡**
