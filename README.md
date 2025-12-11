# Retail Demand Forecast Streamlit App

This workspace contains a Streamlit application that loads a pre-trained LSTM model and predicts retail demand ("Demand Forecast") from user inputs.

Files added:
- `app.py` : Streamlit dashboard
- `utils.py`: Data loading and preprocessing helpers (recreates notebook preprocessing)
- `requirements.txt`: Python dependencies
- `test_predict.py`: small script to verify model load and prediction

How to run:

1. (Optional) Create a virtual environment and activate it.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the Streamlit app:

```powershell
streamlit run app.py
```

Notes:
- The app expects `retail_store_inventory.csv` and `model_lstm_100_100_1.keras` to be in the workspace root (same folder as `app.py`).
- The preprocessing mirrors `final preprocess_and_LSTM.ipynb` (one-hot encoding with `drop_first=True` and StandardScaler on numerical columns).
