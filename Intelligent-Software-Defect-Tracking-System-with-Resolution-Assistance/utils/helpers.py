from __future__ import annotations

import pandas as pd
import numpy as np
import streamlit as st


# =============================================================================
# Theme Helpers
# =============================================================================

def get_current_theme() -> str:
    """
    Returns the current theme stored in Streamlit session state.

    Returns
    -------
    str
        "Light" or "Dark"
    """
    return st.session_state.get("theme", "Light")


def is_dark_theme() -> bool:
    """True if current theme is Dark."""
    return get_current_theme() == "Dark"


def get_plotly_template() -> str:
    """
    Returns the appropriate Plotly template.
    """
    return "plotly_dark" if is_dark_theme() else "plotly_white"


# =============================================================================
# Safe DataFrame Helpers
# =============================================================================

def safe_column(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Returns a dataframe column if it exists,
    otherwise an empty Series.

    Parameters
    ----------
    df : DataFrame
    column : str

    Returns
    -------
    Series
    """
    if column in df.columns:
        return df[column]

    return pd.Series(dtype="object")


def safe_count(df: pd.DataFrame, column: str, value) -> int:
    """
    Safely count occurrences of a value inside a column.
    """
    if column not in df.columns:
        return 0

    return int(
        (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            str(value).strip().lower()
        ).sum()
    )


# =============================================================================
# KPI Calculations
# =============================================================================

def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate dashboard KPIs.

    Expected columns (if available):

    Status
    Severity
    Resolution_Time
    Duplicate
    """

    total_bugs = len(df)

    open_bugs = safe_count(df, "Status", "Open")

    closed_bugs = (
        safe_count(df, "Status", "Closed")
        + safe_count(df, "Status", "Resolved")
    )

    critical_bugs = safe_count(df, "Severity", "Critical")

    duplicate_bugs = (
        safe_count(df, "Duplicate", "Yes")
        + safe_count(df, "Duplicate", 1)
        + safe_count(df, "Duplicate", True)
    )

    avg_resolution = 0.0

    if "Resolution_Time" in df.columns:
        avg_resolution = round(
            pd.to_numeric(
                df["Resolution_Time"],
                errors="coerce"
            ).mean(),
            2,
        )

    closure_rate = 0.0

    if total_bugs > 0:
        closure_rate = round(
            (closed_bugs / total_bugs) * 100,
            2,
        )

    return {
        "Total Bugs": total_bugs,
        "Open Bugs": open_bugs,
        "Closed Bugs": closed_bugs,
        "Critical Bugs": critical_bugs,
        "Average Resolution Time": avg_resolution,
        "Duplicate Bugs": duplicate_bugs,
        "Bug Closure Rate": closure_rate,
    }


# =============================================================================
# Formatting
# =============================================================================

def format_number(value) -> str:
    """
    Format integers/floats nicely.
    """

    if value is None:
        return "-"

    if isinstance(value, float):
        return f"{value:,.2f}"

    if isinstance(value, int):
        return f"{value:,}"

    return str(value)


def percentage(value) -> str:
    """
    Convert numeric value into percentage string.
    """
    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "0%"


# =============================================================================
# Date Helpers
# =============================================================================

def convert_datetime(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convert multiple columns to datetime.
    """

    for col in columns:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    return df


# =============================================================================
# Missing Value Handling
# =============================================================================

def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values safely.
    """

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            df[col] = df[col].fillna(
                df[col].median()
            )

        else:

            mode = (
                df[col].mode().iloc[0]
                if not df[col].mode().empty
                else "Unknown"
            )

            df[col] = df[col].fillna(mode)

    return df


# =============================================================================
# Duplicate Removal
# =============================================================================

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates().reset_index(drop=True)


# =============================================================================
# Search Utility
# =============================================================================

def global_search(
    df: pd.DataFrame,
    keyword: str,
) -> pd.DataFrame:
    """
    Search across all columns.
    """

    if keyword is None or keyword.strip() == "":
        return df

    keyword = keyword.lower()

    mask = np.column_stack(
        [
            df[col]
            .astype(str)
            .str.lower()
            .str.contains(keyword, na=False)
            for col in df.columns
        ]
    ).any(axis=1)

    return df.loc[mask]


# =============================================================================
# Export Utility
# =============================================================================

def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """
    Convert dataframe into downloadable CSV bytes.
    """

    return df.to_csv(index=False).encode("utf-8")


# =============================================================================
# Status Colors
# =============================================================================

STATUS_COLORS = {
    "Open": "#ef4444",
    "Closed": "#22c55e",
    "Resolved": "#3b82f6",
    "Assigned": "#f59e0b",
    "In Progress": "#8b5cf6",
    "Reopened": "#ec4899",
}


SEVERITY_COLORS = {
    "Critical": "#dc2626",
    "High": "#f97316",
    "Medium": "#eab308",
    "Low": "#22c55e",
}