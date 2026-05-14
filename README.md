# 🦟 Dengue Prediction System - Backend API

[![Railway Deployment](https://img.shields.io/badge/Railway-Deployed-success?style=for-the-badge&logo=railway)](https://dengue-backend-production.up.railway.app/)
[![Python Version](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://www.python.org/)

This is the core API layer for the Dengue Alert PK system. It serves a Machine Learning model that predicts the likelihood of dengue based on user-reported symptoms. 

## 🚀 Technical Architecture
The backend is built with efficiency and scalability in mind, utilizing a modern Python stack:

* **Framework:** Flask (Lightweight WSGI web application framework).
* **ML Engine:** Scikit-learn (Used for loading and executing the trained `.pkl` predictive model).
* **Production Server:** Gunicorn (Green Unicorn) for handling concurrent requests in a production environment.
* **Deployment:** Containerized and hosted on **Railway** with automated CI/CD.

## 🛠️ Key Features
* **RESTful API:** Provides a clean POST endpoint for symptom analysis.
* **CORS Integration:** Configured via `flask-cors` to allow secure communication with the Next.js frontend hosted on Vercel.
* **Environment Dynamic:** Automatically detects deployment ports to ensure 100% uptime on cloud environments.

## 📍 API Specification
### Endpoint: `POST /predict`
The API expects a JSON payload containing binary indicators (1 for Yes, 0 for No) for symptoms.

**Request Body:**
```json
{
  "fever": 1,
  "headache": 0,
  "joint_pain": 1,
  "bleeding": 0
}
