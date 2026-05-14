# 🦟 Dengue Prediction System - Backend API

[![Railway Deployment](https://img.shields.io/badge/Railway-Deployed-success?style=for-the-badge&logo=railway)](https://dengue-backend-production.up.railway.app/)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://www.python.org/)

Ye is project ka core API layer hai jo Machine Learning model ko serve karta hai. Ye model user ke symptoms ke base par dengue predict karta hai.

## 🚀 Tech Stack
* **Framework:** Flask (Python)
* **Server:** Gunicorn (WSGI)
* **Deployment:** Railway
* **Libraries:** Scikit-learn, Pandas, NumPy, Flask-CORS

## 🛠️ Key Features
* **ML Model Integration:** Pickle file ke zariye trained model ko load karta hai.
* **CORS Enabled:** Frontend requests (Vercel) ko handle karne ke liye CORS configured hai.
* **Scalable Hosting:** Railway par high-performance containerized deployment.

## 📍 API Endpoints
### POST `/predict`
Input JSON format:
```json
{
  "fever": 1,
  "headache": 1,
  "joint_pain": 0,
  "bleeding": 0
}
