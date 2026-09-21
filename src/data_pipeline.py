import pandas as pd
import sqlite3
from pathlib import Path

class DataPipeline:
    def __init__(self):
        self.raw_path = Path("data/raw/sales.csv")
        self.db_path = Path("data/database/retail.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        Path("data/processed").mkdir(parents=True, exist_ok=True)

    def process(self):
        df = pd.read_csv(self.raw_path)
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        
        # Validation
        invalid_sales = len(df[df['Sales'] < 0])
        invalid_qty = len(df[df['Quantity'] <= 0])
        if invalid_sales > 0 or invalid_qty > 0:
            print(f"Validation WARNING: {invalid_sales} negative sales, {invalid_qty} invalid quantities.")
            df = df[(df['Sales'] >= 0) & (df['Quantity'] > 0)]
            
        df.drop_duplicates(inplace=True)
        
        # Feature Engineering (Business features)
        df['Profit_Margin'] = (df['Profit'] / df['Sales']).fillna(0)
        df['YearMonth'] = df['Order_Date'].dt.to_period('M').astype(str)
        
        df.to_csv("data/processed/cleaned_sales.csv", index=False)
        
        # SQL Load
        conn = sqlite3.connect(self.db_path)
        df.to_sql('orders', conn, if_exists='replace', index=False)
        conn.close()
        return df
