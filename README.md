# Financial Fraud Detection – Multi-Source ETL + Modeling

**Portfolio project** that mirrors a real-world fintech data role: ingest messy 3rd‑party data (fintech API logs, credit bureau CSV, mobile money usage), clean + validate, engineer features, run **anomaly detection + supervised models**, and serve alerts via a **Streamlit** app. Includes an **Airflow DAG** and **CI**.

> Matches JD requirements: 3rd‑party integration, ETL/ELT, data quality, scalable architecture, ML for risk, documentation, and security practices.

## Highlights
- **Data sources** (synthetic but realistic): Transaction logs (JSON/CSV), Credit Bureau (CSV), Mobile Money usage (CSV).
- **ETL**: schema alignment, deduping, timestamp normalization, enrichment, and checks.
- **Quality**: missingness, duplicates, z-score outliers; report in `reports/quality_report.json`.
- **Features**: velocity, device/merchant risk, time-of-day, rolling stats, user history, credit score.
- **Models**:
  - **IsolationForest** for unsupervised anomalies.
  - **Logistic Regression (class_weight='balanced')** for supervised fraud classification.
- **Metrics**: Precision/Recall/F1/ROC-AUC, PR-AUC, confusion matrix; written to `reports/metrics.json`.
- **Serving**: Streamlit dashboard for alerts & KPIs.
- **Orchestration**: Airflow DAG (skeleton) for daily runs.
- **CI**: GitHub Actions workflow to run ETL + tests on PRs.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1) Run ETL + feature build
python scripts/etl_pipeline.py --run_all

# 2) Train & evaluate
python scripts/model_train.py --train --eval

# 3) Anomaly scoring (unsupervised)
python scripts/anomaly_detection.py --score

# 4) Launch dashboard
streamlit run app/streamlit_app.py
```

## Repo layout

```
fraud-detection-etl/
├─ README.md
├─ requirements.txt
├─ configs/
│  └─ config.yaml
├─ data/
│  ├─ raw/              # synthetic data (safe to commit)
│  └─ processed/        # features, train/test, predictions
├─ scripts/
│  ├─ etl_pipeline.py
│  ├─ model_train.py
│  └─ anomaly_detection.py
├─ models/              # persisted sklearn models
├─ app/
│  └─ streamlit_app.py
├─ dags/
│  └─ airflow_dag.py
├─ reports/
│  ├─ quality_report.json
│  └─ metrics.json
├─ tests/
│  └─ test_quality.py
└─ .github/workflows/
   └─ ci.yml
```

## Security & Compliance
- No PII; all data are synthetic.
- Config-driven paths; secrets (if any real APIs are used) via environment variables.
- Documented transformations; reproducible pipeline.

## License
MIT
