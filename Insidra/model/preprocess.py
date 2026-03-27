import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(df):
    df = df.copy()

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    # Encode categorical features
    for col in ["location", "device", "file_sensitivity"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])

    # Final feature set (NO emp_id, NO timestamp)
    features = [
        "hour",
        "files_accessed",
        "file_sensitivity",
        "location",
        "device",
        "failed_logins",
        "session_duration",
        "is_weekend"
    ]

    X = df[features]

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, df