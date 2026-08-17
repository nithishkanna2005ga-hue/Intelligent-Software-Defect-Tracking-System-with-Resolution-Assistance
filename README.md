# Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance
# Intelligent Software Defect Tracking System with Resolution Assistance

An intelligent software defect tracking system built using **Python, Streamlit, Machine Learning, and historical defect data**. The system helps users track, analyze, predict, and manage software defects efficiently.

## Overview

This application provides an interactive platform for managing software defect records and analyzing defect trends. It includes dashboards, analytics, AI-based predictions, duplicate detection, and resolution time analysis.

The system uses historical bug data and machine learning models to assist in predicting defect properties and understanding software defect patterns.

## Key Features

### 📊 Dashboard
- Total bug statistics
- Open and resolved bugs
- Critical bug count
- Average resolution time
- Priority and severity distribution
- Status and module-wise analysis

### 🐞 Bug Records
- View software defect records
- Search and filter bugs
- Analyze Bug ID, module, priority, severity, status, and other details

### 📈 Analytics and Trends
- Priority distribution
- Severity distribution
- Bug status analysis
- Module-wise and team-wise bug analysis
- Bug trends over time
- Resolution time analysis

### 🤖 AI Prediction
Machine learning models are used to predict defect-related information based on bug descriptions and historical data.

The project includes models for:
- Severity Prediction
- Priority Prediction
- Resolution Time Prediction

### 🔍 Duplicate Detection
The system compares bug descriptions to help identify potentially similar or duplicate defects.

### ⏱️ Resolution Analysis
- Analyze defect resolution time
- Compare resolution performance
- Study resolution trends using historical bug data

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Pandas | Data processing and analysis |
| Plotly | Interactive visualizations |
| Scikit-learn | Machine learning |
| Joblib | Model storage |
| CSV | Defect dataset storage |

## Project Structure

```text
Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance/
│
├── app.py
├── requirements.txt
├── train_priority_model.py
├── train_resolution_model.py
├── train_severity_model.py
│
├── assets/
│   └── style.css
│
├── data/
│   └── Bug_Life_Cycle_Managementreport.csv
│
├── models/
│   ├── priority_model.pkl
│   ├── priority_vectorizer.pkl
│   ├── resolution_model.pkl
│   ├── severity_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── utils/
│   ├── ai_model.py
│   ├── charts.py
│   ├── data_loader.py
│   ├── export.py
│   ├── filters.py
│   └── helpers.py
│
└── views/
    ├── ai_prediction.py
    ├── analytics.py
    ├── bug_records.py
    ├── dashboard.py
    ├── duplicate_detection.py
    ├── reports.py
    ├── resolution_time.py
    ├── settings.py
    └── trends.py
