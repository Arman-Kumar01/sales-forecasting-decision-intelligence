import os
from src.generate_data import generate_synthetic_data
from src.data_pipeline import DataPipeline
from src.analytics import run_segmentation, detect_anomalies, run_forecasting
from src.decision_engine import generate_recommendations

def main():
    print("1. Generating Data...")
    generate_synthetic_data()
    
    print("2. Running ETL & Database Load...")
    df = DataPipeline().process()
    
    print("3. Running AI/ML Analytics...")
    rfm = run_segmentation(df)
    anomalies = detect_anomalies(df)
    metrics = run_forecasting(df)
    
    print(f"\n[Model Metrics]: MAE: {metrics['MAE']:.2f}, MAPE: {metrics['MAPE']:.2f}%")
    
    print("4. Generating Business Intelligence Actions...")
    generate_recommendations(rfm, anomalies, metrics)
    
    print("\nPipeline Complete! Run `run_dashboard.bat` to launch the Streamlit App.")

if __name__ == "__main__":
    main()
