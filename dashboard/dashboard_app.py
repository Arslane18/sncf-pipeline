import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(
    page_title="SNCF Disruptions Dashboard",
    page_icon="🚆",
    layout="wide",
)

st.title("🚆 SNCF Disruptions Dashboard")

conn = duckdb.connect("data/sncf.duckdb")

# ── Load data ────────────────────────────────────────────────────────────────

df_severity = conn.execute("""
    SELECT * FROM mart_disruptions_by_serverity
""").fetchdf()

df_latest = conn.execute("""
    SELECT
        id,
        status,
        severity,
        ingestion_ts,
        messages
    FROM marts_latest_disruptions
""").fetchdf()

df_transitions = conn.execute("""
    SELECT * FROM marts_status_transitions
""").fetchdf()

# ── KPI Row ───────────────────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total disruptions (all time)",
        int(df_severity["nb_disruptions"].sum()),
    )

with col2:
    active = df_latest[df_latest["status"] == "active"]
    st.metric(
        "Currently active",
        len(active),
    )

with col3:
    st.metric(
        "Unique disruptions tracked",
        df_latest["id"].nunique(),
    )

with col4:
    st.metric(
        "Status transitions recorded",
        len(df_transitions),
    )

st.divider()

# ── Severity chart (existing, with filter) ───────────────────────────────────

st.subheader("Disruptions by severity")

status_options = ["All"] + sorted(df_severity["status"].unique().tolist())
status_filter = st.selectbox("Filter by status", options=status_options)

df_sev_filtered = (
    df_severity
    if status_filter == "All"
    else df_severity[df_severity["status"] == status_filter]
)

severity_agg = (
    df_sev_filtered
    .groupby("severity")["nb_disruptions"]
    .sum()
    .reset_index()
)
st.bar_chart(severity_agg.set_index("severity"))

st.divider()

# ── Latest disruptions ────────────────────────────────────────────────────────

st.subheader("📋 Latest state of each disruption")

status_badge_color = {
    "active":  "🔴",
    "past":    "⚪",
    "future":  "🟡",
}

df_latest_display = df_latest.copy()
df_latest_display["status"] = df_latest_display["status"].apply(
    lambda s: f"{status_badge_color.get(s, '')} {s}"
)

display_cols = ["id", "status", "severity", "updated_at", "ingestion_ts"]
display_cols = [c for c in display_cols if c in df_latest_display.columns]

st.dataframe(
    df_latest_display[display_cols],
    width='stretch',
    hide_index=True,
)

st.divider()

# ── Raw data ──────────────────────────────────────────────────────────────────

with st.expander("🗃️ Raw severity data"):
    st.dataframe(df_sev_filtered, width='stretch', hide_index=True)