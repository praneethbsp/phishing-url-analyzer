# 🛡️ Phishing URL Detection & Real-Time Defense API

An end-to-end Machine Learning and API pipeline that analyzes raw web links and classifies them as **Safe** or **Phishing** using extracted lexical, structural, and semantic patterns.

---

## 📌 Project Overview
Phishing attacks frequently bypass signature-based filters by altering domain structures and lexical characteristics. This project trains and evaluates multiple machine learning architectures on the **PhiUSIIL Phishing URL Dataset** (235,000+ URLs) and deploys the highest-performing model via a low-latency **FastAPI** inference endpoint.

---

## 🚀 Key Features
* **12 Lexical & Structural Indicators:** Extracts length, dot counts, digit density, hyphen distribution, subdirectory nesting, URL encoding, raw IP detection, HTTPS status, and deceptive security keywords.
* **Trained Models Evaluated:**
  * **Logistic Regression:** Baseline linear classification.
  * **Decision Tree Classifier:** Non-linear rule learning with pre-pruning (`max_depth=5`) to prevent overfitting.
  * **Random Forest Classifier (Selected):** Ensemble model leveraging 100 estimators, bagging, and feature subsampling to minimize false negatives.
* **Production API Service:** Built with **FastAPI** and **Uvicorn**, serving the model directly via a structured `POST /predict` endpoint with input validation and confidence percentages.

---

## 📊 Model Performance Comparison

| Metric | Logistic Regression | Decision Tree (Pruned) | Random Forest (100 Trees) |
|---|---|---|---|
| **Accuracy** | 99.32% | 99.46% | **99.54%** |
| **Phishing Recall** | 98.48% | 99.01% | **99.01%** |
| **Missed Phishing URLs (FN)** | 305 | 199 | **199** |
| **False Positives (FP)** | **14** | 24 | 19 |

> **Security Priority:** In phishing detection, **Phishing Recall** is prioritized over simple accuracy to minimize False Negatives (missed threats that compromise users).

---

## 🛠️ Project Structure
```text
phishing-url-analyzer/
├── data/
│   └── PhiUSIIL_Phishing_URL_Dataset.csv
├── notebooks/
│   ├── day1_eda.ipynb
│   └── phishing_rf_model.joblib
├── app.py
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Quickstart & Local Setup
1. Clone the repository
Bash
git clone https://github.com/praneethbsp/phishing-url-analyzer.git
cd phishing-url-analyzer
2. Set up virtual environment
Bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
3. Install dependencies
Bash
pip install -r requirements.txt
4. Start the inference API
Bash
uvicorn app:app --reload --port 8000
🔌 API Usage
Interactive Docs (Swagger UI)
Visit http://127.0.0.1:8000/docs in your browser to test endpoints interactively.

Predict Endpoint (POST /predict)
Request Payload:

JSON
{
  "url": "http://192.168.1.1/secure-update/login.php"
}
Response Payload:

JSON
{
  "url": "http://192.168.1.1/secure-update/login.php",
  "is_safe": false,
  "prediction_label": "Phishing",
  "phishing_confidence_pct": 100.0,
  "safe_confidence_pct": 0.0
}
💻 Tech Stack
Language: Python 3.10+

Data Processing & ML: Pandas, NumPy, Scikit-Learn, Joblib

Backend Serving: FastAPI, Pydantic, Uvicorn