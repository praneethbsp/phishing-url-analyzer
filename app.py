import os
import re
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np


app = FastAPI(
    title="Phishing URL Detection API",
    description="Inference API serving the trained Random Forest Classifier",
    version="1.0.0"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "notebooks", "phishing_rf_model.joblib")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at expected path: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print(f"[+] Model loaded successfully from: {MODEL_PATH}")


class URLRequest(BaseModel):
    url: str


def extract_features(url: str):
    parsed = urlparse(url)
    hostname = parsed.netloc or ""
    path = parsed.path or ""
    query = parsed.query or ""

    
    url_len = len(url)

    
    dots = url.count(".")

   
    digits = sum(c.isdigit() for c in url)

    
    hyphens = url.count("-")

    
    special_chars = len(re.findall(r'[@_!#$%^&*()<>?/\|}{~:]', url))

    
    subdirs = path.count("/")

    
    query_params = len(query.split("&")) if query else 0

    
    ip_pattern = r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])'
    has_ip = 1 if re.search(ip_pattern, hostname) else 0

    
    has_https = 1 if parsed.scheme.lower() == "https" else 0

    
    has_at = 1 if "@" in url else 0

    
    keywords = ["login", "verify", "update", "secure", "account", "banking", "signin", "confirm", "wallet"]
    kw_count = sum(1 for kw in keywords if kw in url.lower())

    
    has_enc = 1 if "%" in url else 0

    return [
        url_len, dots, digits, hyphens, special_chars,
        subdirs, query_params, has_ip, has_https, has_at,
        kw_count, has_enc
    ]


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Phishing URL Detector",
        "model_loaded": True
    }


@app.post("/predict")
def predict_url(payload: URLRequest):
    cleaned_url = payload.url.strip()
    if not cleaned_url:
        raise HTTPException(status_code=400, detail="URL field cannot be empty.")

    feature_vector = np.array([extract_features(cleaned_url)])

    
    prediction = int(model.predict(feature_vector)[0])
    probabilities = model.predict_proba(feature_vector)[0]

    prob_phishing = round(float(probabilities[0]) * 100, 2)
    prob_safe = round(float(probabilities[1]) * 100, 2)

    return {
        "url": cleaned_url,
        "is_safe": bool(prediction == 1),
        "prediction_label": "Safe" if prediction == 1 else "Phishing",
        "phishing_confidence_pct": prob_phishing,
        "safe_confidence_pct": prob_safe
    }