"""
===============================================================================
Data Loader Utility
Bug Life Cycle Management Dashboard
===============================================================================

Centralized dataset loading system.
All pages use this file to access bug data.
===============================================================================
"""

from __future__ import annotations

from datetime import datetime, timedelta

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


# =============================================================================
# PROJECT PATHS
# =============================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent


DATA_DIR = ROOT_DIR / "data"


CSV_FILE = DATA_DIR / "Bug_Life_Cycle_Management.csv"


# =============================================================================
# SAMPLE DATA GENERATOR
# (Temporary fallback until real dataset is connected)
# =============================================================================

def create_sample_data():

    np.random.seed(42)


    n = 500


    statuses = [

        "Open",
        "Assigned",
        "In Progress",
        "Resolved",
        "Closed",

    ]


    priorities = [

        "Low",
        "Medium",
        "High",
        "Critical",

    ]


    severities = [

        "Minor",
        "Major",
        "Critical",
        "Blocker",

    ]


    developers = [

        "Alex",
        "John",
        "Emma",
        "David",
        "Sophia",
        "Daniel",

    ]


    modules = [

        "Authentication",
        "UI",
        "Database",
        "API",
        "Reports",
        "Notification",
        "Payment",

    ]


    resolutions = [

        "Fixed",
        "Duplicate",
        "Rejected",
        "Cannot Reproduce",

    ]


    start_date = datetime.today() - timedelta(days=180)


    df = pd.DataFrame({

        "Bug ID":

            [

                f"BUG-{1000+i}"

                for i in range(n)

            ],


        "Status":

            np.random.choice(

                statuses,

                n

            ),


        "Priority":

            np.random.choice(

                priorities,

                n

            ),


        "Severity":

            np.random.choice(

                severities,

                n

            ),


        "Developer":

            np.random.choice(

                developers,

                n

            ),


        "Module":

            np.random.choice(

                modules,

                n

            ),


        "Resolution":

            np.random.choice(

                resolutions,

                n

            ),


        "Resolution Days":

            np.random.randint(

                1,

                30,

                n

            ),


        "Created Date":

            [

                start_date +

                timedelta(

                    days=int(i)

                )

                for i in np.random.randint(

                    0,

                    180,

                    n

                )

            ],


        "Duplicate":

            np.random.choice(

                [

                    "Yes",

                    "No"

                ],

                n,

                p=[0.15,0.85]

            )

    })


    return df
# =============================================================================
# LOAD DATASET
# =============================================================================

@st.cache_data
def load_data():

    """
    Loads the bug dataset.

    Priority:
    1. Real CSV file
    2. Sample dataset fallback
    """


    if CSV_FILE.exists():


        try:


            df = pd.read_csv(

                CSV_FILE

            )


            return clean_dataset(df)


        except Exception:


            return create_sample_data()


    else:


        return create_sample_data()



# =============================================================================
# DATA CLEANING
# =============================================================================

def clean_dataset(df):


    df = df.copy()


    # Remove duplicate rows

    df.drop_duplicates(

        inplace=True

    )


    # Fill missing values

    df.fillna(

        "Unknown",

        inplace=True

    )


    # Standardize text columns

    text_columns = [

        "Status",

        "Priority",

        "Severity",

        "Developer",

        "Module",

        "Resolution",

        "Duplicate",

    ]


    for col in text_columns:


        if col in df.columns:


            df[col] = (

                df[col]

                .astype(str)

                .str.strip()

                .str.title()

            )


    # Date conversion

    if "Created Date" in df.columns:


        df["Created Date"] = pd.to_datetime(

            df["Created Date"],

            errors="coerce",

        )


    return df



# =============================================================================
# MAIN DATA ACCESS FUNCTION
# =============================================================================

def get_dataframe():

    """
    Universal dataframe provider.

    All dashboard pages call this.
    """


    df = load_data()


    return df
# =============================================================================
# DATASET VALIDATION
# =============================================================================

def validate_dataset(df):

    """
    Checks whether required columns exist.
    """


    required_columns = [

        "Bug ID",

        "Status",

        "Priority",

        "Severity",

        "Developer",

        "Module",

        "Resolution",

        "Resolution Days",

        "Created Date",

        "Duplicate",

    ]


    missing_columns = [

        col

        for col in required_columns

        if col not in df.columns

    ]


    return missing_columns



# =============================================================================
# DEBUG INFORMATION
# =============================================================================

def dataset_info():

    """
    Returns dataset information
    for debugging.
    """


    df = get_dataframe()


    return {

        "Rows":

        len(df),


        "Columns":

        list(df.columns),


        "Missing Values":

        df.isnull()

        .sum()

        .to_dict(),

    }



# =============================================================================
# INITIAL DATA CHECK
# =============================================================================

if __name__ == "__main__":


    data = get_dataframe()


    print(

        "Dataset Loaded Successfully"

    )


    print(

        data.head()

    )


    print(

        dataset_info()

    )