import os
from pathlib import Path
import pandas as pd
import pytest
from src.generate_data import generate_synthetic_data

def test_data_generation():
    test_path = Path('data/raw/test_sales.csv')
    try:
        generate_synthetic_data(rows=100, output_path=str(test_path))
        df = pd.read_csv(test_path)
        assert len(df) >= 100
        assert 'Sales' in df.columns
        assert df['Sales'].min() >= 0
    finally:
        if test_path.exists():
            test_path.unlink()
