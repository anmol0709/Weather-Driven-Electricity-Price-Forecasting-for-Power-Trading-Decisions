# System Architecture & Data Flow

## 🏗️ Overall Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                      │
│                   (Streamlit Web App)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tab 1: Single       Tab 2: Batch      Tab 3: Info  │  │
│  │  Prediction          Prediction        & Docs       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Input Validation → Data Processing → Prediction   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                     ML MODEL LAYER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Feature Scaling  →  LightGBM Model  →  Result      │  │
│  │  (scaler.joblib)   (lgbm_model.joblib)              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Prediction Result  →  Visualization  →  Export    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Single Prediction Flow

```
USER INPUT
    ↓
┌─────────────────────┐
│ Date & Time         │ → Calculate day_of_week, month, etc.
│ Weather Data        │ → Temperature, Humidity, Wind
│ Market Data         │ → Volume, Bid Surplus, Schedule
└─────────────────────┘
    ↓
VALIDATION
    ↓
┌─────────────────────┐
│ Check Ranges        │ → All values within valid ranges
│ Check Required      │ → All fields provided
└─────────────────────┘
    ↓
DATA PROCESSING
    ↓
┌─────────────────────┐
│ Feature Creation    │ → Calculate Temp², etc.
│ Feature Scaling     │ → Normalize using scaler.joblib
│ Format Input        │ → Prepare for model
└─────────────────────┘
    ↓
ML PREDICTION
    ↓
┌─────────────────────┐
│ LightGBM Model      │ → Predict: ₹/MWh
└─────────────────────┘
    ↓
RESULT INTERPRETATION
    ↓
┌─────────────────────┐
│ Price Category      │ → Low/Medium/High/Scarcity
│ Trading Signal      │ → Buy/Sell/Hold
│ Display Result      │ → Show price + interpretation
└─────────────────────┘
    ↓
OUTPUT
```

---

## 📈 Batch Prediction Flow

```
USER UPLOADS CSV
    ↓
┌─────────────────────┐
│ Read File           │ → Load CSV into memory
└─────────────────────┘
    ↓
VALIDATION
    ↓
┌─────────────────────┐
│ Check Columns       │ → Verify required columns exist
│ Check Data Types    │ → Ensure numeric where needed
│ Check Values        │ → Within valid ranges
└─────────────────────┘
    ↓
PREVIEW & APPROVAL
    ↓
┌─────────────────────┐
│ Show First 10 Rows  │ → User confirms data looks right
│ Show Statistics     │ → Column ranges, types
└─────────────────────┘
    ↓
BATCH PROCESSING
    ↓
┌──────────────────────────────────────────┐
│ For each row:                            │
│  ├─ Calculate derived features           │
│  ├─ Scale features using scaler          │
│  ├─ Pass to LightGBM model               │
│  └─ Collect prediction                   │
└──────────────────────────────────────────┘
    ↓
AGGREGATE RESULTS
    ↓
┌─────────────────────┐
│ Calculate Stats     │ → Mean, Min, Max, Std Dev
│ Add to DataFrame    │ → Include in results
└─────────────────────┘
    ↓
VISUALIZATION
    ↓
┌─────────────────────┐
│ Create Chart        │ → Line chart of predictions
│ Show Table          │ → All results with predictions
└─────────────────────┘
    ↓
EXPORT
    ↓
┌─────────────────────┐
│ Generate CSV        │ → Original data + predictions
│ Provide Download    │ → User downloads results
└─────────────────────┘
    ↓
OUTPUT
```

---

## 🔄 Data Transformation Pipeline

```
RAW INPUT
┌────────────────────┐
│ Date: 2026-05-15   │
│ Hour: 15           │
│ Temp: 30.0        │
│ Humidity: 55      │
│ Wind: 1.5         │
│ Volume: 1300      │
│ etc...            │
└────────────────────┘
    ↓
FEATURE ENGINEERING
┌────────────────────┐
│ Temp² = 900.0      │
│ Day_of_week = 2    │
│ Month = 5          │
│ Quarter = 2        │
│ Week_of_year = 19  │
│ Day_of_year = 135  │
└────────────────────┘
    ↓
STANDARDIZATION
┌────────────────────────────────────────┐
│ Using StandardScaler from training:    │
│ weather_vars = (raw - mean) / std      │
│ All in [-2 to +2] range                │
└────────────────────────────────────────┘
    ↓
PREPARATION FOR MODEL
┌────────────────────┐
│ 15 features total: │
│ ├─ 9 normalized    │
│ ├─ 1 volume-like   │
│ └─ 5 categorical   │
│                    │
│ Ready for LightGBM │
└────────────────────┘
    ↓
MODEL INPUT
```

---

## 🧠 Model Architecture

```
LIGHTGBM REGRESSOR
│
├─ Input Layer (15 features)
│  ├─ market_volume
│  ├─ bid_surplus
│  ├─ final_schedule
│  ├─ price_lag_24h      } (scaled)
│  ├─ temp, temp_sq
│  ├─ dwpt, rhum, wspd
│  ├─ hour                } (categorical)
│  ├─ day_of_week
│  ├─ month, day_of_year
│  ├─ week_of_year
│  └─ quarter
│
├─ Trees (100 estimators)
│  ├─ Tree 1: Split on hour & temp
│  ├─ Tree 2: Split on volume & wind
│  ├─ Tree 3: Split on humidity & time
│  └─ ... (repetitive refinement)
│
└─ Output: Price (₹/MWh)
```

---

## 📁 File Dependencies

```
app.py (Main Application)
│
├── Imports:
│   ├─ streamlit (UI framework)
│   ├─ pandas, numpy (data processing)
│   ├─ plotly (visualization)
│   └─ joblib (model loading)
│
└── Runtime Dependencies:
    ├─ lgbm_model.joblib ← REQUIRED
    ├─ scaler.joblib     ← REQUIRED
    └─ example_batch_data.csv (for testing)
```

---

## 🌐 Deployment Architecture

### Local Development
```
Developer Machine
├─ Python 3.8+
├─ Virtual Environment
├─ Streamlit Server (port 8501)
└─ Web Browser (localhost:8501)
```

### Docker Container
```
Host Machine
│
└─ Docker Daemon
   │
   └─ Container (electricity-forecaster)
      ├─ Python 3.9
      ├─ All dependencies
      ├─ Streamlit Server (0.0.0.0:8501)
      └─ Models loaded
```

### Cloud Deployment
```
Cloud Provider (AWS/GCP/Azure)
│
├─ Load Balancer
│  │
│  ├─ Container Instance 1 (Streamlit)
│  ├─ Container Instance 2 (Streamlit)
│  └─ Container Instance 3 (Streamlit)
│
├─ Model Storage (S3/GCS)
│  ├─ lgbm_model.joblib
│  └─ scaler.joblib
│
└─ Database (Optional)
   └─ Prediction logs & history
```

---

## 🔄 Request-Response Cycle

### Single Prediction

```
1. USER INPUT
   └─ Click "Predict Price" button
   
2. STREAMLIT CAPTURES INPUT
   └─ All form values collected
   
3. VALIDATION
   └─ Check ranges, types, required fields
   
4. FEATURE ENGINEERING
   └─ Calculate derived features (temp², day_of_week, etc.)
   
5. FEATURE SCALING
   └─ Load scaler.joblib → Transform features
   
6. MODEL INFERENCE
   └─ Load lgbm_model.joblib → Generate prediction
   
7. INTERPRETATION
   └─ Categorize price → Generate trading signal
   
8. DISPLAY RESULT
   └─ Show price, range, interpretation, charts
   
9. USER SEES RESULT
   └─ Within 2-3 seconds
```

### Batch Prediction

```
1. USER UPLOADS CSV
   └─ File selected and uploaded
   
2. FILE READING
   └─ pandas.read_csv() → DataFrame loaded
   
3. VALIDATION
   └─ Check columns, data types, ranges
   
4. PREVIEW
   └─ Display first 10 rows to user
   
5. USER CLICKS PREDICT
   └─ Batch processing initiated
   
6. LOOP THROUGH ROWS
   For each row:
   ├─ Engineer features
   ├─ Scale features
   ├─ Get prediction
   └─ Store result
   
7. AGGREGATE RESULTS
   └─ Calculate statistics
   
8. GENERATE OUTPUTS
   ├─ Statistics table
   ├─ Results table
   ├─ Visualization chart
   └─ Download button
   
9. USER DOWNLOAD
   └─ CSV file with all predictions
```

---

## 💾 Data Storage

```
Session Memory (Temporary)
│
├─ Cached Models
│  ├─ @st.cache_resource
│  ├─ lgbm_model (24hr TTL)
│  └─ scaler (24hr TTL)
│
└─ Session Variables
   ├─ predictions
   ├─ input_data
   └─ visualization
   
Persistent Storage (Files)
│
├─ lgbm_model.joblib (4-10 MB)
├─ scaler.joblib (small <1MB)
├─ example_batch_data.csv (small <50KB)
└─ uploaded batch files (temporary)
```

---

## 🔌 Integration Points

```
External Integration Options
│
├─ Weather API Integration
│  └─ Fetch weather data → Use in app
│
├─ Market Data Integration
│  └─ Get live IEX data → Use in app
│
├─ Trading System Integration
│  └─ Export predictions → Execute trades
│
├─ Database Integration
│  └─ Log predictions → Track accuracy
│
└─ Dashboard Integration
   └─ Embed predictions → Monitoring dashboard
```

---

## 📊 Performance Characteristics

```
Single Prediction
├─ Input processing: ~50-100ms
├─ Model loading (cached): ~0ms
├─ Prediction: ~10-50ms
├─ Result formatting: ~50-100ms
└─ Total: ~150-300ms per prediction

Batch Prediction (1000 rows)
├─ File upload: ~1-2s
├─ Parsing & validation: ~1-2s
├─ Feature engineering (1000): ~2-3s
├─ Model predictions (1000): ~1-2s
├─ Result aggregation: ~1-2s
└─ Total: ~8-12 seconds

Visualization
├─ Chart generation: ~500-1000ms
└─ Total response: ~300-500ms
```

---

## 🔒 Security Layers

```
INPUT VALIDATION
│
├─ Type checking (int, float)
├─ Range verification (min/max)
├─ Required field checks
└─ SQL injection protection (N/A - no DB)

MODEL SECURITY
│
├─ Model integrity (joblib checksums)
├─ Scaler consistency (same training data)
└─ Version tracking

DEPLOYMENT SECURITY
│
├─ XSRF protection (configured)
├─ CORS restrictions (configured)
├─ SSL/TLS (with reverse proxy)
└─ Error message sanitization
```

---

## 🚀 Scalability Design

```
For Increased Load:

Horizontal Scaling
├─ Multiple Streamlit instances
├─ Load balancer (Nginx, AWS ELB)
├─ Shared model file storage (NFS, S3)
└─ Session persistence (Redis)

Vertical Scaling
├─ Increase CPU (more threads)
├─ Increase RAM (larger batches)
├─ Enable GPU acceleration
└─ Optimize model inference

Caching Strategy
├─ Model: 24-hour cache
├─ Scaler: 24-hour cache
├─ Results: Per-session cache
└─ Static files: Browser cache
```

---

## 📈 Prediction Pipeline Visualization

```
FEATURES (15 inputs)
│
├─ Weather (5): temp, temp², dwpt, rhum, wspd
├─ Market (4): volume, bid, schedule, lag_24h
└─ Time (6): hour, dow, month, doy, woy, qtr
│
↓ PREPROCESSING
│
├─ Feature Validation
├─ Default Imputation
├─ Type Conversion
└─ Feature Scaling
│
↓ ENCODING
│
├─ Numerical → Already scaled
├─ Categorical → As-is (LightGBM handles)
└─ Target → Price (₹/MWh)
│
↓ MODEL INFERENCE
│
└─ LightGBM Regressor
   ├─ 100 decision trees
   ├─ Each tree predicts diffs
   ├─ Sum predictions
   └─ Output: Final price
│
↓ POST-PROCESSING
│
├─ Clip to realistic range [500, 10000]
├─ Round to 2 decimals
├─ Categorize (Low/Mid/High/Scarcity)
└─ Generate signal
│
↓ DISPLAY
│
└─ ₹X,XXX/MWh with interpretation
```

---

## 🔄 Error Handling Flow

```
ERROR OCCURS
│
├─ Validation Error (Invalid Input)
│  └─ Show user-friendly message
│
├─ File Error (Bad CSV)
│  └─ Show parsing error details
│
├─ Model Error (Missing file)
│  └─ Show setup instructions
│
├─ Processing Error (OOM)
│  └─ Suggest splitting data
│
└─ Unexpected Error
   └─ Log error & show generic message
```

---

## 📊 Key Metrics Dashboard (Optional Future)

```
Could be added to Tab 3:

Metrics:
├─ Predictions Made (Today/Week/Month)
├─ Accuracy vs Actuals (if tracked)
├─ Average Price Predicted
├─ Price Range Distribution
├─ Most Common Trading Signal
└─ System Performance (response time)

Charts:
├─ Price time series
├─ Temperature vs Price correlation
├─ Accuracy over time
└─ Signal effectiveness
```

---

This architecture is designed for:
- ✅ **Reliability**: Fault tolerant, error handling
- ✅ **Performance**: Caching, optimization
- ✅ **Scalability**: Horizontal scaling support
- ✅ **Security**: Input validation, safe defaults
- ✅ **Maintainability**: Clear separation of concerns

---

**Last Updated:** March 2026
**Architecture Version:** 1.0
