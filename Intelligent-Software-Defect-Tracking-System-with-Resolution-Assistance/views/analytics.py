"""
===============================================================================
Analytics Page
Bug Life Cycle Management Dashboard
===============================================================================

Advanced analytics and quality insights.
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.data_loader import get_dataframe


# =============================================================================
# PAGE STYLE
# =============================================================================

def apply_analytics_style():

    st.markdown(
        """
        <style>

        html, body, [class*="css"] {
            font-size: 20px;
            font-weight: 600;
        }

        h1 {
            font-size: 42px !important;
            font-weight: 900 !important;
        }

        h2 {
            font-size: 32px !important;
            font-weight: 900 !important;
        }

        h3 {
            font-size: 26px !important;
            font-weight: 800 !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 32px !important;
            font-weight: 900 !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 20px !important;
            font-weight: 800 !important;
        }

        button {
            font-size: 18px !important;
            font-weight: 800 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# ANALYTICS PAGE
# =============================================================================

def show_analytics():


    apply_analytics_style()


    df = get_dataframe()


    st.title("📈 Bug Life Cycle Analytics Dashboard")


    st.markdown(
        """
        <h3>
        Advanced analysis of bug quality, priority,
        severity and developer performance
        </h3>
        """,
        unsafe_allow_html=True
    )


    st.divider()



    # =========================================================================
    # KPI SECTION
    # =========================================================================


    total_bugs = len(df)


    duplicate_count = (
        df[df["Duplicate"] == "Yes"].shape[0]
        if "Duplicate" in df.columns
        else 0
    )


    avg_resolution = round(
        df["Resolution Days"].mean(),
        2
    )


    high_priority = (
        df[
            df["Priority"].isin(
                [
                    "High",
                    "Critical"
                ]
            )
        ].shape[0]
    )



    col1,col2,col3,col4 = st.columns(4)


    col1.metric(
        "Total Bugs",
        total_bugs
    )


    col2.metric(
        "High Priority",
        high_priority
    )


    col3.metric(
        "Duplicates",
        duplicate_count
    )


    col4.metric(
        "Avg Resolution",
        f"{avg_resolution} Days"
    )


    st.divider()



    # =========================================================================
    # FILTER SECTION
    # =========================================================================


    st.header("🔍 Analytics Filters")


    c1,c2 = st.columns(2)


    with c1:

        priority_filter = st.multiselect(
            "Select Priority",
            df["Priority"].unique(),
            default=df["Priority"].unique()
        )


    with c2:

        severity_filter = st.multiselect(
            "Select Severity",
            df["Severity"].unique(),
            default=df["Severity"].unique()
        )


    filtered_df = df[
        df["Priority"].isin(priority_filter)
        &
        df["Severity"].isin(severity_filter)
    ]


    st.success(
        f"Showing {len(filtered_df)} bug records"
    )


    st.divider()
    # =========================================================================
    # PRIORITY VS SEVERITY HEATMAP
    # =========================================================================


    st.header("🔥 Priority vs Severity Analysis")


    heatmap_data = (
        filtered_df
        .groupby(
            [
                "Priority",
                "Severity"
            ]
        )
        .size()
        .reset_index(
            name="Bug Count"
        )
    )


    heatmap_table = (
        heatmap_data
        .pivot(
            index="Priority",
            columns="Severity",
            values="Bug Count"
        )
        .fillna(0)
    )


    fig_heatmap = px.imshow(
        heatmap_table,
        text_auto=True,
        aspect="auto",
        title="Bug Distribution Heatmap"
    )


    fig_heatmap.update_layout(
        height=500,
        title_font_size=26
    )


    st.plotly_chart(
        fig_heatmap,
        use_container_width=True,
        key="priority_severity_heatmap"
    )


    st.divider()



    # =========================================================================
    # STATUS ANALYSIS
    # =========================================================================


    st.header("📊 Bug Status Analytics")


    status_df = (
        filtered_df["Status"]
        .value_counts()
        .reset_index()
    )


    status_df.columns = [
        "Status",
        "Count"
    ]


    fig_status = px.bar(
        status_df,
        x="Status",
        y="Count",
        text="Count",
        color="Status",
        title="Current Bug Status Distribution"
    )


    fig_status.update_layout(
        height=500,
        title_font_size=26
    )


    st.plotly_chart(
        fig_status,
        use_container_width=True,
        key="bug_status_chart"
    )


    st.divider()



    # =========================================================================
    # RESOLUTION PERFORMANCE
    # =========================================================================


    st.header("⏱ Resolution Performance")


    resolution_df = (
        filtered_df
        .groupby("Priority")
        ["Resolution Days"]
        .mean()
        .reset_index()
    )


    resolution_df.columns = [
        "Priority",
        "Average Resolution Days"
    ]


    fig_resolution = px.bar(
        resolution_df,
        x="Priority",
        y="Average Resolution Days",
        text_auto=".2f",
        color="Priority",
        title="Average Resolution Time By Priority"
    )


    fig_resolution.update_layout(
        height=500,
        title_font_size=26
    )


    st.plotly_chart(
        fig_resolution,
        use_container_width=True,
        key="resolution_time_chart"
    )


    st.divider()
    # =========================================================================
    # MODULE-WISE BUG ANALYSIS
    # =========================================================================


    st.header("📂 Module-wise Bug Analysis")


    module_df = (
        filtered_df["Module"]
        .value_counts()
        .reset_index()
    )


    module_df.columns = [
        "Module",
        "Bug Count"
    ]


    fig_module = px.bar(
        module_df,
        x="Module",
        y="Bug Count",
        text="Bug Count",
        color="Bug Count",
        title="Bugs Reported By Module"
    )


    fig_module.update_layout(
        height=500,
        title_font_size=26
    )


    st.plotly_chart(
        fig_module,
        use_container_width=True,
        key="module_analysis_chart"
    )


    st.divider()



    # =========================================================================
    # DEVELOPER PERFORMANCE
    # =========================================================================


    st.header("👨‍💻 Developer Performance")


    developer_df = (
        filtered_df
        .groupby("Developer")
        .agg(
            Assigned_Bugs=(
                "Bug ID",
                "count"
            ),

            Avg_Resolution=(
                "Resolution Days",
                "mean"
            )
        )
        .reset_index()
    )


    developer_df["Avg_Resolution"] = (
        developer_df["Avg_Resolution"]
        .round(2)
    )


    fig_developer = px.scatter(
        developer_df,
        x="Assigned_Bugs",
        y="Avg_Resolution",
        size="Assigned_Bugs",
        hover_name="Developer",
        title="Developer Workload vs Resolution Time"
    )


    fig_developer.update_layout(
        height=500,
        title_font_size=26
    )


    st.plotly_chart(
        fig_developer,
        use_container_width=True,
        key="developer_performance_chart"
    )


    st.divider()



    # =========================================================================
    # BUG REPORTING TREND
    # =========================================================================


    st.header("📅 Bug Reporting Trend")


    trend_df = filtered_df.copy()


    trend_df["Month"] = (
        trend_df["Created Date"]
        .dt.to_period("M")
        .astype(str)
    )


    monthly_bug = (
        trend_df
        .groupby("Month")
        .size()
        .reset_index(
            name="Bug Count"
        )
    )


    fig_month = px.line(
        monthly_bug,
        x="Month",
        y="Bug Count",
        markers=True,
        title="Monthly Bug Reporting Trend"
    )


    fig_month.update_layout(
        height=500,
        title_font_size=26
    )


    st.plotly_chart(
        fig_month,
        use_container_width=True,
        key="bug_trend_chart"
    )


    st.divider()
    # =========================================================================
    # AUTOMATED INSIGHTS
    # =========================================================================


    st.header("📌 Automated Analytics Insights")


    insight_col1, insight_col2 = st.columns(2)



    # -------------------------------------------------------------------------
    # MOST AFFECTED MODULE
    # -------------------------------------------------------------------------


    with insight_col1:


        top_module = (
            filtered_df["Module"]
            .value_counts()
            .idxmax()
        )


        top_module_count = (
            filtered_df["Module"]
            .value_counts()
            .max()
        )


        st.info(
            f"""
            ### 📂 Most Affected Module

            **{top_module}**

            Total Bugs:
            **{top_module_count}**
            """
        )



    # -------------------------------------------------------------------------
    # SLOW RESOLUTION MODULE
    # -------------------------------------------------------------------------


    with insight_col2:


        slow_module = (
            filtered_df
            .groupby("Module")["Resolution Days"]
            .mean()
            .idxmax()
        )


        slow_time = round(
            filtered_df
            .groupby("Module")["Resolution Days"]
            .mean()
            .max(),
            2
        )


        st.warning(
            f"""
            ### ⏱ Slowest Resolution Module

            **{slow_module}**

            Average Time:

            **{slow_time} Days**
            """
        )


    st.divider()



    # =========================================================================
    # ANALYTICS SUMMARY TABLE
    # =========================================================================


    st.header("📋 Analytics Summary")


    summary_df = (
        filtered_df
        .groupby("Priority")
        .agg(

            Total_Bugs=(
                "Bug ID",
                "count"
            ),

            Avg_Resolution_Days=(
                "Resolution Days",
                "mean"
            )
        )
        .reset_index()
    )


    summary_df[
        "Avg_Resolution_Days"
    ] = (
        summary_df[
            "Avg_Resolution_Days"
        ]
        .round(2)
    )



    st.dataframe(
        summary_df,
        use_container_width=True,
        height=400
    )


    st.divider()



    # =========================================================================
    # EXPORT REPORT
    # =========================================================================


    st.header("📥 Export Analytics Report")


    csv_data = (
        summary_df
        .to_csv(
            index=False
        )
        .encode("utf-8")
    )


    st.download_button(

        label="⬇ Download Analytics CSV",

        data=csv_data,

        file_name="Bug_Analytics_Report.csv",

        mime="text/csv",

        use_container_width=True
    )


    st.divider()



    st.success(
        "✅ Analytics Dashboard Completed Successfully"
    )
