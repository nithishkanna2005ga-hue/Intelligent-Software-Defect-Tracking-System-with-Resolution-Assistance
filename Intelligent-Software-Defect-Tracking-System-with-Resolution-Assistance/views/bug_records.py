"""
===============================================================================
Bug Records Page
Bug Life Cycle Management Dashboard
===============================================================================

Complete bug repository management with filtering, searching and exporting.
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.data_loader import get_dataframe


# =============================================================================
# BUG RECORDS PAGE
# =============================================================================

def show_bug_records():

    df = get_dataframe()

    st.header("📂 Bug Records")

    st.caption(
        "Search, filter and manage complete bug lifecycle records"
    )

    st.markdown("---")


    # =========================================================================
    # SUMMARY CARDS
    # =========================================================================

    total = len(df)

    open_count = (
        df[df["Status"] == "Open"]
        .shape[0]
    )

    critical = (
        df[df["Priority"] == "Critical"]
        .shape[0]
    )

    duplicate = (
        df[df["Duplicate"] == "Yes"]
        .shape[0]
        if "Duplicate" in df.columns
        else 0
    )


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Total Records",
        total,
    )


    c2.metric(
        "Open Bugs",
        open_count,
    )


    c3.metric(
        "Critical Bugs",
        critical,
    )


    c4.metric(
        "Duplicates",
        duplicate,
    )


    st.markdown("---")


    # =========================================================================
    # SEARCH
    # =========================================================================

    st.subheader("🔍 Search Bugs")


    search_text = st.text_input(
        "Search by Bug ID, Developer or Module"
    )


    filtered_df = df.copy()


    if search_text:

        search_text = search_text.lower()


        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(
                lambda row:
                row.str.lower()
                .str.contains(
                    search_text
                )
                .any(),
                axis=1,
            )
        ]


    st.info(
        f"Showing {len(filtered_df)} records"
    )


    st.markdown("---")
    # =========================================================================
    # ADVANCED FILTERS
    # =========================================================================

    st.subheader("🎯 Advanced Filters")


    filter_col1, filter_col2 = st.columns(2)

    filter_col3, filter_col4 = st.columns(2)


    # -------------------------------------------------------------------------
    # Status Filter
    # -------------------------------------------------------------------------

    with filter_col1:

        status_filter = st.multiselect(

            "Status",

            sorted(
                df["Status"]
                .unique()
                .tolist()
            ),

            default=df["Status"]
            .unique()
            .tolist(),

        )


    # -------------------------------------------------------------------------
    # Priority Filter
    # -------------------------------------------------------------------------

    with filter_col2:

        priority_filter = st.multiselect(

            "Priority",

            sorted(
                df["Priority"]
                .unique()
                .tolist()
            ),

            default=df["Priority"]
            .unique()
            .tolist(),

        )


    # -------------------------------------------------------------------------
    # Severity Filter
    # -------------------------------------------------------------------------

    with filter_col3:

        severity_filter = st.multiselect(

            "Severity",

            sorted(
                df["Severity"]
                .unique()
                .tolist()
            ),

            default=df["Severity"]
            .unique()
            .tolist(),

        )


    # -------------------------------------------------------------------------
    # Module Filter
    # -------------------------------------------------------------------------

    with filter_col4:

        module_filter = st.multiselect(

            "Module",

            sorted(
                df["Module"]
                .unique()
                .tolist()
            ),

            default=df["Module"]
            .unique()
            .tolist(),

        )


    # =========================================================================
    # APPLY FILTERS
    # =========================================================================

    filtered_df = filtered_df[

        filtered_df["Status"]
        .isin(status_filter)

        &

        filtered_df["Priority"]
        .isin(priority_filter)

        &

        filtered_df["Severity"]
        .isin(severity_filter)

        &

        filtered_df["Module"]
        .isin(module_filter)

    ]


    st.success(

        f"{len(filtered_df)} matching records found"

    )


    st.markdown("---")


    # =========================================================================
    # QUICK SORTING
    # =========================================================================

    st.subheader("↕ Sort Records")


    sort_column = st.selectbox(

        "Sort By",

        filtered_df.columns,

    )


    ascending = st.toggle(

        "Ascending Order",

        value=True,

    )


    filtered_df = filtered_df.sort_values(

        by=sort_column,

        ascending=ascending,

    )
    # =========================================================================
    # COLUMN SELECTION
    # =========================================================================

    st.subheader("📋 Bug Data Table")


    available_columns = filtered_df.columns.tolist()


    selected_columns = st.multiselect(

        "Select Columns to Display",

        available_columns,

        default=available_columns,

    )


    display_df = filtered_df[selected_columns]


    # =========================================================================
    # PAGINATION
    # =========================================================================

    records_per_page = st.selectbox(

        "Records Per Page",

        [10, 25, 50, 100],

        index=1,

    )


    total_pages = max(

        1,

        (len(display_df) - 1)
        // records_per_page
        + 1

    )


    if "bug_page" not in st.session_state:

        st.session_state.bug_page = 1


    page_number = st.number_input(

        "Page",

        min_value=1,

        max_value=total_pages,

        value=st.session_state.bug_page,

    )


    st.session_state.bug_page = page_number


    start_index = (

        page_number - 1

    ) * records_per_page


    end_index = (

        start_index

        + records_per_page

    )


    page_df = display_df.iloc[
        start_index:end_index
    ]


    st.dataframe(

        page_df,

        use_container_width=True,

        height=450,

    )


    st.caption(

        f"Page {page_number} of {total_pages}"

    )


    st.markdown("---")


    # =========================================================================
    # BUG DETAILS VIEW
    # =========================================================================

    st.subheader("🔎 Bug Details")


    if not filtered_df.empty:


        selected_bug = st.selectbox(

            "Select Bug ID",

            filtered_df["Bug ID"]

            .tolist(),

        )


        bug_details = filtered_df[

            filtered_df["Bug ID"]

            == selected_bug

        ].iloc[0]


        detail_col1, detail_col2 = st.columns(2)


        with detail_col1:

            st.write(
                "**Bug ID:**",
                bug_details["Bug ID"]
            )

            st.write(
                "**Status:**",
                bug_details["Status"]
            )

            st.write(
                "**Priority:**",
                bug_details["Priority"]
            )

            st.write(
                "**Severity:**",
                bug_details["Severity"]
            )


        with detail_col2:

            st.write(
                "**Developer:**",
                bug_details["Developer"]
            )

            st.write(
                "**Module:**",
                bug_details["Module"]
            )

            st.write(
                "**Resolution Days:**",
                bug_details["Resolution Days"]
            )

            st.write(
                "**Resolution:**",
                bug_details["Resolution"]
            )


    st.markdown("---")
    # =========================================================================
    # DATA QUALITY CHECKS
    # =========================================================================

    st.subheader("🧹 Data Quality Analysis")


    quality_col1, quality_col2, quality_col3 = st.columns(3)


    with quality_col1:

        missing_values = (
            filtered_df
            .isnull()
            .sum()
            .sum()
        )


        st.metric(
            "Missing Values",
            missing_values,
        )


    with quality_col2:

        duplicate_records = (
            filtered_df
            .duplicated()
            .sum()
        )


        st.metric(
            "Duplicate Records",
            duplicate_records,
        )


    with quality_col3:

        total_columns = (
            filtered_df
            .shape[1]
        )


        st.metric(
            "Total Columns",
            total_columns,
        )


    st.markdown("---")


    # =========================================================================
    # MISSING VALUE REPORT
    # =========================================================================

    with st.expander(
        "View Missing Value Report"
    ):

        missing_report = (

            filtered_df

            .isnull()

            .sum()

            .reset_index()

        )


        missing_report.columns = [

            "Column",

            "Missing Count",

        ]


        st.dataframe(

            missing_report,

            use_container_width=True,

        )


    # =========================================================================
    # EXPORT FILTERED RECORDS
    # =========================================================================

    st.subheader("📥 Export Bug Records")


    csv_file = (

        filtered_df

        .to_csv(index=False)

        .encode("utf-8")

    )


    st.download_button(

        label="Download Filtered Bug Records",

        data=csv_file,

        file_name="filtered_bug_records.csv",

        mime="text/csv",

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # FINAL STATUS
    # =========================================================================

    st.success(

        "Bug record analysis completed successfully."

    )
    