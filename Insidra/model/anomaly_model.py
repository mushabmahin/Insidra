from sklearn.ensemble import IsolationForest

def train_model(X):
    model = IsolationForest(
        n_estimators=100,
        contamination=0.08,   # realistic assumption: ~8% anomalies
        random_state=42
    )
    model.fit(X)
    return model


def predict(model, X):
    scores = model.decision_function(X)
    labels = model.predict(X)   # -1 anomaly, 1 normal
    return scores, labels