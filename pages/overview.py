"""
Overview Page of the Car Price Analytics Dashboard.
Displays key performance indicators (KPIs) and visualizations based on filtered data.
"""

# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- Page config ----------------
st.title("Western Car Price System Analysis")
st.caption("This dashboard provides insights into Western car prices through "
           "filtering, summarizing, visualization, and price prediction. "
           "Built with Streamlit + pandas + matplotlib.")

# ---------------- Load filtered data ----------------
if "filtered_df" not in st.session_state:
    st.warning("No data found. Please visit the Home page to load and filter the dataset.")
    st.stop()

df = st.session_state["filtered_df"]

# ---------------- Compute KPIs ----------------
if df.empty:
    st.error("No cars match the selected filters.")
    st.stop()

avg_price = df["price"].mean()
avg_hp = df["horsepower"].mean()
avg_enginesize = df["enginesize"].mean()
avg_mileage = ((df["citympg"] + df["highwaympg"]) / 2).mean()

# ---------------- Display KPIs ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Price", f"£{avg_price:,.0f}")
col2.metric("Average Horsepower", f"{avg_hp:,.0f} hp")
col3.metric("Average Engine Size", f"{avg_enginesize:,.0f} cc")
col4.metric("Average Mileage", f"{avg_mileage:,.1f} mpg")

st.divider()

# ---------------- Plot: Price distribution ----------------
st.subheader("Price Distribution")

fig = px.histogram(
    df,
    x="price",
    nbins=25,
    title="Distribution of Car Prices (Filtered Data)",
    labels={"price": "Price (£)", "count": "Number of Cars"},
    color_discrete_sequence=["#1f77b4"],
)

fig.update_layout(
    bargap=0.05,
    xaxis_title="Price (£)",
    yaxis_title="Number of Cars",
    template="simple_white",
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Data table ----------------
st.subheader("Filtered Dataset")
st.dataframe(
    df.reset_index(drop=True),
    use_container_width=True,
    height=400
)

# ---------------- Global filters display ----------------
with st.expander("Active Filters Summary"):
    filters = st.session_state.get("global_filters", {})
    st.json(filters)