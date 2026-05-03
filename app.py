import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Survey Data Cleaning & Indicator Explorer",
    layout="wide"
)

# App title
st.title("📊 Survey Data Cleaning & Indicator Explorer")

st.markdown(
    """
    This interactive application demonstrates how survey data can be cleaned,
    analyzed, and transformed into meaningful Monitoring & Evaluation (M&E) indicators.
    """
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("survey_data_anonymized.csv")

df = load_data()

# Basic dataset overview
st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Responses", df.shape[0])

with col2:
    st.metric("Number of Columns", df.shape[1])

with col3:
    st.metric("Regions Covered", df["region"].nunique())

# Show raw data (preview only)
st.subheader("Sample of Raw Data")
st.dataframe(df.head(10))