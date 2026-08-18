"""
===============================================================================
Dashboard Page
Bug Life Cycle Management Dashboard
===============================================================================
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.data_loader import get_dataframe

# =============================================================================
# SAMPLE DATA LOADER
# Replace this with your dataset loader later.
# =============================================================================

@st.cache_data
def load_dashboard_data():

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

    start_date = datetime.today() - timedelta(days=180)

    df = pd.DataFrame({

        "Bug ID":
            [f"BUG-{1000+i}" for i in range(n)],

        "Status":
            np.random.choice(statuses, n),

        "Priority":
            np.random.choice(priorities, n),

        "Severity":
            np.random.choice(severities, n),

        "Developer":
            np.random.choice(developers, n),

        "Module":
            np.random.choice(modules, n),

        "Resolution Days":
            np.random.randint(1, 20, n),

        "Created Date":
            [
                start_date +
                timedelta(days=int(i))
                for i in np.random.randint(0, 180, n)
            ],
    })

    return df


# =============================================================================
# MAIN DASHBOARD
# =============================================================================

def show_dashboard():

    df = load_dashboard_data()

    st.header("📊 Dashboard Overview")

    st.caption(
        "Real-time Bug Life Cycle Monitoring"
    )

    total_bugs = len(df)

    open_bugs = df[
        df["Status"] == "Open"
    ].shape[0]

    closed_bugs = df[
        df["Status"] == "Closed"
    ].shape[0]

    critical_bugs = df[
        df["Priority"] == "Critical"
    ].shape[0]

    avg_resolution = round(
        df["Resolution Days"].mean(),
        2,
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Bugs",
        total_bugs,
    )

    c2.metric(
        "Open",
        open_bugs,
    )

    c3.metric(
        "Closed",
        closed_bugs,
    )

    c4.metric(
        "Critical",
        critical_bugs,
    )

    c5.metric(
        "Avg Resolution",
        f"{avg_resolution} Days",
    )

    st.markdown("---")
    # =========================================================================
    # ROW 1 : STATUS & PRIORITY
    # =========================================================================

    col1, col2 = st.columns(2)

    with col1:

        status_count = (
            df["Status"]
            .value_counts()
            .reset_index()
        )

        status_count.columns = [
            "Status",
            "Count",
        ]

        fig_status = px.pie(
            status_count,
            names="Status",
            values="Count",
            title="Bug Status Distribution",
            hole=0.45,
        )

        fig_status.update_layout(
            height=420,
            legend_title="Status",
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True,
        )

    with col2:

        priority_count = (
            df["Priority"]
            .value_counts()
            .reset_index()
        )

        priority_count.columns = [
            "Priority",
            "Count",
        ]

        fig_priority = px.bar(
            priority_count,
            x="Priority",
            y="Count",
            color="Priority",
            title="Priority Distribution",
            text="Count",
        )

        fig_priority.update_layout(
            height=420,
            showlegend=False,
        )

        st.plotly_chart(
            fig_priority,
            use_container_width=True,
        )

    st.markdown("---")

    # =========================================================================
    # ROW 2 : SEVERITY & MODULES
    # =========================================================================

    col3, col4 = st.columns(2)

    with col3:

        severity_count = (
            df["Severity"]
            .value_counts()
            .reset_index()
        )

        severity_count.columns = [
            "Severity",
            "Count",
        ]

        fig_severity = px.bar(
            severity_count,
            x="Severity",
            y="Count",
            color="Severity",
            title="Severity Analysis",
            text="Count",
        )

        fig_severity.update_layout(
            height=420,
            showlegend=False,
        )

        st.plotly_chart(
            fig_severity,
            use_container_width=True,
        )

    with col4:

        module_count = (
            df["Module"]
            .value_counts()
            .reset_index()
        )

        module_count.columns = [
            "Module",
            "Count",
        ]

        fig_module = px.treemap(
            module_count,
            path=["Module"],
            values="Count",
            title="Module-wise Bug Distribution",
        )

        fig_module.update_layout(
            height=420,
        )

        st.plotly_chart(
            fig_module,
            use_container_width=True,
        )

    st.markdown("---")
    # =========================================================================
    # ROW 3 : BUG TREND & DEVELOPER WORKLOAD
    # =========================================================================

    col5, col6 = st.columns(2)

    with col5:

        trend_df = (
            df.groupby("Created Date")
            .size()
            .reset_index(name="Bug Count")
            .sort_values("Created Date")
        )

        fig_trend = px.line(
            trend_df,
            x="Created Date",
            y="Bug Count",
            markers=True,
            title="Bug Reporting Trend",
        )

        fig_trend.update_layout(
            height=420,
            xaxis_title="Date",
            yaxis_title="Number of Bugs",
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True,
        )

    with col6:

        developer_df = (
            df["Developer"]
            .value_counts()
            .reset_index()
        )

        developer_df.columns = [
            "Developer",
            "Assigned Bugs",
        ]

        fig_dev = px.bar(
            developer_df,
            x="Developer",
            y="Assigned Bugs",
            color="Assigned Bugs",
            text="Assigned Bugs",
            title="Developer Workload",
        )

        fig_dev.update_layout(
            height=420,
            showlegend=False,
        )

        st.plotly_chart(
            fig_dev,
            use_container_width=True,
        )

    st.markdown("---")

    # =========================================================================
    # ROW 4 : RESOLUTION TIME ANALYSIS
    # =========================================================================

    col7, col8 = st.columns(2)

    with col7:

        fig_resolution = px.histogram(
            df,
            x="Resolution Days",
            nbins=20,
            title="Resolution Time Distribution",
        )

        fig_resolution.update_layout(
            height=420,
            xaxis_title="Resolution Days",
            yaxis_title="Bug Count",
        )

        st.plotly_chart(
            fig_resolution,
            use_container_width=True,
        )

    with col8:

        avg_module = (
            df.groupby("Module")["Resolution Days"]
            .mean()
            .reset_index()
            .sort_values(
                "Resolution Days",
                ascending=False,
            )
        )

        fig_module_time = px.bar(
            avg_module,
            x="Module",
            y="Resolution Days",
            color="Resolution Days",
            text_auto=".1f",
            title="Average Resolution Time by Module",
        )

        fig_module_time.update_layout(
            height=420,
            showlegend=False,
        )

        st.plotly_chart(
            fig_module_time,
            use_container_width=True,
        )

    st.markdown("---")
    # =========================================================================
    # FILTERS
    # =========================================================================

    st.subheader("🔍 Explore Bug Records")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:

        selected_status = st.selectbox(
            "Status",
            ["All"] + sorted(df["Status"].unique().tolist()),
        )

    with filter_col2:

        selected_priority = st.selectbox(
            "Priority",
            ["All"] + sorted(df["Priority"].unique().tolist()),
        )

    with filter_col3:

        selected_module = st.selectbox(
            "Module",
            ["All"] + sorted(df["Module"].unique().tolist()),
        )

    filtered_df = df.copy()

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["Status"] == selected_status
        ]

    if selected_priority != "All":
        filtered_df = filtered_df[
            filtered_df["Priority"] == selected_priority
        ]

    if selected_module != "All":
        filtered_df = filtered_df[
            filtered_df["Module"] == selected_module
        ]

    st.markdown("---")

    # =========================================================================
    # RECENT BUG RECORDS
    # =========================================================================

    st.subheader("📋 Recent Bug Records")

    st.dataframe(
        filtered_df.sort_values(
            "Created Date",
            ascending=False,
        ),
        use_container_width=True,
        height=400,
    )

    # =========================================================================
    # DOWNLOAD
    # =========================================================================

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Filtered Data (CSV)",
        data=csv,
        file_name="bug_dashboard_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("---")

    # =========================================================================
    # DASHBOARD INSIGHTS
    # =========================================================================

    st.subheader("📌 Dashboard Insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.info(
            f"""
• Total Visible Bugs: **{len(filtered_df)}**

• Open Bugs: **{(filtered_df['Status'] == 'Open').sum()}**

• Closed Bugs: **{(filtered_df['Status'] == 'Closed').sum()}**
"""
        )

    with insight_col2:

        avg_days = round(
            filtered_df["Resolution Days"].mean(),
            2,
        )

        st.success(
            f"""
• Average Resolution: **{avg_days} Days**

• Developers: **{filtered_df['Developer'].nunique()}**

• Modules: **{filtered_df['Module'].nunique()}**
"""
        )

    st.markdown("---")

    st.caption(
        "© Bug Life Cycle Management Dashboard • Enterprise Professional Edition"
    )
