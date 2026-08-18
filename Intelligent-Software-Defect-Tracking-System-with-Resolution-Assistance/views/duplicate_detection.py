"""
===============================================================================
Duplicate Detection Page
Bug Life Cycle Management Dashboard
===============================================================================

AI-assisted duplicate bug report detection using text similarity.
===============================================================================
"""

from __future__ import annotations

import re

import pandas as pd
import streamlit as st

from utils.data_loader import get_dataframe


# =============================================================================
# TEXT PREPROCESSING
# =============================================================================

def clean_text(text):

    if pd.isna(text):

        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text,
    )

    text = " ".join(
        text.split()
    )

    return text


# =============================================================================
# SIMILARITY FUNCTION
# =============================================================================

def calculate_similarity(text1, text2):

    from sklearn.feature_extraction.text import TfidfVectorizer

    from sklearn.metrics.pairwise import cosine_similarity


    documents = [

        clean_text(text1),

        clean_text(text2),

    ]


    vectorizer = TfidfVectorizer()


    vectors = vectorizer.fit_transform(
        documents
    )


    similarity = cosine_similarity(

        vectors[0],

        vectors[1]

    )[0][0]


    return round(

        similarity * 100,

        2

    )


# =============================================================================
# DUPLICATE DETECTION PAGE
# =============================================================================

def show_duplicate_detection():

    df = get_dataframe()


    st.header("🔍 Duplicate Bug Detection")


    st.caption(

        "Compare bug descriptions and identify possible duplicate reports"

    )


    st.markdown("---")


    # =========================================================================
    # INPUT AREA
    # =========================================================================

    st.subheader("📝 Compare Bug Reports")


    col1, col2 = st.columns(2)


    with col1:

        bug1 = st.text_area(

            "Bug Report 1",

            placeholder=

            "Enter first bug description..."

        )


    with col2:

        bug2 = st.text_area(

            "Bug Report 2",

            placeholder=

            "Enter second bug description..."

        )


    st.markdown("---")
    # =========================================================================
    # DUPLICATE ANALYSIS
    # =========================================================================

    if st.button(

        "🔍 Check Duplicate",

        use_container_width=True,

    ):


        if not bug1 or not bug2:

            st.warning(

                "Please enter both bug reports."

            )


        else:

            similarity = calculate_similarity(

                bug1,

                bug2,

            )


            st.session_state.similarity_score = similarity


            st.markdown("---")


            st.subheader(

                "🧠 Similarity Result"

            )


            result_col1, result_col2 = st.columns(2)


            with result_col1:


                st.metric(

                    "Similarity Score",

                    f"{similarity}%",

                )


            with result_col2:


                if similarity >= 75:


                    st.error(

                        "⚠ Possible Duplicate Bug"

                    )


                elif similarity >= 45:


                    st.warning(

                        "⚡ Similar Bugs Detected"

                    )


                else:


                    st.success(

                        "✅ Not Duplicate"

                    )


            st.progress(

                int(similarity)

                / 100

            )


            st.markdown("---")


            # =================================================================
            # EXPLANATION
            # =================================================================

            if similarity >= 75:

                st.info(

                    """
The two bug reports have a high text similarity.
They should be reviewed before creating a new bug.
"""

                )


            elif similarity >= 45:

                st.info(

                    """
The reports contain similar keywords.
Manual verification is recommended.
"""

                )


            else:

                st.info(

                    """
The reports appear different based on text similarity.
"""

                )


    st.markdown("---")
    # =========================================================================
    # EXISTING BUG SIMILARITY SEARCH
    # =========================================================================

    st.subheader("📂 Search Similar Existing Bugs")


    if "Description" in df.columns:

        search_bug = st.text_area(

            "Enter New Bug Description",

            placeholder=
            "Describe the new bug to find similar reports..."

        )


        if st.button(

            "🔎 Find Similar Bugs",

            use_container_width=True,

        ):


            if not search_bug:


                st.warning(

                    "Enter a bug description first."

                )


            else:

                from sklearn.feature_extraction.text import TfidfVectorizer

                from sklearn.metrics.pairwise import cosine_similarity


                descriptions = (

                    df["Description"]

                    .fillna("")

                    .apply(clean_text)

                    .tolist()

                )


                descriptions.append(

                    clean_text(search_bug)

                )


                vectorizer = TfidfVectorizer()


                vectors = vectorizer.fit_transform(

                    descriptions

                )


                similarity_scores = cosine_similarity(

                    vectors[-1],

                    vectors[:-1]

                )[0]


                result = df.copy()


                result["Similarity Score"] = (

                    similarity_scores * 100

                ).round(2)


                result = result.sort_values(

                    "Similarity Score",

                    ascending=False,

                )


                st.success(

                    "Similar bug reports found."

                )


                st.dataframe(

                    result.head(10),

                    use_container_width=True,

                )


    else:

        st.info(

            """
Your dataset does not contain a Description column.

Add a Description field to enable
existing bug similarity search.
"""

        )


    st.markdown("---")


    # =========================================================================
    # DUPLICATE STATISTICS
    # =========================================================================

    st.subheader("📊 Duplicate Statistics")


    if "Duplicate" in df.columns:


        duplicate_count = (

            df[df["Duplicate"] == "Yes"]

            .shape[0]

        )


        normal_count = (

            df[df["Duplicate"] == "No"]

            .shape[0]

        )


        col1, col2 = st.columns(2)


        col1.metric(

            "Duplicate Bugs",

            duplicate_count,

        )


        col2.metric(

            "Unique Bugs",

            normal_count,

        )


    else:

        st.info(

            "Duplicate label column not available in dataset."

        )


    st.markdown("---")
    # =========================================================================
    # DETECTION HISTORY
    # =========================================================================

    st.subheader("📝 Detection History")


    if "duplicate_history" not in st.session_state:

        st.session_state.duplicate_history = []


    if "similarity_score" in st.session_state:


        history_record = {

            "Similarity Score":

            f"{st.session_state.similarity_score}%"

        }


        if history_record not in st.session_state.duplicate_history:

            st.session_state.duplicate_history.append(

                history_record

            )


    if st.session_state.duplicate_history:


        history_df = pd.DataFrame(

            st.session_state.duplicate_history

        )


        st.dataframe(

            history_df,

            use_container_width=True,

        )


    else:

        st.info(

            "No duplicate detection history available."

        )


    st.markdown("---")


    # =========================================================================
    # AI RECOMMENDATION PANEL
    # =========================================================================

    st.subheader("🤖 AI Recommendation")


    if "similarity_score" in st.session_state:


        score = st.session_state.similarity_score


        if score >= 75:


            recommendation = (

                "High similarity detected. "
                "Review existing bugs before creating a new issue."

            )


        elif score >= 45:


            recommendation = (

                "Moderate similarity detected. "
                "Perform manual verification."

            )


        else:


            recommendation = (

                "Low similarity. "
                "Bug appears to be a new issue."

            )


        st.info(

            recommendation

        )


    else:

        st.info(

            "Run duplicate detection to generate AI recommendations."

        )


    st.markdown("---")


    # =========================================================================
    # EXPORT REPORT
    # =========================================================================

    st.subheader("📥 Export Detection Report")


    if "similarity_score" in st.session_state:


        export_df = pd.DataFrame(

            {

                "Similarity Score":

                [

                    st.session_state.similarity_score

                ]

            }

        )


        csv = export_df.to_csv(

            index=False

        ).encode("utf-8")


        st.download_button(

            label="Download Duplicate Report",

            data=csv,

            file_name="duplicate_detection_report.csv",

            mime="text/csv",

            use_container_width=True,

        )


    st.success(

        "Duplicate detection analysis completed successfully."

    )