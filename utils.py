import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Columns used in the notebook
NUMERICAL_COLS = ['Inventory Level', 'Units Sold', 'Units Ordered', 'Price', 'Discount', 'Competitor Pricing']
CAT_COLUMNS = ['Store ID', 'Product ID', 'Category', 'Region', 'Weather Condition', 'Seasonality']

def load_and_preprocess(csv_path='retail_store_inventory.csv'):
    """Load CSV, one-hot encode categorical columns (drop_first=True), scale numerical cols.
    Returns:
      df_reconstructed: DataFrame with scaled numerical cols and one-hot columns
      feature_columns: list of columns used as model input (exclude Date and Demand Forecast)
      scaler: fitted StandardScaler for numerical columns
      raw_means: dict of means of numerical columns in original scale
      scaled_means: dict of means of scaled numerical columns (should be ~0)
      category_options: dict mapping categorical column -> list of unique values (for UI)
    """
    df = pd.read_csv(csv_path)
    # Ensure Date is datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    # Save raw means for defaults
    raw_means = {}
    for col in NUMERICAL_COLS:
        raw_means[col] = float(df[col].mean()) if col in df.columns else 0.0

    # Keep category options from raw df for UI
    category_options = {}
    for c in CAT_COLUMNS:
        if c in df.columns:
            # convert to string for stable selectbox choices
            category_options[c] = sorted(df[c].astype(str).unique().tolist())
        else:
            category_options[c] = []

    # One-hot encode
    existing_cat_cols = [c for c in CAT_COLUMNS if c in df.columns]
    if existing_cat_cols:
        df_encoded = pd.get_dummies(df, columns=existing_cat_cols, drop_first=True)
    else:
        df_encoded = df.copy()

    # Scale numerical columns
    scaler = StandardScaler()
    present_numerical = [c for c in NUMERICAL_COLS if c in df_encoded.columns]
    if present_numerical:
        scaled_values = scaler.fit_transform(df_encoded[present_numerical])
        df_scaled = pd.DataFrame(scaled_values, columns=present_numerical, index=df_encoded.index)
    else:
        df_scaled = pd.DataFrame(index=df_encoded.index)

    # Reconstruct DataFrame: drop original numerical cols and concat scaled
    df_reconstructed = df_encoded.drop(columns=present_numerical, errors='ignore').reset_index(drop=True)
    if not df_scaled.empty:
        df_reconstructed = pd.concat([df_reconstructed, df_scaled.reset_index(drop=True)], axis=1)

    feature_columns = [c for c in df_reconstructed.columns if c not in ('Date', 'Demand Forecast')]

    # compute scaled means (should be near 0)
    scaled_means = {}
    for c in present_numerical:
        scaled_means[c] = float(df_scaled[c].mean())

    return df_reconstructed, feature_columns, scaler, raw_means, scaled_means, category_options, df


def get_knn_defaults(raw_df, categorical_inputs, n_neighbors=5):
    """Use KNN to find similar records in the raw data and return mean numerical values.
    
    Args:
      raw_df: raw dataframe with Date, Store ID, Product ID, etc.
      categorical_inputs: dict of {cat_col: chosen_value}
      n_neighbors: number of neighbors to average
      
    Returns:
      dict of numerical col -> mean value from similar records
    """
    if raw_df is None or raw_df.empty:
        return {}
    
    try:
        # Filter by exact categorical matches
        filtered_df = raw_df.copy()
        for cat_col, chosen in categorical_inputs.items():
            if chosen is not None and cat_col in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[cat_col] == chosen]
        
        if filtered_df.empty:
            # Fallback: if no exact match, use all data
            filtered_df = raw_df.copy()
        
        # Build KNN on numerical columns
        present_numerical = [c for c in NUMERICAL_COLS if c in filtered_df.columns]
        if not present_numerical:
            return {}
        
        X = filtered_df[present_numerical].values
        if X.shape[0] == 0:
            return {}
        
        n_neighbors = min(n_neighbors, X.shape[0])
        knn = NearestNeighbors(n_neighbors=n_neighbors)
        knn.fit(X)
        
        # Get the first neighbor (if X has 1 row, it will be itself)
        _, indices = knn.kneighbors(X[0:1])
        neighbors = filtered_df.iloc[indices[0]]
        
        # Return mean of neighbors
        knn_defaults = {}
        for col in present_numerical:
            knn_defaults[col] = float(neighbors[col].mean())
        
        return knn_defaults
    except Exception as e:
        print(f"KNN error: {e}")
        return {}


def build_input_row(feature_columns, category_options, scaler, raw_numeric_inputs, categorical_inputs, holiday):
    """Construct a single-row input (scaled) matching `feature_columns` order.

    - raw_numeric_inputs: dict of numerical column -> raw value (in original scale)
    - categorical_inputs: dict of categorical col -> chosen value (strings)
    - holiday: bool or int for Holiday/Promotion
    Returns a numpy array shaped (1, 1, num_features) ready for model.predict
    """
    # Initialize 0s
    input_data = {col: 0 for col in feature_columns}

    # Handle categorical columns: try to find matching one-hot column f"{col}_{value}"
    for cat_col, chosen in categorical_inputs.items():
        if chosen is None:
            continue
        candidate = f"{cat_col}_{chosen}"
        if candidate in input_data:
            input_data[candidate] = 1
        # If candidate not present, it is likely the dropped/base category -> leave zeros

    # Holiday/Promotion
    if 'Holiday/Promotion' in input_data:
        input_data['Holiday/Promotion'] = 1 if holiday else 0

    # Numeric: scale using scaler
    # Prepare in same order as scaler expects (NUMERICAL_COLS filtered to present)
    numeric_order = [c for c in NUMERICAL_COLS if c in feature_columns]
    if numeric_order:
        raw_vals = [float(raw_numeric_inputs.get(c, 0.0)) for c in numeric_order]
        scaled = scaler.transform([raw_vals])[0]
        for c, s in zip(numeric_order, scaled):
            input_data[c] = float(s)

    # Convert to array in feature_columns order
    arr = np.array([input_data[c] for c in feature_columns], dtype=np.float32)
    arr = arr.reshape(1, 1, -1)
    return arr
