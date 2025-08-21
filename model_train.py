#!/usr/bin/env python3
import argparse, json
from pathlib import Path
import pandas as pd
import numpy as np
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score, average_precision_score, confusion_matrix
import joblib

def load_config(path="configs/config.yaml"):
    with open(path,"r") as f:
        return yaml.safe_load(f)

def select_features(df):
    drop_cols = ["txn_id","timestamp","user_id","merchant_id","device_type","country","label_fraud"]
    return [c for c in df.columns if c not in drop_cols]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/config.yaml")
    p.add_argument("--train", action="store_true")
    p.add_argument("--eval", action="store_true")
    args = p.parse_args()

    cfg = load_config(args.config)
    proc = Path(cfg["paths"]["processed"])
    reports = Path(cfg["paths"]["reports"])
    models_dir = Path(cfg["paths"]["models"])
    models_dir.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv(proc/"train.csv", parse_dates=["timestamp"])
    test  = pd.read_csv(proc/"test.csv", parse_dates=["timestamp"])

    feats = select_features(train)
    X_tr, y_tr = train[feats].values, train["label_fraud"].values
    X_te, y_te = test[feats].values,  test["label_fraud"].values

    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(X_tr, y_tr)

    joblib.dump(clf, models_dir/"logreg.pkl")
    pd.Series(feats).to_csv(models_dir/"features.txt", index=False)

    prob = clf.predict_proba(X_te)[:,1]
    pred = (prob>=0.5).astype(int)

    p_, r_, f1_, _ = precision_recall_fscore_support(y_te, pred, average="binary", zero_division=0)
    roc = roc_auc_score(y_te, prob)
    pr_auc = average_precision_score(y_te, prob)
    cm = confusion_matrix(y_te, pred).tolist()

    metrics = {
        "model": "logistic_regression_balanced",
        "features_used": feats,
        "precision": float(p_),
        "recall": float(r_),
        "f1": float(f1_),
        "roc_auc": float(roc),
        "pr_auc": float(pr_auc),
        "confusion_matrix": cm,
        "positive_rate_test": float(np.mean(y_te))
    }

    reports.mkdir(parents=True, exist_ok=True)
    with open(reports/"metrics.json","w") as f:
        json.dump(metrics, f, indent=2)

    out = test[["txn_id","timestamp","user_id","merchant_id","amount","label_fraud"]].copy()
    out["fraud_prob"] = prob
    out["fraud_pred"] = pred
    out.to_csv(proc/"predictions.csv", index=False)

    print("[OK] Trained and evaluated. Metrics written to reports/metrics.json.")
    print(f"[OK] Predictions saved to {proc/'predictions.csv'}")

if __name__ == "__main__":
    main()
