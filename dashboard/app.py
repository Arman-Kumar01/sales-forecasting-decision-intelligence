import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(
    page_title="Sales Forecasting & Decision Intelligence",
    page_icon="🚀",
    layout="wide"
)

@st.cache_data
def load_data():
    processed_dir = PROJECT_ROOT / 'data' / 'processed'
    cleaned_file = processed_dir / 'cleaned_sales.csv'
    
    # Auto-generate pipeline artifacts if missing (e.g. on fresh cloud deployment)
    if not cleaned_file.exists():
        from main import main as run_pipeline
        with st.spinner("Initializing pipeline, generating synthetic data, and training ML models..."):
            run_pipeline()

    df = pd.read_csv(processed_dir / 'cleaned_sales.csv')
    rfm = pd.read_csv(processed_dir / 'rfm_segments.csv')
    forecast = pd.read_csv(processed_dir / 'forecast_results.csv')
    anomalies = pd.read_csv(processed_dir / 'anomalies.csv')
    recs = pd.read_csv(processed_dir / 'recommendations.csv')
    return df, rfm, forecast, anomalies, recs

df, rfm, forecast, anomalies, recs = load_data()

st.title("🚀 Sales Forecasting & Decision Intelligence")

tab1, tab2, tab3, tab4 = st.tabs(["Executive KPIs", "Forecasting", "Customer Segments", "AI Actions"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${df['Sales'].sum():,.0f}")
    col2.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
    col3.metric("Total Customers", len(df['Customer_ID'].unique()))
    col4.metric("Avg Order Value", f"${df['Sales'].mean():,.2f}")
    
    monthly = df.groupby('YearMonth')['Sales'].sum().reset_index()
    st.plotly_chart(px.line(monthly, x='YearMonth', y='Sales', title="Revenue Trend"), use_container_width=True)

with tab2:
    st.subheader("Random Forest vs Actuals (Validation Set)")
    fig = px.line(forecast, x='Date', y=['Actual', 'Predicted'], markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("RFM Customer Clustering")
    fig2 = px.scatter(rfm, x='Recency', y='Monetary', color='Segment', hover_data=['Frequency'])
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.subheader("Decision Intelligence Engine")
    for _, row in recs.iterrows():
        st.warning(f"**{row['Category']} | {row['Issue']}** \n\n **Action:** {row['Action']}")
