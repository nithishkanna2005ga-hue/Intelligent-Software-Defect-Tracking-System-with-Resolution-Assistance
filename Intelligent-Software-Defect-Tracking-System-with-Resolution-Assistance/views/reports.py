"""
===============================================================================
Reports Page
Bug Life Cycle Management Dashboard
===============================================================================

Professional reporting and export center.
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.data_loader import get_dataframe


# =============================================================================
# REPORTS PAGE
# =============================================================================

def show_reports():

    df = get_dataframe()


    st.header("📄 Reports Center")


    st.caption(

        "Generate professional bug lifecycle reports and export insights"

    )


    st.markdown("---")


    # =========================================================================
    # REPORT KPI SUMMARY
    # =========================================================================

    st.subheader("📊 Executive Summary")


    total_bugs = len(df)


    resolved = (

        df[df["Status"] == "Resolved"]

        .shape[0]

    )


    open_bugs = (

        df[df["Status"] == "Open"]

        .shape[0]

    )


    critical_bugs = (

        df[df["Priority"] == "Critical"]

        .shape[0]

    )


    avg_resolution = round(

        df["Resolution Days"]

        .mean(),

        2

    )


    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(

        "Total Bugs",

        total_bugs

    )


    col2.metric(

        "Resolved",

        resolved

    )


    col3.metric(

        "Open",

        open_bugs

    )


    col4.metric(

        "Critical",

        critical_bugs

    )


    col5.metric(

        "Avg Resolution",

        f"{avg_resolution} Days"

    )


    st.markdown("---")


    # =========================================================================
    # REPORT TYPE SELECTION
    # =========================================================================

    st.subheader("📋 Select Report Type")


    report_type = st.selectbox(

        "Choose Report",

        [

            "Complete Bug Report",

            "Priority Analysis Report",

            "Developer Performance Report",

            "Module Quality Report",

            "Resolution Report",

        ]

    )


    st.markdown("---")
    # =========================================================================
    # REPORT GENERATION
    # =========================================================================

    st.subheader("📊 Generated Report")


    report_df = pd.DataFrame()


    # -------------------------------------------------------------------------
    # COMPLETE BUG REPORT
    # -------------------------------------------------------------------------

    if report_type == "Complete Bug Report":


        report_df = df.copy()


        st.info(

            "Complete bug lifecycle report generated."

        )


    # -------------------------------------------------------------------------
    # PRIORITY ANALYSIS REPORT
    # -------------------------------------------------------------------------

    elif report_type == "Priority Analysis Report":


        report_df = (

            df

            .groupby("Priority")

            .agg(

                Total_Bugs=(

                    "Bug ID",

                    "count"

                ),

                Average_Resolution=(

                    "Resolution Days",

                    "mean"

                ),

            )

            .reset_index()

        )


        report_df[

            "Average_Resolution"

        ] = (

            report_df[

                "Average_Resolution"

            ]

            .round(2)

        )


        st.info(

            "Priority analysis report generated."

        )


    # -------------------------------------------------------------------------
    # DEVELOPER PERFORMANCE REPORT
    # -------------------------------------------------------------------------

    elif report_type == "Developer Performance Report":


        report_df = (

            df

            .groupby("Developer")

            .agg(

                Assigned_Bugs=(

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


        report_df[

            "Avg_Resolution"

        ] = (

            report_df[

                "Avg_Resolution"

            ]

            .round(2)

        )


        st.info(

            "Developer performance report generated."

        )


    # -------------------------------------------------------------------------
    # MODULE QUALITY REPORT
    # -------------------------------------------------------------------------

    elif report_type == "Module Quality Report":


        report_df = (

            df

            .groupby("Module")

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


        report_df[

            "Avg_Resolution"

        ] = (

            report_df[

                "Avg_Resolution"

            ]

            .round(2)

        )


        st.info(

            "Module quality report generated."

        )


    # -------------------------------------------------------------------------
    # RESOLUTION REPORT
    # -------------------------------------------------------------------------

    elif report_type == "Resolution Report":


        report_df = (

            df

            .groupby("Status")

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


        report_df[

            "Avg_Resolution"

        ] = (

            report_df[

                "Avg_Resolution"

            ]

            .round(2)

        )


        st.info(

            "Resolution performance report generated."

        )


    st.dataframe(

        report_df,

        use_container_width=True,

        height=400,

    )


    st.markdown("---")
    # =========================================================================
    # REPORT VISUALIZATION
    # =========================================================================

    st.subheader("📈 Report Visualization")


    if not report_df.empty:


        chart_column = report_df.columns[0]


        numeric_columns = (

            report_df

            .select_dtypes(

                include="number"

            )

            .columns

            .tolist()

        )


        if numeric_columns:


            selected_metric = st.selectbox(

                "Select Metric",

                numeric_columns,

            )


            import plotly.express as px


            fig = px.bar(

                report_df,

                x=chart_column,

                y=selected_metric,

                text=selected_metric,

                title=f"{selected_metric} Analysis",

            )


            fig.update_layout(

                height=430,

            )


            st.plotly_chart(

                fig,

                use_container_width=True,

            )


    st.markdown("---")


    # =========================================================================
    # QUALITY SCORE
    # =========================================================================

    st.subheader("⭐ Bug Quality Score")


    total = len(df)


    if total > 0:


        resolved_percentage = (

            df[

                df["Status"]

                == "Resolved"

            ]

            .shape[0]

            /

            total

            *

            100

        )


        duplicate_percentage = 0


        if "Duplicate" in df.columns:


            duplicate_percentage = (

                df[

                    df["Duplicate"]

                    == "Yes"

                ]

                .shape[0]

                /

                total

                *

                100

            )


        quality_score = (

            resolved_percentage

            -

            duplicate_percentage

        )


        quality_score = max(

            0,

            min(

                100,

                round(

                    quality_score,

                    2

                )

            )

        )


        st.metric(

            "Overall Quality Score",

            f"{quality_score}%"

        )


        st.progress(

            quality_score / 100

        )


        if quality_score >= 80:


            st.success(

                "Excellent bug management quality."

            )


        elif quality_score >= 50:


            st.warning(

                "Average quality. Improvement required."

            )


        else:


            st.error(

                "Low quality score. Immediate attention needed."

            )


    st.markdown("---")


    # =========================================================================
    # MANAGEMENT INSIGHTS
    # =========================================================================

    st.subheader("💡 Management Insights")


    highest_priority = (

        df["Priority"]

        .value_counts()

        .idxmax()

    )


    largest_module = (

        df["Module"]

        .value_counts()

        .idxmax()

    )


    st.info(

        f"""
### Key Observations

🔹 Most Common Priority:
**{highest_priority}**

🔹 Most Affected Module:
**{largest_module}**

Use these insights to improve testing strategy,
resource allocation and release planning.
"""

    )


    st.markdown("---")
    # =========================================================================
    # EXPORT REPORT
    # =========================================================================

    st.subheader("📥 Export Reports")


    if not report_df.empty:


        csv_report = (

            report_df

            .to_csv(

                index=False

            )

            .encode("utf-8")

        )


        st.download_button(

            label="Download CSV Report",

            data=csv_report,

            file_name="bug_lifecycle_report.csv",

            mime="text/csv",

            use_container_width=True,

        )


    st.markdown("---")


    # =========================================================================
    # PDF REPORT INFORMATION
    # =========================================================================

    st.subheader("📄 Professional Report")


    st.info(

        """
PDF report generation module is ready.

The final version can generate:

✔ Executive summary

✔ Bug statistics

✔ Analytics charts

✔ Resolution analysis

✔ Quality score

✔ Management recommendations


"""

    )


    st.markdown("---")


    # =========================================================================
    # FINAL STATUS
    # =========================================================================

    st.success(

        "Bug lifecycle report generation completed successfully."

    )