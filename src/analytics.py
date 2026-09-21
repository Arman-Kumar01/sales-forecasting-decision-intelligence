import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import joblib
from pathlib import Path

Path("models").mkdir(exist_ok=True)

def run_segmentation(df):
    snapshot = df['Order_Date'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('Customer_ID').agg({
        'Order_Date': lambda x: (snapshot - x.max()).days,
        'Order_ID': 'count',
        'Sales': 'sum'
    }).rename(columns={'Order_Date': 'Recency', 'Order_ID': 'Frequency', 'Sales': 'Monetary'})
    
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm)
    
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
    
    labels = ['Lost', 'At Risk', 'Loyal', 'Champions']
    rfm['Segment'] = pd.qcut(rfm['Monetary'], q=4, labels=labels)
    rfm.to_csv("data/processed/rfm_segments.csv")
    return rfm

def detect_anomalies(df):
    daily = df.groupby('Order_Date').agg({'Sales':'sum'}).reset_index()
    iso = IsolationForest(contamination=0.02, random_state=42)
    daily['Anomaly'] = iso.fit_predict(daily[['Sales']])
    daily.to_csv("data/processed/anomalies.csv", index=False)
    return daily

def run_forecasting(df):
    monthly = df.resample('ME', on='Order_Date')['Sales'].sum().reset_index()
    
    # Time Series Feature Engineering (Lags to prevent leakage)
    monthly['lag_1'] = monthly['Sales'].shift(1)
    monthly['lag_2'] = monthly['Sales'].shift(2)
    monthly['lag_12'] = monthly['Sales'].shift(12)
    monthly['rolling_mean_3'] = monthly['lag_1'].rolling(3).mean()
    monthly['month'] = monthly['Order_Date'].dt.month
    monthly.dropna(inplace=True)
    
    # Chronological Split (NEVER RANDOM)
    train = monthly.iloc[:-6]
    test = monthly.iloc[-6:]
    
    features = ['lag_1', 'lag_2', 'lag_12', 'rolling_mean_3', 'month']
    X_train, y_train = train[features], train['Sales']
    X_test, y_test = test[features], test['Sales']
    
    # Baseline: Naive
    naive_mae = mean_absolute_error(y_test, test['lag_1'])
    
    # ML Model: Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    
    metrics = {
        'MAE': mean_absolute_error(y_test, rf_preds),
        'RMSE': np.sqrt(mean_squared_error(y_test, rf_preds)),
        'MAPE': mean_absolute_percentage_error(y_test, rf_preds) * 100
    }
    
    test_results = pd.DataFrame({'Date': test['Order_Date'], 'Actual': y_test, 'Predicted': rf_preds})
    test_results.to_csv("data/processed/forecast_results.csv", index=False)
    
    joblib.dump(rf, 'models/rf_forecaster.joblib')
    return metrics
