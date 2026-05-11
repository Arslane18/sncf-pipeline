import streamlit as st
import duckdb
import pandas as pd

st.title("🚆 SNCF Disruptions Dashboard")

conn = duckdb.connect("data/sncf.duckdb")

df = conn.execute("""
SELECT *
FROM mart_disruptions_by_serverity
""").fetchdf()

# KPI
st.metric(
    "Total disruptions",
    int(df["nb_disruptions"].sum())
)

# Filters
status = st.selectbox(
    "Status",
    options=["All"] + list(df["status"].unique())
)

if status != "All":
    df = df[df["status"] == status]

# Charts
severity_df = (
    df.groupby("severity")["nb_disruptions"]
    .sum()
    .reset_index()
)

st.subheader("Disruptions by severity")
st.bar_chart(
    severity_df.set_index("severity")
)

st.subheader("Raw data")
st.dataframe(df)