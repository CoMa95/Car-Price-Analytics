"""
Dashboard application for Car Price Analytics using Streamlit.
Includes page navigation and sidebar filters.
"""
import streamlit as st
import pandas as pd

# Configure the Streamlit page
st.set_page_config(
    page_title="Car Price Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load data and store in session state
@st.cache_data
def load_data():
    return pd.read_csv('data/final/car_prices.csv')
if "df" not in st.session_state:
    st.session_state['df'] = load_data()

df = st.session_state['df']

# Define pages for navigation
overview = st.Page("pages/overview.py",
                   title="Overview",
                   icon="🏠")
hypothesis1 = st.Page("pages/hypothesis1.py",
                      title="Hypothesis 1",
                      icon="❓")
hypothesis2 = st.Page("pages/hypothesis2.py",
                      title="Hypothesis 2",
                      icon="❓")
hypothesis3 = st.Page("pages/hypothesis3.py",
                      title="Hypothesis 3",
                      icon="💡")
hypothesis4 = st.Page("pages/hypothesis4.py",
                      title="Hypothesis 4",
                      icon="💡")
hypothesis5 = st.Page("pages/hypothesis5.py",
                      title="Hypothesis 5",
                      icon="❓")
nav = st.navigation([overview, hypothesis1, hypothesis2, hypothesis3, hypothesis4, hypothesis5])

current_page = nav.title

# ---------------- Sidebar (filters) ----------------
with st.sidebar:
    st.header("Filters")

    # price filter
    price_range = st.slider("Price Range",
                            min_value=float(df['price'].min()),
                            max_value=float(df['price'].max()),
                            value=(float(df['price'].min()),
                                   float(df['price'].max())))
    # engine size
    enginesizes = st.slider("Engine Size",
                            min_value=float(df['enginesize'].min()),
                            max_value=float(df['enginesize'].max()),
                            value=(float(df['enginesize'].min()),
                                   float(df['enginesize'].max())))
    # horsepower
    horsepower = st.slider("Horsepower",
                           min_value=float(df['horsepower'].min()),
                           max_value=float(df['horsepower'].max()),
                           value=(float(df['horsepower'].min()),
                                  float(df['horsepower'].max())))
    # fuel type
    # Only show fuel filter if not on Hypothesis 1
    if current_page != "Hypothesis 1":
        fuel_types = st.sidebar.multiselect(
            "Fuel Type(s):",
            options=df["fueltype"].unique().tolist(),
            default=df["fueltype"].unique().tolist()
        )
    else:
        fuel_types = df["fueltype"].unique().tolist()  # include all by default

    # car body type
    carbody_types = st.multiselect("Car Body Type",
                                   options=df['carbody'].unique().tolist(),
                                   default=df['carbody'].unique().tolist())
    # drive wheel type
    drivewheel_types = st.multiselect("Drive Wheel Type",
                                      options=df['drivewheel'].unique()
                                      .tolist(),
                                      default=df['drivewheel'].unique()
                                      .tolist())


# apply filters
def apply_filters(original_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply filters to the original dataframe

    Args:
        original_df (pd.DataFrame): The input DataFrame before filtering

    Returns:
        pd.DataFrame: The filtered DataFrame
    """
    filtered_df = original_df[original_df['price'].between(*price_range)]
    if fuel_types:
        filtered_df = filtered_df[filtered_df['fueltype'].isin(fuel_types)]
    if carbody_types:
        filtered_df = filtered_df[filtered_df['carbody'].isin(carbody_types)]
    if drivewheel_types:
        filtered_df = filtered_df[filtered_df['drivewheel']
                                  .isin(drivewheel_types)]
    filtered_df = filtered_df[filtered_df['enginesize'].between(*enginesizes)]
    filtered_df = filtered_df[filtered_df['horsepower'].between(*horsepower)]
    return filtered_df


st.session_state['filtered_df'] = apply_filters(df)

# display total cars after filtering
st.sidebar.info("**Cars after filtering: "
                f"{st.session_state['filtered_df'].shape[0]}**")

# ---------------- Save global filters to session_state ----------------
st.session_state['global_filters'] = {
    'price_range': price_range,
    'enginesizes': enginesizes,
    'horsepower': horsepower,
    'fuel_types': fuel_types,
    'carbody_types': carbody_types,
    'drivewheel_types': drivewheel_types
}

# Run the navigation
nav.run()
