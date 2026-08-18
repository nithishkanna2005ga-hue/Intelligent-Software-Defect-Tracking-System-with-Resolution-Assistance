"""
===============================================================================
Resolution Intelligence Page
Bug Life Cycle Management Dashboard
===============================================================================

Analyzes bug resolution performance, SLA compliance and bottlenecks.
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px

from utils.data_loader import get_dataframe


# =============================================================================
# RESOLUTION INTELLIGENCE PAGE
# =============================================================================

def show_resolution_time():

    df = get_dataframe()

    st.header("⏱ Resolution Intelligence")

    st.caption(
        "Analyze bug fixing speed, SLA performance and resolution bottlenecks"
    )

    st.markdown("---")


    # =========================================================================
    # KPI SECTION
    # =========================================================================

    total_bugs = len(df)


    average_resolution = round(
        df["Resolution Days"].mean(),
        2
    )


    fastest_resolution = (
        df["Resolution Days"]
        .min()
    )


    slowest_resolution = (
        df["Resolution Days"]
        .max()
    )


    resolved_bugs = (
        df[df["Status"] == "Resolved"]
        .shape[0]
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Bugs",
        total_bugs,
    )


    col2.metric(
        "Average Resolution",
        f"{average_resolution} Days",
    )


    col3.metric(
        "Fastest Fix",
        f"{fastest_resolution} Day",
    )


    col4.metric(
        "Slowest Fix",
        f"{slowest_resolution} Days",
    )


    st.markdown("---")


    # =========================================================================
    # FILTERS
    # =========================================================================

    st.subheader("🔍 Resolution Filters")


    filter1, filter2 = st.columns(2)


    with filter1:

        selected_priority = st.multiselect(
            "Priority",
            df["Priority"].unique(),
            default=df["Priority"].unique(),
        )


    with filter2:

        selected_module = st.multiselect(
            "Module",
            df["Module"].unique(),
            default=df["Module"].unique(),
        )


    filtered_df = df[
        (df["Priority"].isin(selected_priority))
        &
        (df["Module"].isin(selected_module))
    ]


    st.info(
        f"Analysing {len(filtered_df)} bug records"
    )


    st.markdown("---")
    # =========================================================================
    # RESOLUTION TIME DISTRIBUTION
    # =========================================================================

    st.subheader("📊 Resolution Time Distribution")


    fig_distribution = px.histogram(

        filtered_df,

        x="Resolution Days",

        nbins=20,

        title="Bug Resolution Time Frequency",

        text_auto=True,

    )


    fig_distribution.update_layout(

        height=420,

        xaxis_title="Resolution Days",

        yaxis_title="Number of Bugs",

    )


    st.plotly_chart(

        fig_distribution,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # SLA PERFORMANCE
    # =========================================================================

    st.subheader("🎯 SLA Performance Analysis")


    sla_limit = st.slider(

        "Set SLA Resolution Limit (Days)",

        min_value=1,

        max_value=30,

        value=7,

    )


    filtered_df = filtered_df.copy()


    filtered_df["SLA Status"] = (

        filtered_df["Resolution Days"]

        .apply(

            lambda x:

            "Within SLA"

            if x <= sla_limit

            else "SLA Breached"

        )

    )


    sla_count = (

        filtered_df["SLA Status"]

        .value_counts()

        .reset_index()

    )


    sla_count.columns = [

        "SLA Status",

        "Count",

    ]


    fig_sla = px.pie(

        sla_count,

        names="SLA Status",

        values="Count",

        hole=0.45,

        title="SLA Compliance",

    )


    fig_sla.update_layout(

        height=420,

    )


    st.plotly_chart(

        fig_sla,

        use_container_width=True,

    )


    st.markdown("---")
    # =========================================================================
    # MODULE RESOLUTION ANALYSIS
    # =========================================================================

    st.subheader("📂 Module Resolution Performance")


    module_resolution = (

        filtered_df

        .groupby("Module")

        .agg(

            Average_Days=(
                "Resolution Days",
                "mean",
            ),

            Total_Bugs=(
                "Bug ID",
                "count",
            ),

        )

        .reset_index()

    )


    module_resolution["Average_Days"] = (

        module_resolution["Average_Days"]

        .round(2)

    )


    fig_module = px.bar(

        module_resolution,

        x="Module",

        y="Average_Days",

        text="Average_Days",

        color="Average_Days",

        title="Average Resolution Time by Module",

    )


    fig_module.update_layout(

        height=430,

        yaxis_title="Average Days",

    )


    st.plotly_chart(

        fig_module,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # DEVELOPER PERFORMANCE
    # =========================================================================

    st.subheader("👨‍💻 Developer Resolution Performance")


    developer_resolution = (

        filtered_df

        .groupby("Developer")

        .agg(

            Fixed_Bugs=(
                "Bug ID",
                "count",
            ),

            Average_Fix_Time=(
                "Resolution Days",
                "mean",
            ),

        )

        .reset_index()

    )


    developer_resolution[
        "Average_Fix_Time"
    ] = (

        developer_resolution[
            "Average_Fix_Time"
        ]

        .round(2)

    )


    fig_developer = px.scatter(

        developer_resolution,

        x="Fixed_Bugs",

        y="Average_Fix_Time",

        size="Fixed_Bugs",

        hover_name="Developer",

        title="Developer Efficiency Analysis",

    )


    fig_developer.update_layout(

        height=430,

    )


    st.plotly_chart(

        fig_developer,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # BOTTLENECK IDENTIFICATION
    # =========================================================================

    st.subheader("🚨 Resolution Bottlenecks")


    bottleneck = (

        filtered_df

        .groupby("Module")

        ["Resolution Days"]

        .mean()

        .sort_values(

            ascending=False

        )

        .reset_index()

    )


    bottleneck.columns = [

        "Module",

        "Average Resolution Days",

    ]


    st.dataframe(

        bottleneck,

        use_container_width=True,

    )


    st.markdown("---")
    # =========================================================================
    # RESOLUTION TREND ANALYSIS
    # =========================================================================

    st.subheader("📈 Resolution Trend Analysis")


    trend_df = filtered_df.copy()


    trend_df["Month"] = (

        trend_df["Created Date"]

        .dt.to_period("M")

        .astype(str)

    )


    resolution_trend = (

        trend_df

        .groupby("Month")

        ["Resolution Days"]

        .mean()

        .reset_index()

    )


    resolution_trend[
        "Resolution Days"
    ] = (

        resolution_trend[
            "Resolution Days"
        ]

        .round(2)

    )


    fig_trend = px.line(

        resolution_trend,

        x="Month",

        y="Resolution Days",

        markers=True,

        title="Average Resolution Time Trend",

    )


    fig_trend.update_layout(

        height=420,

        yaxis_title="Average Days",

    )


    st.plotly_chart(

        fig_trend,

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # AUTOMATED RECOMMENDATIONS
    # =========================================================================

    st.subheader("💡 Resolution Recommendations")


    slowest_module = (

        filtered_df

        .groupby("Module")

        ["Resolution Days"]

        .mean()

        .idxmax()

    )


    highest_time = round(

        filtered_df

        .groupby("Module")

        ["Resolution Days"]

        .mean()

        .max(),

        2,

    )


    sla_failures = (

        filtered_df[
            filtered_df["Resolution Days"] > 7
        ]

        .shape[0]

    )


    rec_col1, rec_col2 = st.columns(2)


    with rec_col1:

        st.warning(

            f"""
### ⚠ Attention Required

Module:

**{slowest_module}**

Average Resolution:

**{highest_time} Days**

Consider additional testing resources.
"""

        )


    with rec_col2:

        st.info(

            f"""
### 📊 SLA Observation

Bugs exceeding 7 days:

**{sla_failures}**

Review priority assignment and developer workload.
"""

        )


    st.markdown("---")


    # =========================================================================
    # EXPORT REPORT
    # =========================================================================

    st.subheader("📥 Export Resolution Report")


    report = module_resolution.to_csv(

        index=False

    ).encode("utf-8")


    st.download_button(

        label="Download Resolution Report",

        data=report,

        file_name="resolution_intelligence_report.csv",

        mime="text/csv",

        use_container_width=True,

    )


    st.success(

        "Resolution Intelligence analysis completed successfully."

    )
