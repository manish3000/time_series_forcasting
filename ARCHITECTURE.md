# 📐 Architecture & System Design

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (Streamlit)                   │
│                     app.py (532 lines)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  HEADER & NAVIGATION                                       │ │
│  │  ┌─ 📊 Title                                              │ │
│  │  ├─ 🏠 Navigation Menu                                     │ │
│  │  └─ ⚙️ Sidebar Configuration                               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─ SIDEBAR (33%) ─────────────┐ ┌─ MAIN (67%) ─────────────┐  │
│  │                             │ │                           │  │
│  │  ⚙️ CONFIGURATION PANEL     │ │  📈 METRICS DASHBOARD    │  │
│  │  ├─ Product ID Selector    │ │  ├─ 5 KPI Cards         │  │
│  │  ├─ Forecast Days Slider   │ │  │                       │  │
│  │  ├─ Lookback Window        │ │  └─ Product Info        │  │
│  │  ├─ Lead Time Slider       │ │                           │  │
│  │  ├─ Min Stock Input        │ │  🔮 FORECASTING PANEL   │  │
│  │  └─ Action Buttons         │ │  ├─ Tab 1: Historical   │  │
│  │                             │ │  │   & Forecast         │  │
│  │  🚚 REORDER ENGINE         │ │  ├─ Tab 2: Error        │  │
│  │  ├─ Urgency Indicator 🔴   │ │  │   Analysis           │  │
│  │  ├─ Reorder Metrics (4)    │ │  ├─ Tab 3: Moving       │  │
│  │  ├─ Qty & Cost             │ │  │   Averages           │  │
│  │  └─ Confirm Button         │ │  ├─ Tab 4: Seasonality  │  │
│  │                             │ │  │   & Trend           │  │
│  └─────────────────────────────┘ │  ├─ Tab 5: Metrics     │  │
│                                   │  └─ Tab 6: CSV Export  │  │
│                                   └─────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓↑
                    ┌──────────────────┐
                    │  DATA PROCESSING │
                    └──────────────────┘
                              ↓↑
         ┌────────────────────────────────────────┐
         │   CORE COMPUTATION ENGINES             │
         ├────────────────────────────────────────┤
         │                                        │
         │  1. DATA LOADING & CACHING            │
         │     @st.cache_data                   │
         │     └─ Load CSV                      │
         │     └─ Parse Date                    │
         │     └─ Sort by Date                  │
         │                                        │
         │  2. LSTM FORECASTING ENGINE           │
         │     train_lstm_forecast()            │
         │     ├─ Normalize data                │
         │     ├─ Create sequences             │
         │     ├─ Train/test split             │
         │     ├─ Model prediction             │
         │     └─ Calculate metrics            │
         │                                        │
         │  3. FORECAST GENERATION              │
         │     generate_forecasts()            │
         │     ├─ Autoregressive loop          │
         │     ├─ Sequence update              │
         │     ├─ Inverse transform            │
         │     └─ Multi-horizon output         │
         │                                        │
         │  4. REORDER ENGINE                   │
         │     calculate_reorder()             │
         │     ├─ Calculate safety stock       │
         │     ├─ Calculate reorder point      │
         │     ├─ Suggest order quantity       │
         │     ├─ Determine urgency            │
         │     └─ Estimate cost                │
         │                                        │
         │  5. ANALYSIS FUNCTIONS               │
         │     ├─ Moving averages              │
         │     ├─ Trend analysis               │
         │     ├─ Seasonality                  │
         │     └─ Error metrics                │
         │                                        │
         └────────────────────────────────────────┘
                              ↓↑
         ┌────────────────────────────────────────┐
         │   MODEL & DATA RESOURCES               │
         ├────────────────────────────────────────┤
         │                                        │
         │  🧠 LSTM MODEL (Pre-trained)         │
         │  model_lstm_100_100_1.keras          │
         │  ├─ LSTM Layer 1: 100 units         │
         │  ├─ LSTM Layer 2: 100 units         │
         │  ├─ Dense: 100 units                │
         │  └─ Output: 1 unit                  │
         │                                        │
         │  📊 DATA (CSV)                       │
         │  retail_store_inventory.csv          │
         │  ├─ Date                            │
         │  ├─ Product ID                      │
         │  ├─ Inventory Level                 │
         │  ├─ Units Sold                      │
         │  ├─ Demand Forecast                 │
         │  ├─ Price                           │
         │  └─ ... (10+ features)              │
         │                                        │
         └────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
USER INTERACTION
       ↓
┌─────────────────────────────────────┐
│  SELECT PRODUCT ID from dropdown    │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  FILTER DATA for selected product   │
│  df[df['Product ID'] == selected]   │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  PREPARE TIME SERIES DATA           │
│  - Sort by Date                     │
│  - Extract features (Sales, Price)  │
│  - Define last_date & future_dates  │
└────────────┬────────────────────────┘
             ↓
        ┌────┴─────┐
        ↓          ↓
    ┌───────┐  ┌──────────────┐
    │TRAIN  │  │REORDER ENGINE│
    │LSTM   │  │(Runs in      │
    └───┬───┘  │parallel)     │
        ↓      └──────────────┘
  ┌──────────┐        ↓
  │NORMALIZE │   ┌─────────────┐
  │SEQUENCES │   │Calculate    │
  │SPLIT 80  │   │- Daily Avg  │
  │PREDICT   │   │- Safety Stk │
  │METRICS   │   │- Reorder Pt │
  └────┬─────┘   │- Qty & Cost │
       ↓         │- Urgency    │
  ┌─────────┐    └─────────────┘
  │FORECAST │        ↓
  │7, 14, 30│   ┌──────────────┐
  │days     │   │REORDER PANEL │
  └────┬────┘   │Display in UI │
       ↓        └──────────────┘
  ┌──────────────┐
  │VISUALIZATIONS│
  │- 6 Tabs     │
  │- Charts     │
  │- Tables     │
  │- Metrics    │
  └──────────────┘
       ↓
  ┌──────────────┐
  │CSV EXPORT    │
  │& DOWNLOAD    │
  └──────────────┘
```

---

## LSTM Processing Pipeline

```
INPUT: Product Historical Data (Units Sold)
       ├─ 365 days of sales history
       ├─ Values: [45, 52, 48, ...]
       └─ Length: Variable per product

STEP 1: NORMALIZATION
       ├─ StandardScaler().fit_transform()
       ├─ Mean: 50 → 0
       ├─ Std: 10 → 1
       └─ Scaled: [-0.5, 0.2, -0.2, ...]

STEP 2: CREATE SEQUENCES (Lookback = 10)
       ├─ Window 1: [45, 52, 48, 50, 49, 51, 47, 50, 52, 48] → 50
       ├─ Window 2: [52, 48, 50, 49, 51, 47, 50, 52, 48, 49] → 51
       ├─ Window 3: [48, 50, 49, 51, 47, 50, 52, 48, 49, 50] → 52
       └─ ... (repeat for all data)

STEP 3: SPLIT DATA (80% train, 20% test)
       ├─ Training set: 292 sequences
       ├─ Test set: 73 sequences
       └─ Input shape: (sequence, 10, 1)

STEP 4: PASS THROUGH LSTM
       ├─ LSTM Layer 1: 100 units
       │  └─ Output: 100 features
       ├─ LSTM Layer 2: 100 units
       │  └─ Output: 100 features
       ├─ Dense: 100 units, ReLU
       │  └─ Output: 100 features
       └─ Output: 1 unit
          └─ Predicted demand

STEP 5: CALCULATE METRICS
       ├─ MAE = 2.5 units
       ├─ MSE = 8.2 units²
       ├─ RMSE = 2.86 units
       └─ R² = 0.78

STEP 6: GENERATE FUTURE FORECAST
       ├─ Start: Last 10 days
       ├─ Loop 30 times:
       │  ├─ Predict next day
       │  ├─ Add to sequence
       │  └─ Remove first day
       └─ Output: [48.2, 51.5, 50.1, ..., 49.7]

STEP 7: INVERSE TRANSFORM
       ├─ Undo normalization
       ├─ Scaled: [48.2, 51.5, ...] → Original scale
       └─ Output: [48, 52, 50, ...]

OUTPUT: 7-day, 14-day, 30-day forecasts ready for display
```

---

## Reorder Engine Logic Diagram

```
INPUT: Product Data + Forecast
       ├─ Current Inventory: 250 units
       ├─ Units Sold (historical): [45, 52, 48, ...]
       ├─ 14-day Forecast: [48, 52, 50, ...]
       ├─ Product Price: $10/unit
       └─ Lead Time: 7 days

STEP 1: CALCULATE DAILY AVERAGE
       Daily_Avg = Mean(historical sales)
       = (45+52+48+...)/365 = 50 units/day

STEP 2: CALCULATE SAFETY STOCK
       Safety_Stock = Daily_Avg × 2
       = 50 × 2 = 100 units
       (Configurable: can be 1.5× or 3×)

STEP 3: CALCULATE REORDER POINT
       Reorder_Point = (Daily_Avg × Lead_Time) + Safety_Stock
       = (50 × 7) + 100 = 450 units
       (When inventory drops to 450, trigger order)

STEP 4: FORECAST DEMAND FOR 14 DAYS
       Forecast_14D = Sum([48, 52, 50, ...]) = 700 units

STEP 5: CALCULATE REORDER QUANTITY
       Reorder_Qty = MAX(Forecast_14D × 1.5, 50)
       = MAX(700 × 1.5, 50) = 1,050 units

STEP 6: ESTIMATE COST
       Est_Cost = Reorder_Qty × Price
       = 1,050 × $10 = $10,500

STEP 7: DETERMINE URGENCY
       IF Current_Inv < Reorder_Point × 0.5:
           Status = 🔴 CRITICAL
       ELIF Current_Inv < Reorder_Point:
           Status = 🟡 HIGH
       ELIF Current_Inv < Reorder_Point × 1.5:
           Status = 🟢 MEDIUM
       ELSE:
           Status = 🟢 LOW

STEP 8: DISPLAY RECOMMENDATION
       ├─ Current: 250 units
       ├─ Reorder Point: 450 units
       ├─ Status: 🟡 HIGH (250 < 450)
       ├─ Recommended Qty: 1,050 units
       ├─ Estimated Cost: $10,500
       └─ Action: "Order Within 2-3 Days"

OUTPUT: Actionable reorder recommendation
```

---

## UI Component Hierarchy

```
Streamlit App
│
├─ Page Config
│  ├─ Title: "📊 Sales Forecasting Dashboard"
│  ├─ Icon: 📊
│  └─ Layout: wide
│
├─ CSS Styling
│  ├─ .metric-card
│  ├─ .highlight-success
│  └─ .highlight-warning
│
├─ SIDEBAR
│  ├─ Title: "⚙️ Configuration"
│  ├─ Product Selector
│  │  └─ st.selectbox() with all Product IDs
│  ├─ Forecast Settings
│  │  ├─ Days Slider (7-90)
│  │  └─ Lookback Slider (5-30)
│  ├─ Reorder Settings
│  │  ├─ Min Stock Input
│  │  └─ Lead Time Slider (1-14)
│  └─ Action Buttons
│     ├─ Retrain Model
│     └─ Download CSV
│
├─ MAIN CONTENT
│  ├─ Header
│  │  ├─ Title
│  │  └─ Subtitle
│  ├─ Metrics Bar (5 KPIs)
│  │  ├─ Product ID
│  │  ├─ Category
│  │  ├─ Current Inventory
│  │  ├─ Current Price
│  │  └─ Avg Daily Sales
│  ├─ Divider
│  ├─ Two Column Layout
│  │  ├─ LEFT (2/3): Forecasting
│  │  │  ├─ Title: "🔮 Demand Forecasting"
│  │  │  └─ Tabs (6)
│  │  │     ├─ Tab 1: Historical Chart
│  │  │     │  └─ matplotlib Figure
│  │  │     ├─ Tab 2: Error Analysis
│  │  │     │  ├─ Histogram
│  │  │     │  └─ Scatter Plot
│  │  │     ├─ Tab 3: Moving Averages
│  │  │     │  └─ Line Chart (7-day, 30-day)
│  │  │     ├─ Tab 4: Seasonality & Trend
│  │  │     │  ├─ Bar Chart (Monthly)
│  │  │     │  └─ Trend Line
│  │  │     ├─ Tab 5: Performance Metrics
│  │  │     │  ├─ 4 Metric Cards
│  │  │     │  └─ Loss Curves Chart
│  │  │     └─ Tab 6: CSV Export
│  │  │        ├─ Download Button
│  │  │        └─ Data Table
│  │  │
│  │  └─ RIGHT (1/3): Reorder Engine
│  │     ├─ Title: "🚚 Reorder Engine"
│  │     ├─ Urgency Indicator (4 levels)
│  │     ├─ Divider
│  │     ├─ Reorder Metrics (4 KPIs)
│  │     ├─ Divider
│  │     ├─ Recommendation
│  │     │  ├─ Order Quantity Metric
│  │     │  └─ Cost Metric
│  │     └─ Action Button
│  │        └─ Confirm Reorder
│  │
│  └─ Footer
│     └─ Version & Timestamp
│
└─ State Management
   ├─ @st.cache_resource: Model
   ├─ @st.cache_data: Data
   └─ Session State (for user inputs)
```

---

## Data Structures

### Product Data Frame
```python
DataFrame: retail_store_inventory.csv
│
├─ Date (datetime64)
├─ Store ID (object: S001, S002, ...)
├─ Product ID (object: P0001, P0002, ...)
├─ Category (object: Groceries, Toys, ...)
├─ Region (object: North, South, ...)
├─ Inventory Level (float64)
├─ Units Sold (float64)
├─ Units Ordered (float64)
├─ Demand Forecast (float64) ← Target for LSTM
├─ Price (float64)
├─ Discount (float64)
├─ Weather Condition (object)
├─ Holiday/Promotion (int64)
├─ Competitor Pricing (float64)
└─ Seasonality (object: Autumn, Winter, ...)
```

### Forecast Results Dictionary
```python
forecast_results = {
    'y_train': array([45, 52, 48, ...]),      # Training actual
    'y_train_pred': array([46, 51, 49, ...]),  # Training predicted
    'y_test': array([50, 52, 48, ...]),        # Test actual
    'y_test_pred': array([49, 53, 47, ...]),   # Test predicted
    'mae': 2.5,                                # Mean Absolute Error
    'mse': 8.2,                                # Mean Squared Error
    'rmse': 2.86,                              # Root MSE
    'r2': 0.78,                                # R² Score
    'scaler_demand': StandardScaler(),         # For inverse transform
    'scaler_sales': StandardScaler()           # For inverse transform
}
```

### Forecast Output Dictionary
```python
future_forecasts = {
    '7': array([48.2, 51.5, 50.1, 49.8, 52.3, 50.9, 49.7]),
    '14': array([...14 values...]),
    '30': array([...30 values...])
}
```

### Reorder Information Dictionary
```python
reorder_info = {
    'current_inventory': 250.0,       # Current stock
    'reorder_point': 450.0,           # Trigger point
    'reorder_quantity': 1050.0,       # How much to order
    'urgency': "🟡 HIGH - Order Within 2-3 Days",
    'color': "orange",
    'estimated_cost': 10500.0,        # Total order cost
    'safety_stock': 100.0,            # Buffer inventory
    'daily_avg': 50.0                 # Average daily sales
}
```

---

## File Size & Complexity

| File | Lines | Purpose | Complexity |
|------|-------|---------|------------|
| app.py | 532 | Main dashboard | 🔴 High |
| utils.py | 160 | Utilities | 🟡 Medium |
| model_lstm | N/A | Neural Network | 🔴 High |
| retail_store_inventory.csv | ~1000+ | Data | 🟡 Medium |

---

## Dependencies & Versions

```
streamlit >= 1.28.0    # Web framework
tensorflow >= 2.13.0   # LSTM model
pandas >= 1.5.0        # Data manipulation
numpy >= 1.24.0        # Numerical computing
scikit-learn >= 1.3.0  # ML utilities (StandardScaler)
matplotlib >= 3.7.0    # Plotting
seaborn >= 0.12.0      # Statistical plots
```

---

## Performance Characteristics

```
Model Inference: 100-200ms per prediction
Memory Usage: ~500MB for full dataset
Concurrent Users: Recommended max 5 (Streamlit Cloud limit)
Data Processing: < 1s (cached)
Chart Rendering: < 500ms per chart
Reorder Calculation: < 50ms
Full Page Load: 2-3 seconds (initial)
```

---

## Security & Data Flow

```
User Browser (Local)
     ↓
Streamlit Server (Local or Cloud)
     ↓
Python Runtime
     ├─ Load CSV (memory)
     ├─ Train LSTM (RAM)
     ├─ Generate Forecasts (RAM)
     └─ Calculate Reorder (RAM)
     ↓
Display Results (browser)
     ↓
Export CSV (download to user)

⚠️ No data leaves the machine (Local) or server (Cloud)
✅ All processing on server side
✅ No external API calls
✅ No tracking/analytics
```

---

This architecture provides:
- ✅ Scalability
- ✅ Performance
- ✅ User Experience
- ✅ Data Security
- ✅ Maintainability
