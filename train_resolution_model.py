"""
===============================================================================
Resolution Prediction Model Training
Bug Life Cycle Management Dashboard
===============================================================================

Trains a Machine Learning model to predict bug resolution time.
===============================================================================
"""

import os
import pickle

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# =============================================================================
# PATHS
# =============================================================================

DATASET_PATH = r"E:\Bug_Life_Cycle_Management\data\Bug_Life_Cycle_Managementreport.csv"

MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "resolution_model.pkl"
)


# =============================================================================
# LOAD DATA
# =============================================================================

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)


print("Dataset loaded")
print(df.head())


# =============================================================================
# CHECK COLUMNS
# =============================================================================

print("\nAvailable Columns:")
print(df.columns.tolist())


# =============================================================================
# PREPARE DATA
# =============================================================================

# Change this column name if your dataset uses another name

TARGET_COLUMN = "Resolution_Time_Hours"


# Check target exists

if TARGET_COLUMN not in df.columns:

    raise Exception(
        f"{TARGET_COLUMN} column not found in dataset"
    )


# Features used for prediction

features = []


if "Severity" in df.columns:

    features.append("Severity")


if "Priority" in df.columns:

    features.append("Priority")


if "Module" in df.columns:

    features.append("Module")


if "Developer" in df.columns:

    features.append("Developer")


print("\nFeatures Used:")
print(features)



# Convert categorical columns

X = df[features].copy()

y = df[TARGET_COLUMN]


X = pd.get_dummies(X)


# Remove missing values

data = pd.concat(
    [X, y],
    axis=1
).dropna()


X = data.drop(
    TARGET_COLUMN,
    axis=1
)

y = data[TARGET_COLUMN]


# =============================================================================
# TRAIN MODEL
# =============================================================================

print("\nTraining Resolution Model...")


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


# =============================================================================
# TEST MODEL
# =============================================================================

prediction = model.predict(
    X_test
)


print(
    "\nMean Absolute Error:",
    mean_absolute_error(
        y_test,
        prediction
    )
)


print(
    "R2 Score:",
    r2_score(
        y_test,
        prediction
    )
)


# =============================================================================
# SAVE MODEL
# =============================================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


MODEL_DATA = {
    "model": model,
    "features": X.columns.tolist()
}


with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        MODEL_DATA,
        file
    )


print("\n================================")
print("Resolution Model Saved")
print(MODEL_PATH)
print("================================")