import streamlit as st
import pandas as pd
import plotly.express as px


st.markdown("""
<style>
/* ================= GLOBAL DARK MODE LOCK ================= */

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(8px);
    border-right: 1px solid rgba(255,255,255,0.08);

    --text-color: #e5e7eb;
    --label-color: #e5e7eb;
    --secondaryTextColor: #cbd5e1;
}

/* Sidebar text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] p {
    color: #e5e7eb !important;
}

/* ================= DROPDOWN / SELECT OPTIONS FIX ================= */

/* Dropdown panel */
div[data-baseweb="popover"] {
    background-color: #020617 !important;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
}

/* Dropdown option list */
ul[role="listbox"] {
    background-color: #020617 !important;
}

/* Individual options */
li[role="option"] {
    color: #e5e7eb !important;
    background-color: transparent !important;
}

/* Hover / active state */
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: rgba(56, 189, 248, 0.15) !important;
    color: #e5e7eb !important;
}

/* ================= GLASS PANELS ================= */

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 12px;
    border: 1px solid rgba(255,255,255,0.08);
}

div[data-testid="stPlotlyChart"] {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    padding: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}

div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}
</style>
""", unsafe_allow_html=True)



# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Survey Data Cleaning & Indicator Explorer",
    layout="wide"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("survey_data_anonymized.csv")

df = load_data()

# --------------------------------------------------
# App title & description
# --------------------------------------------------
st.title("📊 Survey Data Cleaning & Indicator Explorer")

st.markdown(
    """
    This application demonstrates how survey data can be cleaned,
    analyzed, and transformed into meaningful Monitoring & Evaluation (M&E) indicators.
    """
)

# --------------------------------------------------
# SIDEBAR — Filters
# --------------------------------------------------
st.sidebar.header("🔍 Filters")

# Region filter
region_options = ["All"] + sorted(df["region"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", region_options)

# Gender filter
gender_options = ["All"] + sorted(df["gender"].unique().tolist())
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)

# Year filter
year_options = ["All"] + sorted(df["year"].unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options)

# --------------------------------------------------
# Apply filters
# --------------------------------------------------
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["gender"] == selected_gender]

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["year"] == selected_year]

# --------------------------------------------------
# TABS — Main layout
# --------------------------------------------------
tab_overview, tab_quality, tab_indicators, tab_trends, tab_explorer = st.tabs(
    ["📊 Overview", "🧪 Data Quality", "📈 Indicators", "📉 Trends & Time", "📂 Data Explorer"]
)

# --------------------------------------------------
# TAB 1 — Overview
# --------------------------------------------------
with tab_overview:
    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Responses", filtered_df.shape[0])

    with col2:
        st.metric("Regions Covered", filtered_df["region"].nunique())

    with col3:
        st.metric("Provinces Covered", filtered_df["province"].nunique())

# --------------------------------------------------
# TAB 2 — Data Quality
# --------------------------------------------------
with tab_quality:
    st.subheader("🧪 Data Quality Overview")

    col1, col2, col3 = st.columns(3)

    total_records = filtered_df.shape[0]
    complete_records = filtered_df["response_complete"].sum()
    completeness_rate = round((complete_records / total_records) * 100, 1) if total_records > 0 else 0

    with col1:
        st.metric("Total Responses", total_records)
    with col2:
        st.metric("Complete Responses", complete_records)
    with col3:
        st.metric("Completeness Rate (%)", completeness_rate)

    st.markdown("---")

    st.subheader("Missing Fields Summary")

    missing_summary = (
        filtered_df["missing_fields_count"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    missing_summary.columns = ["Missing Fields Count", "Number of Responses"]

    st.dataframe(missing_summary, use_container_width=True)

    st.markdown("---")

    st.subheader("Sample of Incomplete Responses")

    incomplete_sample = filtered_df[filtered_df["response_complete"] == False]
    if incomplete_sample.empty:
        st.success("✅ All filtered records are complete.")
    else:
        st.dataframe(incomplete_sample.head(10), use_container_width=True)

# --------------------------------------------------
# TAB 3 — Indicators
# --------------------------------------------------
with tab_indicators:
    st.subheader("📈 M&E Indicators")

    indicator = st.selectbox(
        "Select Indicator",
        [
            "School Attendance Rate",
            "Health Service Access Rate",
            "Food Security Status"
        ]
    )

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        if indicator == "School Attendance Rate":
            y_column = "school_attendance"
            positive_label = "Yes"
            indicator_label = "School Attendance"

        elif indicator == "Health Service Access Rate":
            y_column = "health_service_access"
            positive_label = "Yes"
            indicator_label = "Health Service Access"

        else:
            y_column = "food_security_status"
            positive_label = "Secure"
            indicator_label = "Food Security (Secure)"

        valid = filtered_df[y_column].notna()
        total = valid.sum()
        positive = (filtered_df[y_column] == positive_label).sum()
        rate = round((positive / total) * 100, 1) if total > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric(f"{indicator_label} (%)", rate)
        col2.metric("Positive Responses", positive)
        col3.metric("Valid Responses", total)

        st.markdown("---")

        disaggregate_by = st.radio(
            "Disaggregate by:",
            ["Region", "Gender"],
            horizontal=True
        )

        group_col = "region" if disaggregate_by == "Region" else "gender"

        summary = (
            filtered_df
            .groupby(group_col)[y_column]
            .value_counts(normalize=True)
            .rename("percentage")
            .reset_index()
        )

        summary = summary[summary[y_column] == positive_label]
        summary["percentage"] = summary["percentage"] * 100

        fig = px.bar(
            summary,
            x=group_col,
            y="percentage",
            text=summary["percentage"].round(1),
            labels={
                "percentage": f"{indicator_label} (%)",
                group_col: disaggregate_by
            }
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# TAB 4 — Trends & Time Analysis
# --------------------------------------------------
with tab_trends:
    st.subheader("📉 Trends & Time Analysis")

    st.markdown(
        """
        This section analyzes how key M&E indicators change over time.
        Trend analysis helps identify progress, stagnation, or decline across years.
        """
    )

    trend_indicator = st.selectbox(
        "Select Indicator for Trend Analysis",
        [
            "School Attendance Rate",
            "Health Service Access Rate",
            "Food Security (Secure)"
        ],
        key="trend_indicator"
    )

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Indicator mapping
        if trend_indicator == "School Attendance Rate":
            y_column = "school_attendance"
            positive_label = "Yes"
            indicator_label = "School Attendance (%)"

        elif trend_indicator == "Health Service Access Rate":
            y_column = "health_service_access"
            positive_label = "Yes"
            indicator_label = "Health Service Access (%)"

        else:
            y_column = "food_security_status"
            positive_label = "Secure"
            indicator_label = "Food Security (Secure) (%)"

        # Aggregate by year
        trend_df = (
            filtered_df
            .groupby("year")[y_column]
            .apply(lambda x: (x == positive_label).mean() * 100)
            .reset_index(name="percentage")
            .sort_values("year")
        )

        # Line chart
        fig = px.line(
            trend_df,
            x="year",
            y="percentage",
            markers=True,
            labels={
                "year": "Year",
                "percentage": indicator_label
            }
        )

        fig.update_layout(yaxis_range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            **How to read this chart:**
            - Each point represents the indicator value for a given year.
            - Upward trends suggest improvement over time.
            - Downward or flat trends may require further investigation.
            """
        )



# --------------------------------------------------
# TAB 5 — Data Explorer
# --------------------------------------------------
with tab_explorer:
    st.subheader("📂 Data Explorer")

    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data (CSV)",
        csv,
        "filtered_survey_data.csv",
        "text/csv"
    )