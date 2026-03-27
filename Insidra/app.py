import pandas as pd

from model.preprocess import preprocess_data
from model.anomaly_model import train_model, predict
from model.risk_engine import (
    compute_baseline,
    merge_baseline,
    compute_drift,
    add_flags,
    compute_risk,
    assign_alert,
    generate_reason
)

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("data/logs.csv")

# -------------------------
# PIPELINE START
# -------------------------

# Step 1: preprocess
X_scaled, df = preprocess_data(df)

# Step 2: ML model
model = train_model(X_scaled)
scores, labels = predict(model, X_scaled)

df["anomaly_score"] = scores
df["anomaly"] = labels

# Step 3: baseline
baseline = compute_baseline(df)
df = merge_baseline(df, baseline)

# Step 4: drift + flags
df = compute_drift(df)
df = add_flags(df)

# Step 5: risk scoring
df = compute_risk(df)
df = assign_alert(df)

# Step 6: explanations
df["reasons"] = df.apply(generate_reason, axis=1)

# -------------------------
# OUTPUT
# -------------------------
final_cols = ["emp_id", "timestamp", "risk_score", "alert", "anomaly", "reasons"]
df_out = df[final_cols]
df_out.to_csv("data/scored_logs.csv", index=False)
print("Pipeline successful! Sample output:")
print(df_out.head())