import pandas as pd
import numpy as np
from datetime import timedelta

def generate_synthetic_data(rows=10000, start_date='2020-01-01', output_path='data/raw/sales.csv'):
    np.random.seed(42)
    dates = pd.date_range(start=start_date, periods=1460, freq='D')
    order_dates = np.random.choice(dates, rows)
    
    # Introduce seasonality: More sales in Q4 (Nov, Dec)
    q4_boost = pd.Series(order_dates).dt.month.isin([11, 12])
    order_dates = np.append(order_dates, np.random.choice(dates[dates.month.isin([11, 12])], int(rows*0.2)))
    
    rows = len(order_dates)
    categories = ['Technology', 'Furniture', 'Office Supplies']
    regions = ['North', 'South', 'East', 'West']
    
    df = pd.DataFrame({
        'Order_ID': [f"ORD-{i:06d}" for i in range(1, rows + 1)],
        'Order_Date': order_dates,
        'Customer_ID': np.random.randint(1000, 1500, rows).astype(str),
        'Product_ID': np.random.randint(200, 250, rows).astype(str),
        'Category': np.random.choice(categories, rows, p=[0.3, 0.2, 0.5]),
        'Region': np.random.choice(regions, rows),
        'Quantity': np.random.randint(1, 10, rows),
        'Unit_Price': np.random.uniform(10, 500, rows).round(2),
        'Discount': np.random.choice([0.0, 0.1, 0.2, 0.5], rows, p=[0.6, 0.2, 0.15, 0.05])
    })
    
    df['Sales'] = (df['Quantity'] * df['Unit_Price'] * (1 - df['Discount'])).round(2)
    df['Profit'] = (df['Sales'] * 0.3 - (df['Sales'] * df['Discount'])).round(2)
    
    # Inject anomaly (Supply chain dump)
    anomaly_idx = (df['Order_Date'] >= '2022-06-10') & (df['Order_Date'] <= '2022-06-12')
    df.loc[anomaly_idx, 'Quantity'] *= 5
    df.loc[anomaly_idx, 'Sales'] *= 5
    
    import os
    os.makedirs('data/raw', exist_ok=True)
    df.sort_values('Order_Date').to_csv(output_path, index=False)
    print(f"Generated {rows} rows of raw data at {output_path}")

if __name__ == "__main__":
    generate_synthetic_data()
