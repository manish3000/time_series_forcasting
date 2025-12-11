# 🚀 Sales Forecasting Dashboard - QUICK START GUIDE

## What You Just Got

A **production-ready Streamlit dashboard** with:
- ✅ LSTM-based demand forecasting
- ✅ 6 interactive visualization tabs
- ✅ Intelligent reorder engine
- ✅ Real-time inventory optimization
- ✅ Model performance metrics (MAE, MSE, RMSE, R²)
- ✅ CSV export functionality

---

## 📋 Installation (5 minutes)

### Step 1: Install Dependencies
Open PowerShell in your project directory and run:

```powershell
pip install -r requirements.txt
```

Or if you prefer manual installation:
```powershell
pip install streamlit tensorflow pandas numpy scikit-learn matplotlib seaborn
```

### Step 2: Verify Your Files
Make sure you have:
- ✅ `app.py` (the dashboard)
- ✅ `model_lstm_100_100_1.keras` (pre-trained model)
- ✅ `retail_store_inventory.csv` (your data)

---

## 🎯 Running the Dashboard (1 command)

```powershell
streamlit run app.py
```

The dashboard will automatically open in your browser at:
```
http://localhost:8501
```

---

## 📊 Dashboard Features Overview

### 1. **Sidebar Configuration Panel**
- 🏭 **Product ID Selector**: Choose any product from your dataset
- 📅 **Forecast Days**: Predict 7-90 days ahead
- 🔍 **LSTM Lookback Window**: Historical window size (5-30 days)
- ⏱️ **Lead Time**: Days to receive new order
- 📦 **Minimum Stock Level**: Safety threshold

### 2. **Top Metrics Dashboard**
Real-time KPIs showing:
- Current Product ID & Category
- Current Inventory Level
- Unit Price
- Average Daily Sales

### 3. **Main Forecasting Panel** (6 Tabs)

#### 📊 Tab 1: Historical & Forecast Chart
- Historical sales over time
- LSTM-generated 30-day forecast
- Interactive line chart with legend

#### 📉 Tab 2: Error Analysis
- Error distribution histogram
- Actual vs Predicted scatter plot
- Mean error calculation

#### 📈 Tab 3: Moving Averages
- 7-day MA (short-term trend)
- 30-day MA (long-term trend)
- Shaded area between MAs

#### 🌊 Tab 4: Seasonality & Trend
- Monthly seasonality patterns
- Polynomial trend fitting (2nd degree)
- Seasonal decomposition

#### 📋 Tab 5: Model Metrics
- **MAE**: Mean Absolute Error
- **MSE**: Mean Squared Error
- **RMSE**: Root Mean Squared Error
- **R² Score**: Goodness of fit (0-1)
- Train vs Validation loss curves

#### 💾 Tab 6: Data Export
- Download forecast as CSV
- 7-day, 14-day, 30-day forecasts
- Date-stamped filename

### 4. **Reorder Engine Panel** (Right Sidebar)

#### Urgency Status
- 🔴 **CRITICAL**: < 50% of reorder point
- 🟡 **HIGH**: < Reorder point
- 🟢 **MEDIUM**: < 150% of reorder point
- 🟢 **LOW**: Stock adequate

#### Metrics Displayed
- Current Inventory Level
- Reorder Point
- Daily Average Sales
- Safety Stock Buffer
- Recommended Order Quantity
- Estimated Order Cost
- One-click Reorder Confirmation

---

## 💡 How the Reorder Engine Works

### Calculation Logic

```
Daily Average Sales = Mean of historical sales

Safety Stock = Daily Average × 2
  (Buffer to prevent stockouts)

Reorder Point = (Daily Avg × Lead Time) + Safety Stock
  (Triggers reordering)

Reorder Quantity = MAX(14-Day Forecast × 1.5, 50 units)
  (How much to order)

Estimated Cost = Reorder Quantity × Current Price
```

### Example Scenario

```
Daily Sales Average: 50 units/day
Lead Time: 7 days
Current Price: $10/unit
Current Inventory: 250 units

Calculations:
Safety Stock = 50 × 2 = 100 units
Reorder Point = (50 × 7) + 100 = 450 units
14-Day Forecast = 700 units
Reorder Quantity = MAX(700 × 1.5, 50) = 1,050 units
Estimated Cost = 1,050 × $10 = $10,500

Status: 🟢 LOW (250 > 450 × 1.5, so not urgent)
```

---

## 📈 Understanding the Metrics

### Forecast Accuracy (Lower is Better)

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **MAE** | Average of \|Actual - Predicted\| | Average prediction error |
| **MSE** | Average of (Actual - Predicted)² | Penalizes large errors |
| **RMSE** | √(MSE) | Same units as forecast |
| **R²** | Variance explained / Total variance | 0-1 scale (1.0 = perfect) |

### Good Model Performance
- MAE < 10% of mean actual value
- R² > 0.7
- Low error variance in histogram

---

## 🔧 Common Customizations

### Change Reorder Safety Multiplier
In `app.py`, find `calculate_reorder_suggestions()` function:

```python
# Current: safety_stock = daily_avg * 2
# More conservative: daily_avg * 3
# Less conservative: daily_avg * 1.5
safety_stock = daily_avg * 2.5  # Change this number
```

### Change Default Lead Time
In `app.py`, find the sidebar section:

```python
# Current: 7 days default
lead_time = st.sidebar.slider("Lead Time (days)", 1, 14, 7)
# Change 7 to your default, e.g., 5 days:
lead_time = st.sidebar.slider("Lead Time (days)", 1, 14, 5)
```

### Change Forecast Days Range
In `app.py`:

```python
# Current: 7-90 days
forecast_days = st.sidebar.slider("Days to Forecast", 7, 90, 30)
# For longer horizons:
forecast_days = st.sidebar.slider("Days to Forecast", 7, 180, 30)
```

---

## 🐛 Troubleshooting

### "Model not found" Error
```
Solution: Ensure 'model_lstm_100_100_1.keras' is in the same 
directory as app.py
```

### "No data found for Product ID"
```
Solution: The product may not exist in your CSV.
Check what products are available by viewing the dropdown.
```

### Streamlit is slow
```
Solutions:
1. Reduce forecast days (use 7 or 14 instead of 90)
2. Reduce lookback window (use 5-10 instead of 30)
3. Press 'R' to clear Streamlit cache
```

### Charts not displaying
```
Solution: 
1. Menu → Settings → Clear Cache
2. Refresh browser
3. Restart: Ctrl+C, then 'streamlit run app.py'
```

### CSV Download Not Working
```
Solution: Check browser download settings and permissions
```

---

## 📊 Sample Workflow

1. **Launch Dashboard**
   ```powershell
   streamlit run app.py
   ```

2. **Select a Product**
   - Choose from dropdown (e.g., P0001)

3. **Configure Settings**
   - Set forecast days to 30
   - Set lead time to your typical order lead time
   - Adjust minimum stock if needed

4. **Analyze Forecasts**
   - View all 6 tabs
   - Check which metrics are good/bad
   - Review error distribution

5. **Review Reorder Status**
   - Check urgency indicator
   - Review recommended quantity and cost
   - Click "Confirm Reorder" if ready

6. **Export Data**
   - Download CSV for reporting
   - Use for supply chain planning

---

## 📱 Dashboard Layout

```
┌─────────────────────────────────────────────┐
│  📊 Sales Forecasting Dashboard             │
│  LSTM-based Demand Forecasting              │
│  & Intelligent Reorder Engine               │
└─────────────────────────────────────────────┘

┌──────────────────┐  ┌─────────────────────┐
│                  │  │                     │
│  SIDEBAR         │  │  MAIN CONTENT       │
│ ⚙️ Configuration  │  │ 📈 Metrics         │
│ • Product ID     │  │ 📊 6 Tabs          │
│ • Forecast Days  │  │ • Forecast Chart   │
│ • Lookback       │  │ • Error Analysis   │
│ • Lead Time      │  │ • Moving Avgs      │
│ • Min Stock      │  │ • Seasonality      │
│ • Actions        │  │ • Metrics          │
│                  │  │ • CSV Export       │
│  🚚 REORDER      │  │                    │
│  • Urgency       │  │                    │
│  • Metrics       │  │                    │
│  • Order Qty     │  │                    │
│  • Cost          │  │                    │
│  • Confirm Btn   │  │                    │
│                  │  │                    │
└──────────────────┘  └─────────────────────┘
```

---

## 🎓 Key Concepts

### LSTM (Long Short-Term Memory)
- Neural network architecture for time series
- Remembers long-term dependencies
- Better than traditional models for demand forecasting

### Lookback Window
- How many historical days to use for prediction
- Higher = more context but slower
- Typical: 7-14 days

### Lead Time
- Days between order placement and receipt
- Affects reorder point calculation
- Typical: 3-14 days for retail

### Safety Stock
- Extra inventory to prevent stockouts
- Protects against demand spikes
- Formula: Daily Average × 2 (adjustable)

---

## 📚 Next Steps

1. **Test with Different Products**
   - Try forecasting 5-10 products
   - Compare their metrics

2. **Optimize Parameters**
   - Find best lookback window
   - Tune safety stock multiplier

3. **Integrate with Systems**
   - Export forecasts to CSV
   - Import into ERP/inventory system

4. **Monitor Performance**
   - Track forecast accuracy over time
   - Adjust model if needed

---

## 📞 Support

For issues:
1. Check README_DASHBOARD.md for detailed documentation
2. Review troubleshooting section above
3. Verify all required files are present
4. Check Python/library versions

---

## 📝 Version Info

- **Version**: 1.0.0
- **Status**: Production Ready ✅
- **Last Updated**: December 2025
- **Python**: 3.8+
- **Key Libraries**: Streamlit, TensorFlow, Pandas, Scikit-learn

---

## ✨ What Makes This Dashboard Special

✅ **Intelligent Reorder Engine** - Not just forecasts, but actionable recommendations
✅ **6 Comprehensive Views** - Multiple angles on your data
✅ **Real-time Calculations** - Updates instantly with selections
✅ **Production Quality** - Clean UI, professional styling
✅ **No External API** - Everything runs locally
✅ **Easy Configuration** - Sidebar sliders for parameters
✅ **Exportable** - Download forecasts as CSV
✅ **Performance Metrics** - Understand model accuracy

---

**Happy Forecasting! 🎉**
