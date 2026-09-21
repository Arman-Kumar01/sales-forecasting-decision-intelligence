import pandas as pd

def generate_recommendations(rfm, anomalies, metrics):
    recs = []
    at_risk = len(rfm[rfm['Segment'] == 'At Risk'])
    recs.append({'Category': 'Marketing', 'Issue': f'{at_risk} High-Value Customers At Risk', 'Action': 'Launch targeted win-back email sequence with 15% discount code.'})
    
    recent_anom = anomalies[anomalies['Anomaly'] == -1]
    if not recent_anom.empty:
         recs.append({'Category': 'Operations', 'Issue': 'Irregular Sales Spikes Detected', 'Action': 'Audit supply chain logs for bulk buyer disruption.'})
    
    pd.DataFrame(recs).to_csv("data/processed/recommendations.csv", index=False)
