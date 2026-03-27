# Getting Started Guide - Electricity Price Forecasting Interface

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run src/app.py
```

Alternatively, use the helper script:
```bash
chmod +x ../run_project.sh
../run_project.sh start
```

### Step 3: Open in Browser
Your default browser should open automatically at `http://localhost:8501`

---

## 📋 Checklist Before Running

- [ ] Python 3.8+ installed
- [ ] Requirements installed: `pip install -r requirements.txt`
- [ ] Files present in directory structure:
  - [ ] `src/app.py`
  - [ ] `models/lgbm_model.joblib`
  - [ ] `models/scaler.joblib`
- [ ] Run command: `streamlit run src/app.py` or `./run_project.sh start`

---

## 🎯 First-Time User Quick Start

### 1. Single Prediction (Under 2 minutes)
1. Go to **"📊 Single Prediction"** tab
2. Set date and time
3. Adjust weather sliders (Temperature = 28°C, Humidity = 60%)
4. Set market volume to ~1200 MW
5. Click **"🔮 Predict Price"**
6. See the predicted electricity price!

**Example Results:**
- Low price (₹1,500): Good for buying
- High price (₹7,000): Good for selling
- Scarcity (₹10,000): Market stress event

### 2. Batch Prediction (Under 5 minutes)
1. Go to **"📈 Batch Prediction"** tab
2. Upload **`data/examples/example_batch_data.csv`** (included in the data folder)
3. Click **"🔮 Predict Batch Prices"**
4. View results and download CSV with predictions

---

## 📊 Understanding the Three Tabs

### Tab 1: Single Prediction 📊
- **For**: Quick price prediction for specific date/time
- **Inputs**: Date, time, weather, and market conditions
- **Output**: Single price prediction + interpretation
- **Use Case**: Check price for specific hour

### Tab 2: Batch Prediction 📈
- **For**: Multiple predictions at once
- **Inputs**: CSV file with many rows
- **Output**: All predictions + statistics + chart
- **Use Case**: Bulk forecasting, trend analysis

### Tab 3: Information ℹ️
- **For**: Learning about the system
- **Includes**: Feature explanations, trading tips, examples
- **Use Case**: Understand what each feature means

---

## 🎓 Understanding Your First Prediction

### Example 1: Afternoon Peak (Expensive)
```
Date: May 15, 2026 (Wednesday)
Time: 5:00 PM (Hour 17)
Temperature: 32°C (hot)
Humidity: 45% (dry)
Wind Speed: 1.2 m/s (calm)
Market Volume: 1500 MW (high demand)

Expected Price: ₹7,500/MWh 🔴
Reason: Hot weather → high AC demand → high price
Trading Tip: Good time to sell electricity
```

### Example 2: Night, Low Demand (Cheap)
```
Date: May 15, 2026
Time: 3:00 AM (Hour 3)
Temperature: 20°C (cool)
Humidity: 70%
Wind Speed: 3.5 m/s (windy)
Market Volume: 600 MW (low demand)

Expected Price: ₹1,800/MWh 🟢
Reason: Low demand at night, wind generation up
Trading Tip: Good time to buy electricity
```

---

## 📁 File Description

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python packages needed |
| `lgbm_model.joblib` | AI model for predictions |
| `scaler.joblib` | Data normalizer |
| `example_batch_data.csv` | Sample data for testing |
| `Frontend_Interface_README.md` | Detailed documentation |

---

## ⚠️ Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
# or
pip install -r requirements.txt
```

### Issue: "File not found" error for models
**Solution:** Ensure these files are in the same folder as `app.py`:
- `lgbm_model.joblib`
- `scaler.joblib`

### Issue: "Port 8501 is already in use"
**Solution:**
```bash
streamlit run app.py --server.port 8502
# Use a different port number
```

### Issue: Slow performance
**Solution:**
- Use batch prediction with smaller CSV files (< 1000 rows)
- Check available RAM
- Close other applications

---

## 🔟 Example Predictions

Try these configurations:

### Price = ~₹2,000 (Low/Normal)
- Hour: 3 (night)
- Temp: 18°C
- Humidity: 72%
- Wind: 3.5 m/s
- Market Volume: 700 MW

### Price = ~₹4,000 (Medium)
- Hour: 10 (morning)
- Temp: 25°C
- Humidity: 65%
- Wind: 2.0 m/s
- Market Volume: 1100 MW

### Price = ~₹7,500 (High)
- Hour: 17 (evening peak)
- Temp: 32°C
- Humidity: 45%
- Wind: 1.2 m/s
- Market Volume: 1500 MW

### Price = ~₹10,000 (Scarcity)
- Hour: 18 (evening)
- Temp: 35°C (very hot)
- Humidity: 30% (very dry)
- Wind: 0.5 m/s (no wind)
- Market Volume: 2000 MW (very high demand)
- Price 24h Ago: 9500

---

## 💡 Pro Tips

1. **Price varies by hour**: Evening (5-8 PM) and morning (7-10 AM) typically have peaks
2. **Temperature is key**: Hot days → high prices, cool days → low prices
3. **Wind matters**: High wind = more renewable generation = lower price
4. **For trading**: 
   - Buy when predictions show low price
   - Sell when predictions show high price
5. **Use historical data**: Reference "Price 24h Ago" from actual market data

---

## 📞 Need Help?

1. **Check Tab 3 (ℹ️)** - Has detailed explanations
2. **Read `Frontend_Interface_README.md`** - Full documentation
3. **Look at `example_batch_data.csv`** - Real data format example
4. **Review error messages** - Streamlit gives helpful hints

---

## 🎯 Next Steps After First Run

1. ✅ Successfully ran app
2. ✅ Made first prediction
3. ✅ Understood price interpretation
4. **Consider**: What real data can you connect?
5. **Consider**: How to integrate with trading system?
6. **Consider**: Batch predictions for weekly forecasts?

---

## 📞 Support Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **LightGBM**: https://lightgbm.readthedocs.io/
- **Pandas**: https://pandas.pydata.org/docs/
- **IEX Market Data**: https://www.iexindia.com/

---

**Happy Predicting! ⚡** 

For questions, refer to `Frontend_Interface_README.md` for detailed documentation.
