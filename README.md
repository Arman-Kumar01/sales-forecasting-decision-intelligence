# 🚀 Sales Forecasting & Decision Intelligence

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.2%2B-orange.svg)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.14%2B-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end Machine Learning and Business Intelligence platform that bridges the gap between predictive time-series modeling and automated executive decision-making.

---

## 🌟 Key Features

1. **Synthetic Data Engine & Automated ETL**:
   - Generates realistic multi-year retail transactions with Q4 holiday seasonality, discount structures, and real-world supply chain anomalies.
   - Cleans, transforms, and loads transactional records into an analytical SQLite database (`retail.db`).

2. **Customer Intelligence (RFM Segmentation)**:
   - Evaluates **Recency**, **Frequency**, and **Monetary** value per customer using K-Means clustering and quantiles.
   - Classifies customer bases into actionable cohorts: *Champions*, *Loyal*, *At Risk*, and *Lost*.

3. **Anomaly Detection**:
   - Unsupervised **Isolation Forest** scanning order timelines to identify uncharacteristic spikes or supply chain disruptions.

4. **Time-Series Sales Forecasting**:
   - Feature engineering with lag variables (`lag_1`, `lag_2`, `lag_12`), rolling averages, and calendar months to prevent data leakage.
   - **Random Forest Regressor** evaluated chronologically against a 6-month out-of-time validation test set (MAE: ~$25k, MAPE: ~7.8%).

5. **Decision Intelligence Engine**:
   - Converts raw ML outputs into automated operational recommendations (e.g. targeted win-back discount campaigns for at-risk cohorts, inventory audits for demand spikes).

6. **Executive Web Dashboard**:
   - Interactive 4-tab Streamlit dashboard built with dynamic Plotly visualizations.

---

## 🏗️ Architecture & Project Structure

```
sales-forecasting-decision-intelligence/
├── dashboard/
│   └── app.py                 # Interactive Streamlit dashboard application
├── src/
│   ├── __init__.py
│   ├── generate_data.py       # Data generator with seasonality & anomalies
│   ├── data_pipeline.py       # ETL pipeline & SQLite persistence
│   ├── analytics.py           # RFM clustering, Anomaly detection, Forecasting
│   └── decision_engine.py     # Rule-based decision recommendation engine
├── sql/
│   └── queries.sql            # Analytical SQL queries (YoY growth, window functions)
├── tests/
│   └── test_pipeline.py       # Pytest unit tests
├── data/                      # Data storage (git-safe, auto-generated)
│   ├── raw/
│   ├── processed/
│   └── database/
├── models/                    # Model serialization directory
├── main.py                    # Complete end-to-end pipeline runner
├── streamlit_app.py           # Streamlit Cloud deployment entry point
├── run_dashboard.bat          # 1-click Windows dashboard launcher
├── requirements.txt           # Project dependencies
└── .gitignore                 # Production-grade git exclusions
```

---

## ⚡ Quickstart (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/Arman-Kumar01/sales-forecasting-decision-intelligence.git
cd sales-forecasting-decision-intelligence
```

### 2. Set up virtual environment (recommended)
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Pipeline & Train Models
```bash
python main.py
```
*Output summary:*
```
1. Generating Data...
Generated 12000 rows of raw data at data/raw/sales.csv
2. Running ETL & Database Load...
3. Running AI/ML Analytics...
[Model Metrics]: MAE: 25143.89, MAPE: 7.82%
4. Generating Business Intelligence Actions...
Pipeline Complete! Run `run_dashboard.bat` to launch the Streamlit App.
```

### 5. Launch the Dashboard
```bash
streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Running Tests

Execute test suite with `pytest`:
```bash
python -m pytest
```

---

## ☁️ Deployment (Streamlit Community Cloud)

You can deploy this application for free on **Streamlit Community Cloud** in 3 simple steps:

1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **"New app"** and configure:
   - **Repository:** `Arman-Kumar01/sales-forecasting-decision-intelligence`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
3. Click **"Deploy!"**

> **Note**: The dashboard includes automated self-healing data generation — if deployed to a fresh environment without pre-cached files, it will automatically build the synthetic data and run the ML models on first startup.

---

## 👤 Author
- **Arman Kumar** - [GitHub](https://github.com/Arman-Kumar01)
