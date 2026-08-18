"""
===============================================================================
AI Prediction Page
Bug Life Cycle Management Dashboard
===============================================================================

Machine Learning based bug analysis and prediction.
===============================================================================
"""

from __future__ import annotations

import os
import pickle

import pandas as pd
import streamlit as st

from utils.data_loader import get_dataframe


# =============================================================================
# MODEL PATHS
# =============================================================================

MODEL_DIR = "models"


TFIDF_VECTORIZER = os.path.join(
    MODEL_DIR,
    "tfidf_vectorizer.pkl"
)


PRIORITY_VECTORIZER = os.path.join(
    MODEL_DIR,
    "priority_vectorizer.pkl"
)


SEVERITY_MODEL = os.path.join(
    MODEL_DIR,
    "severity_model.pkl"
)


PRIORITY_MODEL = os.path.join(
    MODEL_DIR,
    "priority_model.pkl"
)


RESOLUTION_MODEL = os.path.join(
    MODEL_DIR,
    "resolution_model.pkl"
)


# =============================================================================
# LOAD MODEL
# =============================================================================

@st.cache_resource
def load_model(path):

    if os.path.exists(path):

        with open(
            path,
            "rb"
        ) as file:

            return pickle.load(file)

    return None
# =============================================================================
# AI PREDICTION PAGE
# =============================================================================

def show_ai_prediction():

    df = get_dataframe()


    if "prediction_history" not in st.session_state:

        st.session_state.prediction_history = []


    st.header(
        "🤖 AI Bug Prediction"
    )


    st.caption(
        "Machine Learning assisted bug severity, priority and resolution prediction"
    )


    st.markdown("---")


    # =========================================================================
    # LOAD MODELS
    # =========================================================================

    severity_model = load_model(
        SEVERITY_MODEL
    )


    tfidf_vectorizer = load_model(
        TFIDF_VECTORIZER
    )


    priority_model = load_model(
        PRIORITY_MODEL
    )


    priority_vectorizer = load_model(
        PRIORITY_VECTORIZER
    )


    resolution_model = load_model(
        RESOLUTION_MODEL
    )


    # =========================================================================
    # MODEL STATUS
    # =========================================================================

    st.subheader(
        "🧠 Model Status"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Severity Model",
            "Loaded"
            if severity_model
            else "Not Available"
        )


    with col2:

        st.metric(
            "Priority Model",
            "Loaded"
            if priority_model
            else "Not Available"
        )


    with col3:

        st.metric(
            "Resolution Model",
            "Loaded"
            if resolution_model
            else "Not Available"
        )


    st.markdown("---")


    # =========================================================================
    # BUG INPUT
    # =========================================================================

    st.subheader(
        "📝 Enter Bug Details"
    )


    bug_description = st.text_area(
        "Bug Description",
        height=180,
        placeholder="""
Example:

Application crashes when user uploads a large file.
Login page shows unexpected error.
Payment fails after clicking checkout.
"""
    )


    col1, col2 = st.columns(2)


    with col1:

        module = st.selectbox(
            "Module",
            sorted(
                df["Module"]
                .dropna()
                .unique()
                .tolist()
            )
        )


    with col2:

        developer = st.selectbox(
            "Developer",
            sorted(
                df["Developer"]
                .dropna()
                .unique()
                .tolist()
            )
        )


    st.markdown("---")
    # =========================================================================
    # PREDICT BUTTON
    # =========================================================================

    if st.button(
        "🚀 Predict Bug",
        width="stretch"
    ):


        if not bug_description.strip():

            st.warning(
                "Please enter bug description."
            )


        else:


            st.session_state.prediction_text = (
                bug_description
            )


            # ================================================================
            # SEVERITY PREDICTION
            # ================================================================

            if severity_model and tfidf_vectorizer:

                try:

                    X = tfidf_vectorizer.transform(
                        [bug_description]
                    )


                    severity_prediction = (
                        severity_model.predict(X)[0]
                    )


                except Exception:

                    severity_prediction = (
                        "Prediction Error"
                    )


            else:

                severity_prediction = (
                    "Model Not Available"
                )



            # ================================================================
            # PRIORITY PREDICTION
            # ================================================================

            if priority_model and priority_vectorizer:

                try:

                    X_priority = priority_vectorizer.transform(
                        [bug_description]
                    )


                    priority_prediction = (
                        priority_model.predict(X_priority)[0]
                    )


                except Exception:

                    priority_prediction = (
                        "Prediction Error"
                    )


            else:

                priority_prediction = (
                    "Model Not Available"
                )



            # ================================================================
            # RESOLUTION PREDICTION
            # ================================================================

            if resolution_model:

                try:

                    model = resolution_model["model"]

                    features = resolution_model["features"]


                    input_data = pd.DataFrame(
                        [
                            {
                                "Module": module,
                                "Developer": developer
                            }
                        ]
                    )


                    input_data = pd.get_dummies(
                        input_data
                    )


                    input_data = input_data.reindex(
                        columns=features,
                        fill_value=0
                    )


                    resolution_prediction = (
                        model.predict(input_data)[0]
                    )


                except Exception:

                    resolution_prediction = (
                        "Prediction Error"
                    )


            else:

                resolution_prediction = (
                    "Model Not Available"
                )



            # ================================================================
            # STORE RESULTS
            # ================================================================

            st.session_state.severity_result = (
                severity_prediction
            )


            st.session_state.priority_result = (
                priority_prediction
            )


            st.session_state.resolution_result = (
                resolution_prediction
            )


            # ================================================================
            # SAVE HISTORY
            # ================================================================

            st.session_state.prediction_history.append(
                {
                    "Bug Description": bug_description,
                    "Module": module,
                    "Developer": developer,
                    "Severity": severity_prediction,
                    "Priority": priority_prediction,
                    "Resolution": resolution_prediction
                }
            )
    # =========================================================================
    # DISPLAY RESULTS
    # =========================================================================

    if "severity_result" in st.session_state:


        st.markdown("---")


        st.subheader(
            "🎯 Prediction Results"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.success(
                f"Severity: {st.session_state.severity_result}"
            )


        with col2:

            st.info(
                f"Priority: {st.session_state.priority_result}"
            )


        with col3:

            try:

                resolution_hours = float(
                    st.session_state.resolution_result
                )


                resolution_days = round(
                    resolution_hours / 24,
                    2
                )


                st.warning(
                    f"Resolution: {resolution_hours:.2f} hours "
                    f"(≈ {resolution_days} days)"
                )


            except:

                st.warning(
                    f"Resolution: {st.session_state.resolution_result}"
                )


        st.markdown("---")


        st.subheader(
            "📄 Bug Summary"
        )


        st.text_area(
            "Bug Description",
            value=st.session_state.prediction_text,
            height=150,
            disabled=True
        )


        st.markdown("---")


        st.subheader(
            "📋 Prediction History"
        )


        history_df = pd.DataFrame(
            st.session_state.prediction_history
        )


        st.dataframe(
            history_df,
            width="stretch"
        )