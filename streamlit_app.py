import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")
st.title("🕵🏾‍♂️ Fraud Detection – Multi-Source ETL + Modeling")

proc = Path("data/processed")
reports = Path("reports")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Classification Metrics")
    m = reports/"metrics.json"
    if m.exists():
        st.json(json.loads(m.read_text()))
    else:
        st.info("Run training to see metrics (python scripts/model_train.py --train --eval).")

with col2:
    st.subheader("Recent Predictions (Top-Risk)")
    preds = proc/"predictions.csv"
    if preds.exists():
        df = pd.read_csv(preds, parse_dates=["timestamp"])
        st.dataframe(df.sort_values("fraud_prob", ascending=False).head(50))
    else:
        st.info("No predictions yet.")

st.divider()
st.subheader("Anomaly Scores (Unsupervised)")
anom = proc/"anomaly_scores.csv"
if anom.exists():
    df = pd.read_csv(anom, parse_dates=["timestamp"])
    st.dataframe(df.sort_values("anomaly_score", ascending=False).head(50))
else:
    st.info("Run anomaly scoring (python scripts/anomaly_detection.py --score).")
