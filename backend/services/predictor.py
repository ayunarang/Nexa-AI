# services/predictor.py

import joblib

model = joblib.load("models/")

def predict_labels(texts: list[str]) -> list[str]:
    return model.predict(texts)
