# Intelligent Software Defect Tracking System with Resolution Assistance

An intelligent web-based software defect management system that combines **defect tracking, analytics, machine learning, duplicate detection, and resolution-time prediction** in a unified Streamlit application.

## Overview

The system uses historical software defect data to help development and testing teams monitor defects, identify patterns, predict defect properties, and support faster resolution.

## Key Features

* **Dashboard** — Overview of defect statistics, status, severity, priority, and modules
* **Bug Records** — Search, filter, and analyze software defect records
* **Analytics** — Interactive charts and statistical analysis
* **Trends** — Analyze defect patterns and trends over time
* **AI Prediction** — Predict severity, priority, and resolution time
* **Duplicate Detection** — Identify potentially similar defect reports
* **Resolution Analysis** — Analyze and estimate defect resolution time
* **Reports & Export** — Generate and export defect information

## Technology Stack

| Technology   | Purpose                        |
| ------------ | ------------------------------ |
| Python       | Application and ML development |
| Streamlit    | Web application framework      |
| Pandas       | Data processing                |
| NumPy        | Numerical computation          |
| Scikit-learn | Machine learning               |
| NLTK         | Natural language processing    |
| Plotly       | Interactive visualization      |
| Joblib       | Model storage                  |
| Git & GitHub | Version control                |

## Project Structure

```text
├── app.py
├── requirements.txt
├── train_priority_model.py
├── train_resolution_model.py
├── train_severity_model.py
├── assets/
├── data/
├── models/
├── utils/
└── views/
```

## Getting Started

### Prerequisites

* Python 3.10+
* Git
* Modern web browser

### Installation

```bash
git clone https://github.com/nithishkanna2005ga-hue/Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance.git
cd Intelligent-Software-Defect-Tracking-System-with-Resolution-Assistance
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open the application at:

```text
http://localhost:8501
```

To use port `8001`:

```bash
python -m streamlit run app.py --server.port 8001
```

## Machine Learning

The system provides:

* Severity Prediction
* Priority Prediction
* Resolution Time Prediction
* Duplicate Detection

Pre-trained models are stored in the `models/` directory.

Models can be retrained using:

```bash
python train_priority_model.py
python train_severity_model.py
python train_resolution_model.py
```

## Dataset

Historical defect data is stored in:

```text
data/Bug_Life_Cycle_Managementreport.csv
```

The dataset is used for defect analysis, visualization, duplicate detection, and machine learning.

## Workflow

```text
Defect Data → Data Processing → ML Models
     ↓
Prediction & Analysis → Dashboard & Reports
     ↓
Resolution Assistance
```

## Objective

The objective is to provide a centralized and intelligent platform for **software defect tracking, analysis, prediction, and resolution assistance**, enabling data-driven defect management.

