import pandas as pd

# -------------------------
# BASELINE
# -------------------------
def compute_baseline(df):
    baseline = df.groupby("emp_id").agg({
        "hour": "mean",
        "files_accessed": "mean",
        "session_duration": "mean"
    }).reset_index()

    return baseline


# -------------------------
# MERGE BASELINE
# -------------------------
def merge_baseline(df, baseline):
    return df.merge(baseline, on="emp_id", suffixes=("", "_base"))


# -------------------------
# DRIFT
# -------------------------
def compute_drift(df):
    df["login_drift"] = abs(df["hour"] - df["hour_base"])
    df["file_drift"] = df["files_accessed"] / (df["files_accessed_base"] + 1)
    return df


# -------------------------
# FLAGS (EXPLAINABILITY)
# -------------------------
def add_flags(df):
    df["odd_hour"] = (df["hour"] < 6) | (df["hour"] > 22)

    df["file_spike"] = df["files_accessed"] > df["files_accessed_base"] * 3

    df["location_change"] = df["location"] != df.groupby("emp_id")["location"].transform("first")

    df["device_change"] = df["device"] != df.groupby("emp_id")["device"].transform("first")

    return df


# -------------------------
# RISK ENGINE
# -------------------------
def compute_risk(df):
    risk_scores = []

    for _, row in df.iterrows():
        risk = 0

        # ML anomaly
        if row["anomaly"] == -1:
            risk += 40

        # Drift contribution
        if row["file_drift"] > 3:
            risk += 20

        if row["login_drift"] > 5:
            risk += 10

        # Behavioral signals
        if row["file_spike"]:
            risk += 15

        if row["location_change"]:
            risk += 10

        if row["device_change"]:
            risk += 5

        if row["odd_hour"]:
            risk += 5

        if row["failed_logins"] > 3:
            risk += 10

        risk_scores.append(min(risk, 100))

    df["risk_score"] = risk_scores
    return df


# -------------------------
# ALERT LEVEL
# -------------------------
def assign_alert(df):
    def level(score):
        if score > 70:
            return "HIGH"
        elif score > 40:
            return "MEDIUM"
        return "LOW"

    df["alert"] = df["risk_score"].apply(level)
    return df


# -------------------------
# EXPLANATION
# -------------------------
def generate_reason(row):
    reasons = []

    if row["file_spike"]:
        reasons.append("Unusual file access spike")

    if row["location_change"]:
        reasons.append("New login location")

    if row["device_change"]:
        reasons.append("New device used")

    if row["odd_hour"]:
        reasons.append("Unusual login time")

    if row["failed_logins"] > 3:
        reasons.append("Multiple failed login attempts")

    return reasons