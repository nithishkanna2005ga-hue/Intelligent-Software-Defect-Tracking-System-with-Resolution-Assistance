# Intelligent Software Defect Tracking System with Resolution Assistance

An intelligent web-based software defect management system that combines **defect tracking, data analytics, machine learning, duplicate detection, and resolution-time prediction** in a unified Streamlit application.

The system uses historical software defect data to provide actionable insights and AI-assisted predictions for improving defect management and resolution.

## Overview

The application provides an interactive interface for managing and analyzing software defects. It enables users to explore defect records, monitor trends, analyze severity and priority, identify potential duplicates, and obtain machine-learning-based predictions.

### Key Capabilities

* **Defect Management** — Search, filter, and analyze defect records
* **Dashboard & Analytics** — Monitor defect statistics, distributions, and trends
* **AI-Based Prediction** — Predict defect severity, priority, and resolution time
* **Duplicate Detection** — Identify potentially similar defect reports
* **Resolution Analysis** — Analyze historical and predicted resolution times
* **Reports & Export** — Generate and export defect-related information

## Technology Stack

| Technology   | Usage                          |
| ------------ | ------------------------------ |
| Python       | Application and ML development |
| Streamlit    | Web application framework      |
| Pandas       | Data processing                |
| NumPy        | Numerical computation          |
| Scikit-learn | Machine learning               |
| NLTK         | Natural language processing    |
| Plotly       | Interactive visualization      |
| Joblib       | Model serialization            |
| Git & GitHub | Version control                |

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
```

## Getting Started

### Prerequisites

* Python 3.10 or later
* Git
* A modern web browser

### Installation

Clone the repository:

```bash
git clone https://github.com/nithishkanna2005ga-hue/Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance.git
cd Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance
```

Create and activate a virtual environment:

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application

Start the Streamlit application with:

```bash
python -m streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

To run it on a custom port:

```bash
python -m streamlit run app.py --server.port 8001
```

## Machine Learning

The system includes machine learning models for:

* **Severity Prediction**
* **Priority Prediction**
* **Resolution Time Prediction**

Pre-trained models are stored in the `models/` directory.

To retrain the models:

```bash
python train_priority_model.py
python train_severity_model.py
python train_resolution_model.py
```

## Dataset

The application uses historical software defect data stored in:

```text
data/Bug_Life_Cycle_Managementreport.csv
```

The dataset supports analytics, trend analysis, duplicate detection, and machine learning model training.

## Application Workflow

```text
Historical Defect Data
          ↓
    Data Processing
          ↓
 Machine Learning Models
          ↓
Prediction & Analysis
          ↓
 Dashboard & Reports
          ↓
 Resolution Assistance
```

## Purpose

The objective of this project is to provide an intelligent and centralized platform for **software defect tracking and resolution assistance**, helping development and testing teams make data-driven decisions and improve defect management efficiency.

## License

This project is developed for **academic and educational purposes**.
