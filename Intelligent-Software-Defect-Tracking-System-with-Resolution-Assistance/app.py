"""
===============================================================================
Bug Life Cycle Management Dashboard
Enterprise Professional Edition

Author : OpenAI + Nithish
Framework : Streamlit
Version : 2.0.0
===============================================================================
"""


# =============================================================================
# IMPORTS
# =============================================================================

from pathlib import Path
import os
import importlib

import streamlit as st
import plotly.io as pio

# Global Plotly chart styling
pio.templates["professional"] = pio.templates["plotly_white"]

pio.templates["professional"].layout.update(
    font=dict(
        family="Inter",
        size=18,
        color="black"
    ),

    title=dict(
        font=dict(
            family="Inter",
            size=28,
            color="black"
        )
    ),

    xaxis=dict(
        tickfont=dict(
            family="Inter",
            size=16,
            color="black"
        ),
        title_font=dict(
            family="Inter",
            size=20,
            color="black"
        )
    ),

    yaxis=dict(
        tickfont=dict(
            family="Inter",
            size=16,
            color="black"
        ),
        title_font=dict(
            family="Inter",
            size=20,
            color="black"
        )
    ),

    legend=dict(
        font=dict(
            family="Inter",
            size=16,
            color="black"
        )
    )
)

pio.templates.default = "professional"
st.markdown("""
<style>

/* ================================
   GLOBAL PROFESSIONAL DASHBOARD FONT
================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* Apply font everywhere */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}


/* All normal text */
p, span, label, div {
    font-weight: 600 !important;
}


/* Page titles */
h1 {
    font-size: 42px !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 32px !important;
    font-weight: 800 !important;
}

h3 {
    font-size: 25px !important;
    font-weight: 750 !important;
}


/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] * {
    font-size: 17px !important;
    font-weight: 700 !important;
}


/* ================================
   METRIC CARDS
================================ */

[data-testid="stMetric"] {

    border: 2px solid #555 !important;
    border-radius: 15px !important;
    padding: 18px !important;

    box-shadow: 0px 5px 15px rgba(0,0,0,0.18);

}


[data-testid="stMetricValue"] {

    font-size: 38px !important;
    font-weight: 800 !important;

}


[data-testid="stMetricLabel"] {

    font-size: 18px !important;
    font-weight: 800 !important;

}


/* ================================
   BUTTONS
================================ */

button {

    font-weight: 700 !important;
    font-size: 16px !important;

}


/* ================================
   SELECT BOX / INPUT LABELS
================================ */

.stSelectbox label,
.stTextInput label,
.stNumberInput label {

    font-weight: 800 !important;
    font-size: 17px !important;

}


/* ================================
   PLOTLY TOOLBAR
   Remove box around zoom/pan
================================ */

.js-plotly-plot .plotly .modebar {

    background: transparent !important;
    border: none !important;
    box-shadow: none !important;

}


.js-plotly-plot .plotly .modebar-btn {

    background: transparent !important;
    border: none !important;
    box-shadow: none !important;

}


/* ================================
   DATA TABLE
================================ */

[data-testid="stDataFrame"] {

    border: 2px solid #555 !important;
    border-radius: 12px !important;

}

</style>
""", unsafe_allow_html=True)
# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(

    page_title="Bug Life Cycle Management",

    page_icon="🐞",

    layout="wide",

    initial_sidebar_state="expanded",

)



# =============================================================================
# APPLICATION CONSTANTS
# =============================================================================

APP_NAME = "Bug Life Cycle Management"

APP_VERSION = "2.0.0"

APP_DESCRIPTION = (
    "Enterprise Professional Bug Management Dashboard"
)



# =============================================================================
# PROJECT PATHS
# =============================================================================

ROOT_DIR = Path(__file__).resolve().parent


ASSETS_DIR = ROOT_DIR / "assets"


STYLE_FILE = ASSETS_DIR / "styles.css"



# =============================================================================
# SESSION INITIALIZATION
# =============================================================================

DEFAULT_SESSION = {


    "theme": "Light",


    "page": "Dashboard",


    "user_name": "Administrator",


    "company_name": "Enterprise Edition",


    "user_role": "Project Manager",


    "data_loaded": False,


    "refresh_requested": False,

}



for key, value in DEFAULT_SESSION.items():


    if key not in st.session_state:

        st.session_state[key] = value



# =============================================================================
# PAGE REGISTRY
# =============================================================================

PAGE_FUNCTIONS = {


    "Dashboard":
    (
        "views.dashboard",
        "show_dashboard"
    ),



    "Analytics":
    (
        "views.analytics",
        "show_analytics"
    ),



    "Resolution Intelligence":
    (
        "views.resolution_time",
        "show_resolution_time"
    ),



    "Bug Records":
    (
        "views.bug_records",
        "show_bug_records"
    ),



    "Trends":
    (
        "views.trends",
        "show_trends"
    ),



    "Duplicate Detection":
    (
        "views.duplicate_detection",
        "show_duplicate_detection"
    ),



    "AI Prediction":
    (
        "views.ai_prediction",
        "show_ai_prediction"
    ),



    "Reports":
    (
        "views.reports",
        "show_reports"
    ),



    "Settings":
    (
        "views.settings",
        "show_settings"
    ),


}
# =============================================================================
# PAGE LOADER
# =============================================================================

def load_page(page_name):


    module_name, function_name = PAGE_FUNCTIONS[page_name]


    try:


        module = importlib.import_module(

            module_name

        )


        page_function = getattr(

            module,

            function_name

        )


        page_function()



    except ModuleNotFoundError as e:


        st.error(

            f"Page module missing: {module_name}"

        )

        st.exception(e)



    except AttributeError as e:


        st.error(

            f"Function {function_name} not found."

        )

        st.exception(e)



    except Exception as e:


        st.error(

            "Unexpected error while loading page."

        )

        st.exception(e)





# =============================================================================
# LOAD CUSTOM CSS
# =============================================================================

def load_css():


    if STYLE_FILE.exists():


        with open(

            STYLE_FILE,

            "r",

            encoding="utf-8"

        ) as file:


            st.markdown(

                f"<style>{file.read()}</style>",

                unsafe_allow_html=True

            )



load_css()





# =============================================================================
# THEME SYSTEM
# =============================================================================

LIGHT_THEME = {


    "background": "#F4F7FB",

    "sidebar": "#FFFFFF",

    "text": "#111827",

    "border": "#E5E7EB",

}



DARK_THEME = {


    "background": "#0F172A",

    "sidebar": "#111827",

    "text": "#F8FAFC",

    "border": "#334155",

}




def get_theme():


    if st.session_state.theme == "Dark":

        return DARK_THEME


    return LIGHT_THEME




theme = get_theme()





# =============================================================================
# DYNAMIC THEME CSS
# =============================================================================

st.markdown(

f"""

<style>


.stApp {{

background:{theme["background"]};

color:{theme["text"]};

}}



section[data-testid="stSidebar"] {{

background:{theme["sidebar"]};

border-right:1px solid {theme["border"]};

}}



.block-container {{

padding-top:1rem;

padding-bottom:2rem;

}}


</style>


""",

unsafe_allow_html=True,

)
st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"] {
    padding-top: 20px;
}


/* Navigation title */
section[data-testid="stSidebar"] h3 {
    font-size: 22px;
    font-weight: 800;
}


/* Radio container spacing */
section[data-testid="stSidebar"] .stRadio > div {
    gap: 12px;
}


/* Hide radio circles */
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label > div:first-child {
    display: none;
}


/* All navigation buttons */
section[data-testid="stSidebar"] .stRadio label {

    width: 100%;
    background: #ffffff;

    padding: 14px 18px;
    margin: 6px 0;

    border-radius: 12px;

    border: 2px solid #475569;

    box-shadow:
        0 5px 12px rgba(0,0,0,0.20);

    transition: all 0.25s ease;

    font-size: 17px;
    font-weight: 750;

    color: #111827;
}


/* Hover */
section[data-testid="stSidebar"] .stRadio label:hover {

    transform: translateY(-3px);

    border-color: #2563eb;

    box-shadow:
        0 8px 18px rgba(0,0,0,0.30);
}


/* Selected navigation */
section[data-testid="stSidebar"] 
.stRadio label:has(input:checked) {

    background: #2563eb;

    color: white;

    border-color: #1e3a8a;


    /* pressed inside effect */

    box-shadow:

        inset 4px 4px 10px rgba(0,0,0,0.35),

        inset -4px -4px 10px rgba(255,255,255,0.25);

    transform: scale(0.96);
}


/* Make all sidebar text bold */
section[data-testid="stSidebar"] p {

    font-weight: 700;

}

</style>
""", unsafe_allow_html=True)





# =============================================================================
# SIDEBAR
# =============================================================================
st.sidebar.markdown("""
<h2 style="
text-align:center;
font-size:26px;
font-weight:900;
color:#111827;
">
BUG LIFE CYCLE MANAGEMENT
</h2>
""", unsafe_allow_html=True)
with st.sidebar:


    st.markdown(

        """

        <div style="text-align:center;">

        <h2>🐞 Bug Life Cycle</h2>

        <p>Enterprise Dashboard</p>

        </div>

        """,

        unsafe_allow_html=True,

    )


    st.divider()


    st.markdown("### 👤 User")


    st.write(

        st.session_state.user_name

    )


    st.caption(

        st.session_state.company_name

    )


    st.caption(

        st.session_state.user_role

    )


    st.divider()


    selected_page = st.radio(

        "Navigation",

        list(PAGE_FUNCTIONS.keys()),

        index=list(PAGE_FUNCTIONS.keys())

        .index(

            st.session_state.page

        ),

    )


    st.session_state.page = selected_page



    st.divider()


    dark_mode = st.toggle(

        "🌙 Dark Mode",

        value=

        st.session_state.theme == "Dark",

    )


    st.session_state.theme = (

        "Dark"

        if dark_mode

        else "Light"

    )



    st.divider()
    # -------------------------------------------------------------------------
    # REFRESH BUTTON
    # -------------------------------------------------------------------------

    if st.button(

        "🔄 Refresh Dashboard",

        use_container_width=True,

    ):


        st.session_state.refresh_requested = True


        st.cache_data.clear()


        st.rerun()



    st.divider()


    st.caption(

        f"Version {APP_VERSION}"

    )





# =============================================================================
# MAIN HEADER
# =============================================================================

st.title(

    st.session_state.page

)


st.caption(

    APP_DESCRIPTION

)





# =============================================================================
# WELCOME BANNER
# =============================================================================

st.markdown(
"""
<style>

.dashboard-card {

padding:18px;

border-radius:12px;

background:#2563eb15;

border:1px solid #2563eb30;

margin-bottom:20px;

}

</style>
""",
unsafe_allow_html=True
)





# =============================================================================
# LOADING STATUS
# =============================================================================

with st.spinner(

    "Loading dashboard..."

):


    st.session_state.data_loaded = True





# =============================================================================
# PAGE EXECUTION
# =============================================================================

load_page(

    st.session_state.page

)





# =============================================================================
# SYSTEM STATUS
# =============================================================================

st.divider()


status1, status2, status3, status4 = st.columns(4)



with status1:


    st.success(

        "🟢 System Online"

    )



with status2:


    st.info(

        f"🎨 Theme: {st.session_state.theme}"

    )



with status3:


    st.info(

        f"👤 {st.session_state.user_name}"

    )



with status4:


    st.info(

        f"📦 {APP_VERSION}"

    )





# =============================================================================
# REFRESH MESSAGE
# =============================================================================

if st.session_state.refresh_requested:


    st.toast(

        "Dashboard refreshed successfully",

        icon="✅"

    )


    st.session_state.refresh_requested = False
# =============================================================================
# APPLICATION INFORMATION
# =============================================================================

with st.expander(

    "ℹ Application Information",

    expanded=False,

):


    col1, col2 = st.columns(2)



    with col1:


        st.markdown(

            "### Session Information"

        )


        st.write(

            f"**User:** {st.session_state.user_name}"

        )


        st.write(

            f"**Company:** {st.session_state.company_name}"

        )


        st.write(

            f"**Role:** {st.session_state.user_role}"

        )



    with col2:


        st.markdown(

            "### Dashboard Information"

        )


        st.write(

            f"**Page:** {st.session_state.page}"

        )


        st.write(

            f"**Theme:** {st.session_state.theme}"

        )


        st.write(

            f"**Version:** {APP_VERSION}"

        )





# =============================================================================
# PROJECT HEALTH CHECK
# =============================================================================

with st.expander(

    "🩺 System Health",

    expanded=False,

):


    required_folders = [

        "views",

        "utils",

        "assets",

        "data",

        "models",

    ]


    for folder in required_folders:


        path = ROOT_DIR / folder



        if path.exists():


            st.success(

                f"✅ {folder} folder available"

            )


        else:


            st.warning(

                f"⚠ {folder} folder missing"

            )





# =============================================================================
# DEBUG INFORMATION
# =============================================================================

if os.getenv(

    "DEBUG",

    "False"

).lower() == "true":


    with st.expander(

        "🛠 Developer Debug"

    ):


        st.json(

            {

                "page":

                st.session_state.page,


                "theme":

                st.session_state.theme,


                "version":

                APP_VERSION,

            }

        )





# =============================================================================
# FOOTER
# =============================================================================

st.divider()


st.markdown(

"""

<div style="text-align:center;padding:15px;">


<b>

🐞 Bug Life Cycle Management Dashboard

</b>


<br>


Enterprise Professional Edition


<br><br>


Built with

❤️ Streamlit • Python • Pandas • Plotly • Machine Learning


</div>


""",

unsafe_allow_html=True,

)
