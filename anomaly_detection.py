#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import yaml
from sklearn.ensemble import IsolationForest

def load_config(path="configs/config.yaml"):
    with open(path,"r") as f:
        return yaml.safe_load(f)

def select_features(df):
    drop_cols = ["txn_id","timestamp","user_id","merchant_id","device_type","country","label_fraud"]
    return [c for c in df.columns if c not in drop_cols]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/config.yaml")
    p.add_argument("--score", action="store_true")
    args = p.parse_args()

    cfg = load_config(args.config)
    proc = Path(cfg["paths"]["processed"])

    features = pd.read_csv(proc/"features.csv", parse_dates=["timestamp"])
    feats = select_features(features)
    X = features[feats].values

    iso = IsolationForest(n_estimators=200, contamination=0.025, random_state=42)
    scores = -iso.fit_predict(X)  # 2 (outlier) or 1 (inlier)
    anomaly_score = iso.decision_function(X) * -1

    out = features[["txn_id","timestamp","user_id","merchant_id","amount","label_fraud"]].copy()
    out["anomaly_flag"] = (scores==2).astype(int)
    out["anomaly_score"] = anomaly_score
    out.to_csv(proc/"anomaly_scores.csv", index=False)

    print(f"[OK] Anomaly scores saved to {proc/'anomaly_scores.csv'}")

if __name__ == "__main__":
    main()
