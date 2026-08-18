# ==========================================================
# TRAIN BUG SEVERITY PREDICTION MODEL
# ==========================================================

import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# Dataset path

DATA_PATH = "data/Bug_Life_Cycle_Managementreport.csv"


# Load data

df = pd.read_csv(DATA_PATH)


# Remove missing values

df = df.fillna("Unknown")


# Combine text information

df["Text"] = (

    df["Bug_Title"].astype(str)
    + " "
    + df["Bug_Description"].astype(str)

)



# Input and output

X = df["Text"]

y = df["Priority"]



# Convert text into numbers

vectorizer = TfidfVectorizer(

    stop_words="english",

    max_features=5000

)


X_vector = vectorizer.fit_transform(X)



# Split data

X_train, X_test, y_train, y_test = train_test_split(

    X_vector,

    y,

    test_size=0.2,

    random_state=42

)



# Train model

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42

)


model.fit(

    X_train,

    y_train

)



# Accuracy

accuracy = model.score(

    X_test,

    y_test

)


print(
    "Model Accuracy:",
    round(accuracy*100,2),
    "%"
)



# Save model

pickle.dump(

    model,

    open(
        "models/severity_model.pkl",
        "wb"
    )

)


pickle.dump(

    vectorizer,

    open(
        "models/tfidf_vectorizer.pkl",
        "wb"
    )

)


print(
    "Model Saved Successfully"
)