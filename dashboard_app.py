import streamlit as st
import pandas as pd

# Configure the Streamlit page
st.set_page_config(
    page_title="Car Price Analytics Dashboard",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "df" not in st.session_state:
    st.session_state['df'] = pd.read_csv('data/final/car_prices.csv')

df = st.session_state['df']

# Define pages for navigation
overview = st.Page("pages/overview.py",
                   title="Overview",
                   icon="")

nav = st.navigation([overview])

# ---------------- Sidebar (filters) ----------------
with st.sidebar:
    st.header("Filters")

    # price filter
    price_range = st.slider("Price Range", min_value=float(df['price'].min()), max_value=float(df['price'].max()), value=(float(df['price'].min()), float(df['price'].max())))
    # engine size
    enginesizes = st.slider("Engine Size", min_value=float(df['enginesize'].min()), max_value=float(df['enginesize'].max()), value=(float(df['enginesize'].min()), float(df['enginesize'].max())))
    # horsepower
    horsepower = st.slider("Horsepower", min_value=float(df['horsepower'].min()), max_value=float(df['horsepower'].max()), value=(float(df['horsepower'].min()), float(df['horsepower'].max())))
    # fuel type
    fuel_types = st.multiselect("Fuel Type", options=df['fueltype'].unique().tolist(), default=df['fueltype'].unique().tolist())
    # car body type
    carbody_types = st.multiselect("Car Body Type", options=df['carbody'].unique().tolist(), default=df['carbody'].unique().tolist())
    # drive wheel type
    drivewheel_types = st.multiselect("Drive Wheel Type", options=df['drivewheel'].unique().tolist(), default=df['drivewheel'].unique().tolist())

# apply filters
def apply_filters(df):
    df = df[df['price'].between(*price_range)]
    if fuel_types:
        df = df[df['fueltype'].isin(fuel_types)]
    if carbody_types:
        df = df[df['carbody'].isin(carbody_types)]
    if drivewheel_types:
        df = df[df['drivewheel'].isin(drivewheel_types)]
    df = df[df['enginesize'].between(*enginesizes)]
    df = df[df['horsepower'].between(*horsepower)]
    return df


filtered_df = apply_filters(df)

# display total cars after filtering
st.sidebar.info(f"**Cars after filtering: {filtered_df.shape[0]}**")

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
