"""
===============================================================================
Trends Page
Bug Life Cycle Management Dashboard
===============================================================================

Time-based bug reporting and pattern analysis.
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.data_loader import get_dataframe


# =============================================================================
# TRENDS PAGE
# =============================================================================

def show_trends():

    df = get_dataframe()

    st.header("📉 Bug Trends Analysis")

    st.caption(
        "Analyze bug growth patterns, reporting trends and lifecycle behavior"
    )

    st.markdown("---")


    # =========================================================================
    # DATE PREPARATION
    # =========================================================================

    trend_df = df.copy()


    trend_df["Created Date"] = pd.to_datetime(
        trend_df["Created Date"],
        errors="coerce",
    )


    trend_df["Month"] = (

        trend_df["Created Date"]

        .dt.to_period("M")

        .astype(str)

    )


    # =========================================================================
    # KPI SECTION
    # =========================================================================

    total_bugs = len(trend_df)


    months = (
        trend_df["Month"]
        .nunique()
    )


    avg_monthly = round(

        total_bugs / months,

        2

    )


    latest_month = (

        trend_df["Month"]

        .value_counts()

        .idxmax()

    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "Total Bugs",
        total_bugs,
    )


    c2.metric(
        "Average Monthly Bugs",
        avg_monthly,
    )


    c3.metric(
        "Peak Reporting Month",
        latest_month,
    )


    st.markdown("---")


    # =========================================================================
    # FILTERS
    # =========================================================================

    st.subheader("🔍 Trend Filters")


    col1, col2 = st.columns(2)


    with col1:

        selected_module = st.multiselect(

            "Module",

            sorted(
                trend_df["Module"]
                .unique()
                .tolist()
            ),

            default=trend_df["Module"]
            .unique()
            .tolist(),

        )


    with col2:

        selected_priority = st.multiselect(

            "Priority",

            sorted(
                trend_df["Priority"]
                .unique()
                .tolist()
            ),

            default=trend_df["Priority"]
            .unique()
            .tolist(),

        )


    filtered_df = trend_df[

        trend_df["Module"]
        .isin(selected_module)

        &

        trend_df["Priority"]
        .isin(selected_priority)

    ]


    st.info(
        f"Analysing {len(filtered_df)} bug records"
    )


    st.markdown("---")
    # =========================================================================
    # MONTHLY BUG REPORTING TREND
    # =========================================================================

    st.subheader("📈 Monthly Bug Reporting Trend")


    monthly_trend = (

        filtered_df

        .groupby("Month")

        .size()

        .reset_index(
            name="Bug Count"
        )

    )


    fig_monthly = px.line(

        monthly_trend,

        x="Month",

        y="Bug Count",

        markers=True,

        title="Monthly Bug Creation Trend",

    )


    fig_monthly.update_layout(

        height=430,

        xaxis_title="Month",

        yaxis_title="Number of Bugs",

    )


    st.plotly_chart(

        fig_monthly,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # STATUS TREND ANALYSIS
    # =========================================================================

    st.subheader("📊 Status Movement Over Time")


    status_trend = (

        filtered_df

        .groupby(

            [

                "Month",

                "Status"

            ]

        )

        .size()

        .reset_index(

            name="Count"

        )

    )


    fig_status = px.area(

        status_trend,

        x="Month",

        y="Count",

        color="Status",

        title="Bug Status Trend",

    )


    fig_status.update_layout(

        height=450,

    )


    st.plotly_chart(

        fig_status,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # PRIORITY TREND ANALYSIS
    # =========================================================================

    st.subheader("🔥 Priority Trend Analysis")


    priority_trend = (

        filtered_df

        .groupby(

            [

                "Month",

                "Priority"

            ]

        )

        .size()

        .reset_index(

            name="Count"

        )

    )


    fig_priority = px.bar(

        priority_trend,

        x="Month",

        y="Count",

        color="Priority",

        barmode="group",

        title="Priority-wise Bug Trend",

    )


    fig_priority.update_layout(

        height=450,

    )


    st.plotly_chart(

        fig_priority,

        use_container_width=True,

    )


    st.markdown("---")
    # =========================================================================
    # MODULE GROWTH TREND
    # =========================================================================

    st.subheader("📂 Module Growth Analysis")


    module_trend = (

        filtered_df

        .groupby(

            [

                "Month",

                "Module"

            ]

        )

        .size()

        .reset_index(

            name="Bug Count"

        )

    )


    fig_module = px.line(

        module_trend,

        x="Month",

        y="Bug Count",

        color="Module",

        markers=True,

        title="Module-wise Bug Growth",

    )


    fig_module.update_layout(

        height=450,

    )


    st.plotly_chart(

        fig_module,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # DEVELOPER TREND ANALYSIS
    # =========================================================================

    st.subheader("👨‍💻 Developer Bug Handling Trend")


    developer_trend = (

        filtered_df

        .groupby(

            [

                "Month",

                "Developer"

            ]

        )

        .size()

        .reset_index(

            name="Resolved / Assigned Bugs"

        )

    )


    fig_developer = px.area(

        developer_trend,

        x="Month",

        y="Resolved / Assigned Bugs",

        color="Developer",

        title="Developer Workload Trend",

    )


    fig_developer.update_layout(

        height=450,

    )


    st.plotly_chart(

        fig_developer,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # CRITICAL BUG MONITORING
    # =========================================================================

    st.subheader("🚨 Critical Bug Monitoring")


    critical_df = filtered_df[

        filtered_df["Priority"]

        .isin(

            [

                "High",

                "Critical"

            ]

        )

    ]


    critical_trend = (

        critical_df

        .groupby("Month")

        .size()

        .reset_index(

            name="Critical Bugs"

        )

    )


    fig_critical = px.area(

        critical_trend,

        x="Month",

        y="Critical Bugs",

        title="High/Critical Bug Trend",

    )


    fig_critical.update_layout(

        height=420,

    )


    st.plotly_chart(

        fig_critical,

        use_container_width=True,

    )


    st.markdown("---")
    # =========================================================================
    # AUTOMATED TREND INSIGHTS
    # =========================================================================

    st.subheader("📌 Trend Insights")


    insight_col1, insight_col2 = st.columns(2)


    # -------------------------------------------------------------------------
    # Peak Month
    # -------------------------------------------------------------------------

    with insight_col1:

        peak_month = (

            filtered_df["Month"]

            .value_counts()

            .idxmax()

        )


        peak_count = (

            filtered_df["Month"]

            .value_counts()

            .max()

        )


        st.info(

            f"""
### 📅 Peak Bug Reporting Period

Month:

**{peak_month}**

Reported Bugs:

**{peak_count}**
"""

        )


    # -------------------------------------------------------------------------
    # Most Problematic Module
    # -------------------------------------------------------------------------

    with insight_col2:

        problem_module = (

            filtered_df["Module"]

            .value_counts()

            .idxmax()

        )


        problem_count = (

            filtered_df["Module"]

            .value_counts()

            .max()

        )


        st.warning(

            f"""
### ⚠ Problematic Module

Module:

**{problem_module}**

Total Bugs:

**{problem_count}**
"""

        )


    st.markdown("---")


    # =========================================================================
    # TREND SUMMARY TABLE
    # =========================================================================

    st.subheader("📋 Monthly Trend Summary")


    summary = (

        filtered_df

        .groupby("Month")

        .agg(

            Total_Bugs=(
                "Bug ID",
                "count"
            ),

            Avg_Resolution=(
                "Resolution Days",
                "mean"
            ),

        )

        .reset_index()

    )


    summary[
        "Avg_Resolution"
    ] = (

        summary[
            "Avg_Resolution"
        ]

        .round(2)

    )


    st.dataframe(

        summary,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # EXPORT TREND REPORT
    # =========================================================================

    st.subheader("📥 Export Trend Analysis")


    csv_report = (

        summary

        .to_csv(index=False)

        .encode("utf-8")

    )


    st.download_button(

        label="Download Trend Report",

        data=csv_report,

        file_name="bug_trend_report.csv",

        mime="text/csv",

        use_container_width=True,

    )


    st.success(

        "Trend analysis completed successfully."

    )
