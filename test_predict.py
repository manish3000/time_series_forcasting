from pathlib import Path
import numpy as np
import tensorflow as tf
from utils import load_and_preprocess, build_input_row

BASE = Path(__file__).parent
MODEL_PATH = BASE / 'model_lstm_100_100_1.keras'

def main():
    df_reconstructed, feature_columns, scaler, raw_means, scaled_means, category_options = load_and_preprocess(str(BASE / 'retail_store_inventory.csv'))

    print('Loaded preprocessing, number of features:', len(feature_columns))

    # Build a default input using raw_means and first available categorical choices
    categorical_inputs = {}
    for k, opts in category_options.items():
        categorical_inputs[k] = opts[0] if opts else None

    raw_numeric_inputs = {k: raw_means.get(k, 0.0) for k in ['Inventory Level', 'Units Sold', 'Units Ordered', 'Price', 'Discount', 'Competitor Pricing']}

    inp = build_input_row(feature_columns, category_options, scaler, raw_numeric_inputs, categorical_inputs, holiday=False)

    model = tf.keras.models.load_model(str(MODEL_PATH))
    pred = model.predict(inp)
    print('Predicted Demand Forecast:', float(pred.flatten()[0]))

if __name__ == '__main__':
    main()
