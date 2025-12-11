import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from utils import load_and_preprocess, build_input_row, get_knn_defaults

BASE = Path(__file__).parent
MODEL_PATH = BASE / 'model_lstm_100_100_1.keras'


@st.cache_resource
def load_model(path):
    try:
        return tf.keras.models.load_model(path)
    except Exception as e:
        st.error(f"Could not load model: {e}")
        return None


@st.cache_data
def prepare_data():
    df_reconstructed, feature_columns, scaler, raw_means, scaled_means, category_options, raw_df = load_and_preprocess(str(BASE / 'retail_store_inventory.csv'))
    return df_reconstructed, feature_columns, scaler, raw_means, scaled_means, category_options, raw_df


def main():
    st.title('Retail Demand Forecast (LSTM)')
    st.markdown('Provide input values and press **Predict** to get a demand forecast')

    df_reconstructed, feature_columns, scaler, raw_means, scaled_means, category_options, raw_df = prepare_data()

    model = load_model(MODEL_PATH)
    if model is None:
        st.warning('Model not loaded. Place `model_lstm_100_100_1.keras` in the workspace root.')

    # Inputs
    st.sidebar.header('Prediction Inputs')
    date = st.sidebar.date_input('Date')

    categorical_inputs = {}
    for cat in ['Store ID', 'Product ID', 'Category', 'Region', 'Weather Condition', 'Seasonality']:
        options = category_options.get(cat, [])
        if options:
            choice = st.sidebar.selectbox(cat, options)
        else:
            choice = None
        categorical_inputs[cat] = str(choice) if choice is not None else None

    # Get KNN-based defaults based on categorical selections (n=5)
    knn_defaults = get_knn_defaults(raw_df, categorical_inputs, n_neighbors=5)
    
    # Automatically use KNN defaults for numerical values
    raw_numeric_inputs = {}
    for num in ['Inventory Level', 'Units Sold', 'Units Ordered', 'Price', 'Discount', 'Competitor Pricing']:
        raw_numeric_inputs[num] = knn_defaults.get(num) or raw_means.get(num, 0.0)

    holiday = st.sidebar.checkbox('Holiday/Promotion', value=False)

    if st.sidebar.button('Predict'):
        if model is None:
            st.error('Model not available — cannot predict.')
            return

        # Build input
        inp = build_input_row(feature_columns, category_options, scaler, raw_numeric_inputs, categorical_inputs, holiday)

        # Predict
        pred = model.predict(inp)
        pred_value = float(pred.flatten()[0])

        st.success(f'Predicted Demand Forecast: {pred_value:.2f}')
        
        # Summary section
        st.subheader('📊 Forecast Summary')
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Predicted Demand", value=f"{pred_value:.2f}")
        
        with col2:
            # Calculate mean actual demand from data
            mean_actual = float(df_reconstructed['Demand Forecast'].mean())
            st.metric(label="Mean Actual Demand", value=f"{mean_actual:.2f}")
        
        with col3:
            # Calculate variance from actual
            actual_std = float(df_reconstructed['Demand Forecast'].std())
            st.metric(label="Demand Std Dev", value=f"{actual_std:.2f}")
        
        # Model info
        st.info(f"""
        **Model Information:**
        - **Architecture**: LSTM (100 units) + Dense (100 units) + Output Dense (1 unit)
        - **Training**: 10 epochs with validation split
        - **Loss Function**: Mean Squared Error (MSE)
        - **Optimizer**: Adam
        - **Input Features**: {len(feature_columns)} features (one-hot encoded categories + scaled numerical)
        
        **Prediction Context:**
        - This forecast is based on {len(feature_columns)} input features derived from categorical and numerical data
        - KNN (n=5) was used to select similar historical records for numerical feature values
        - The prediction is scaled from the model's output
        """)
        

        st.write('---')
        st.subheader('📝 Input Parameters Used')
        st.write('**Date:**', date)
        st.write('**Categorical inputs:**', {k: v for k, v in categorical_inputs.items() if v})
        st.write('**Numeric inputs (auto-computed via KNN, n=5):**')
        for k, v in raw_numeric_inputs.items():
            st.write(f"  - {k}: {v:.2f}")
        st.write('**Holiday/Promotion:**', '✓ Yes' if holiday else '✗ No')

        # Show prediction comparison graph
        st.subheader('Actual vs Predicted Forecast (Sample)')
        try:
            # Generate predictions on a sample of test set
            X_sample = df_reconstructed.drop(columns=['Date', 'Demand Forecast']).values.astype(np.float32)
            X_sample = X_sample.reshape(X_sample.shape[0], 1, X_sample.shape[1])
            y_actual = df_reconstructed['Demand Forecast'].values
            
            # Predict on sample (first 200 records)
            sample_size = min(200, len(y_actual))
            y_pred_sample = model.predict(X_sample[:sample_size])
            y_pred_sample = y_pred_sample.flatten()

            # Scatter plot
            fig2, ax2 = plt.subplots(figsize=(8, 8))
            ax2.scatter(y_actual[:sample_size], y_pred_sample, alpha=0.5, s=20)
            # Perfect prediction line
            min_val = min(y_actual[:sample_size].min(), y_pred_sample.min())
            max_val = max(y_actual[:sample_size].max(), y_pred_sample.max())
            ax2.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
            ax2.set_xlabel('Actual Demand Forecast')
            ax2.set_ylabel('Predicted Demand Forecast')
            ax2.set_title('Scatter: Actual vs Predicted')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)
        except Exception as e:
            st.error(f"Could not generate graphs: {e}")


if __name__ == '__main__':
    main()
