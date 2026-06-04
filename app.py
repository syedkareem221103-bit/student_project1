import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/startup_success_dataset.csv")

df = load_data()

# ---------------------------------
# HEADER
# ---------------------------------
st.title("🚀 Startup Success Analytics Dashboard")
st.markdown("Deep Business Intelligence & Startup Insights")

st.markdown("---")

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header("Filters")

sector = st.sidebar.multiselect(
    "Sector",
    df["sector"].unique(),
    default=df["sector"].unique()
)

outcome = st.sidebar.multiselect(
    "Outcome",
    df["outcome"].unique(),
    default=df["outcome"].unique()
)

investor = st.sidebar.multiselect(
    "Investor Type",
    df["investor_type"].unique(),
    default=df["investor_type"].unique()
)

filtered = df[
    (df["sector"].isin(sector))
    & (df["outcome"].isin(outcome))
    & (df["investor_type"].isin(investor))
]

# ---------------------------------
# KPI SECTION
# ---------------------------------
st.subheader("📊 Executive Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Startups",
    f"{len(filtered):,}"
)

c2.metric(
    "Avg Revenue",
    f"${filtered['revenue_million'].mean():,.0f}"
)

c3.metric(
    "Avg Team Size",
    f"{filtered['team_size'].mean():.0f}"
)

c4.metric(
    "Avg Funding Rounds",
    f"{filtered['funding_rounds'].mean():.1f}"
)

st.markdown("---")

# ---------------------------------
# OUTCOME DISTRIBUTION
# ---------------------------------
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        filtered,
        names="outcome",
        title="Startup Outcomes"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
        filtered,
        x="sector",
        color="outcome",
        title="Sector Wise Outcomes"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# REVENUE ANALYSIS
# ---------------------------------
st.subheader("💰 Revenue Analysis")

fig = px.box(
    filtered,
    x="outcome",
    y="revenue_million",
    color="outcome",
    title="Revenue Distribution by Outcome"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# FUNDING VS REVENUE
# ---------------------------------
st.subheader("📈 Funding Impact")

fig = px.scatter(
    filtered.sample(min(5000, len(filtered))),
    x="funding_rounds",
    y="revenue_million",
    color="outcome",
    size="team_size",
    hover_data=["sector"],
    title="Funding vs Revenue"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# EXPERIENCE ANALYSIS
# ---------------------------------
st.subheader("👨‍💼 Founder Analysis")

col1, col2 = st.columns(2)

with col1:
    fig = px.violin(
        filtered,
        x="outcome",
        y="founder_experience_years",
        color="outcome",
        title="Founder Experience"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    exp = filtered.groupby("outcome")[
        "founder_experience_years"
    ].mean().reset_index()

    fig = px.bar(
        exp,
        x="outcome",
        y="founder_experience_years",
        color="outcome",
        title="Average Founder Experience"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# INVESTOR ANALYSIS
# ---------------------------------
st.subheader("🏦 Investor Intelligence")

fig = px.sunburst(
    filtered,
    path=["investor_type", "outcome"],
    title="Investor Type Impact"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# MARKET ANALYSIS
# ---------------------------------
st.subheader("🌎 Market Analysis")

fig = px.scatter(
    filtered.sample(min(5000, len(filtered))),
    x="market_size_billion",
    y="product_traction_users",
    color="outcome",
    title="Market Size vs Traction"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# CORRELATION MATRIX
# ---------------------------------
st.subheader("🔥 Correlation Matrix")

numeric_cols = [
    "funding_rounds",
    "founder_experience_years",
    "team_size",
    "market_size_billion",
    "product_traction_users",
    "burn_rate_million",
    "revenue_million"
]

corr = filtered[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Correlation Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# AUTOMATIC INSIGHTS
# ---------------------------------
st.subheader("🧠 AI Business Insights")

top_sector = (
    filtered.groupby("sector")
    .size()
    .sort_values(ascending=False)
    .index[0]
)

top_outcome = (
    filtered["outcome"]
    .value_counts()
    .idxmax()
)

best_investor = (
    filtered.groupby("investor_type")
    ["revenue_million"]
    .mean()
    .idxmax()
)

st.success(
    f"""
    • Most Active Sector: {top_sector}

    • Most Common Outcome: {top_outcome}

    • Highest Revenue Investor Type: {best_investor}

    • Average Revenue: ${filtered['revenue_million'].mean():,.0f}

    • Average Founder Experience: {filtered['founder_experience_years'].mean():.1f} years
    """
)

# ---------------------------------
# DATA TABLE
# ---------------------------------
st.subheader("📋 Raw Dataset")

st.dataframe(filtered, use_container_width=True)

# ---------------------------------
# DOWNLOAD
# ---------------------------------
csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_startups.csv",
    "text/csv"
)
