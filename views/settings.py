"""
===============================================================================
Settings Page
Bug Life Cycle Management Dashboard
===============================================================================

Application configuration and user preferences.
===============================================================================
"""

from __future__ import annotations

import streamlit as st

from utils.data_loader import get_dataframe


# =============================================================================
# SETTINGS PAGE
# =============================================================================

def show_settings():

    df = get_dataframe()


    st.header("⚙ Settings")


    st.caption(

        "Configure dashboard preferences and system options"

    )


    st.markdown("---")


    # =========================================================================
    # USER SETTINGS
    # =========================================================================

    st.subheader("👤 User Preferences")


    user_col1, user_col2 = st.columns(2)


    with user_col1:


        user_name = st.text_input(

            "User Name",

            value=st.session_state.get(

                "user_name",

                "Admin"

            ),

        )


    with user_col2:


        company_name = st.text_input(

            "Company Name",

            value=st.session_state.get(

                "company_name",

                "Software Organization"

            ),

        )


    if st.button(

        "💾 Save User Settings",

        use_container_width=True,

    ):


        st.session_state.user_name = user_name

        st.session_state.company_name = company_name


        st.success(

            "User settings updated successfully."

        )


    st.markdown("---")


    # =========================================================================
    # THEME SETTINGS
    # =========================================================================

    st.subheader("🎨 Appearance Settings")


    theme_option = st.radio(

        "Select Theme",

        [

            "Light",

            "Dark",

        ],

        index=(

            1

            if st.session_state.theme == "Dark"

            else 0

        ),

    )


    if st.button(

        "Apply Theme",

        use_container_width=True,

    ):


        st.session_state.theme = theme_option


        st.rerun()


    st.markdown("---")
    # =========================================================================
    # DATA SETTINGS
    # =========================================================================

    st.subheader("📂 Dataset Settings")


    data_col1, data_col2 = st.columns(2)


    with data_col1:


        st.metric(

            "Total Records",

            len(df),

        )


    with data_col2:


        st.metric(

            "Total Columns",

            df.shape[1],

        )


    st.write(

        "Current Dataset Preview"

    )


    st.dataframe(

        df.head(10),

        use_container_width=True,

    )


    st.markdown("---")


    # =========================================================================
    # CACHE MANAGEMENT
    # =========================================================================

    st.subheader("🔄 Cache Management")


    st.write(

        """
Clear cached data when:

- Dataset is updated
- New records are added
- Dashboard shows old information
"""

    )


    if st.button(

        "🧹 Clear Dashboard Cache",

        use_container_width=True,

    ):


        st.cache_data.clear()

        st.cache_resource.clear()


        st.success(

            "Cache cleared successfully."

        )


        st.rerun()


    st.markdown("---")


    # =========================================================================
    # DASHBOARD PREFERENCES
    # =========================================================================

    st.subheader("📊 Dashboard Preferences")


    refresh_time = st.selectbox(

        "Auto Refresh Interval",

        [

            "Disabled",

            "1 Minute",

            "5 Minutes",

            "15 Minutes",

            "30 Minutes",

        ],

    )


    chart_animation = st.toggle(

        "Enable Chart Animations",

        value=True,

    )


    compact_mode = st.toggle(

        "Compact Dashboard View",

        value=False,

    )


    st.session_state.refresh_time = refresh_time

    st.session_state.chart_animation = chart_animation

    st.session_state.compact_mode = compact_mode


    st.success(

        "Dashboard preferences saved."

    )


    st.markdown("---")
    # =========================================================================
    # SYSTEM INFORMATION
    # =========================================================================

    st.subheader("💻 System Information")


    info_col1, info_col2 = st.columns(2)


    with info_col1:

        st.info(

            """
### Application

🐞 Bug Life Cycle Management Dashboard


Framework:

Streamlit


Architecture:

Modular Enterprise Design


"""

        )


    with info_col2:

        st.info(

            """
### Features

✔ Analytics Dashboard

✔ Bug Repository

✔ AI Prediction

✔ Duplicate Detection

✔ Reporting System


"""

        )


    st.markdown("---")


    # =========================================================================
    # VERSION INFORMATION
    # =========================================================================

    st.subheader("ℹ Application Details")


    details = {

        "Application":

        "Bug Life Cycle Management Platform",

        "Version":

        "2.0",

        "Framework":

        "Streamlit",

        "Status":

        "Production Ready",

    }


    st.table(details)


    st.markdown("---")


    # =========================================================================
    # RESET SETTINGS
    # =========================================================================

    st.subheader("⚠ Reset Configuration")


    st.warning(

        """
This will reset dashboard preferences
to default values.
"""

    )


    if st.button(

        "Reset Settings",

        use_container_width=True,

    ):


        st.session_state.theme = "Light"

        st.session_state.primary_color = "#2563eb"

        st.session_state.refresh_time = "Disabled"

        st.session_state.chart_animation = True

        st.session_state.compact_mode = False


        st.success(

            "Settings reset successfully."

        )


        st.rerun()


    st.markdown("---")


    st.success(

        "Settings configuration completed successfully."

    )
