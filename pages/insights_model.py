import streamlit as st
import pandas as pd
import joblib  # or pickle, depending on how you saved the model
from pathlib import Path

# ---------------- Page setup ----------------
st.title("Predictive Model Showcase")
st.caption(
    "This section demonstrates a multiple linear regression model trained to estimate car prices "
    "based on selected features. The model is illustrative and not production-grade, "
    "serving as a proof of concept for future implementation."
)

# ---------------- Load filtered data ----------------

if "df" not in st.session_state:
    st.warning("No data found. Please visit the Home page to load and filter the dataset.")
    st.stop()

df = st.session_state["df"]

# ---------------- Data preparation ----------------

# given the exponential dist. of 'Price', an upper quantile cap will be applied
lower, upper = df['price'].quantile([0.0, 0.99])
df = df.query('price <= @upper')
df.reset_index(inplace = True, drop = True)

# recategorise 'symboling' to improve balance
df['symboling'] = df['symboling'].astype('category')
df['symboling_binned']= df['symboling'].cat.remove_categories([3]).replace({-2: 'Low', -1: 'Low', 0: 'Medium', 1: 'High', 2: 'Very High', 3: 'Very High'})


# ---------------- Model description ----------------
st.subheader("Model Overview")
st.markdown(
    """
    The model used here is a :green[**MultipleLinear Regression**] trained on the filtered dataset.  
    It estimates car prices based on several numerical and categorical predictors such as
    horsepower or car body type. Its performance metrics on the test set are as follows:
    - :blue[**R² (Coefficient of Determination)**]: 0.963
    - :blue[**RMSE (Root Mean Squared Error)**]: 3087976.29

    Below is a visual assessment of its performance on the test data.
    """
)

# ---------------- Model performance figure ----------------
st.image("figures/predicted_vs_actual.png",
    use_container_width=True,
    caption="Predicted vs Actual Prices — Test Set"
)

st.divider()

# ---------------- User Input Section ----------------
st.subheader("Try the Model")

st.markdown(
    """
    Enter example feature values below to see the model's predicted price.  
    The inputs are simplified to demonstrate how user interaction could work in a future production dashboard.
    """
)

# columns of inputs
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    curbweight = st.slider(
        "Curbweight (lbs)",
        min_value=float(df['curbweight'].min()),
        max_value=float(df['curbweight'].max()),
        value=float(df['curbweight'].median()),
        step=float(100)
    )
with col2:
    horsepower = st.slider(
        "Horsepower",
        min_value=float(df['horsepower'].min()),
        max_value=float(df['horsepower'].max()),
        value=float(df['horsepower'].median()),
        step=float(10)
    )
with col3:
    price_per_hp = st.slider(
        "Price per Horsepower",
        min_value=float(df['price_per_hp'].min()),
        max_value=float(df['price_per_hp'].max()),
        value=float(df['price_per_hp'].median()),
        step=float(10)
    )
with col4:
    wheelbase = st.slider(
        "Wheelbase",
        min_value=float(df['wheelbase'].min()),
        max_value=float(df['wheelbase'].max()),
        value=float(df['wheelbase'].median()),
        step=float(1)
    )
with col5:
    boreratio = st.slider(
        "Bore Ratio",
        min_value=float(df['boreratio'].min()),
        max_value=float(df['boreratio'].max()),
        value=float(df['boreratio'].median()),
        step=float(0.1)
    )

col6, col7, col8, col9, col10 = st.columns(5)

with col6:
    power_to_weight_ratio = st.slider(
        "Power to Weight Ratio",
        min_value=float(df['power_to_weight_ratio'].min()),
        max_value=float(df['power_to_weight_ratio'].max()),
        value=float(df['power_to_weight_ratio'].median()),
        step=float(0.01)
    )
with col7:
    # Example categorical input (dropdown)
    carbody = st.selectbox(
        "Car Body Type",
        options=df['carbody'].unique().tolist(),
        index=0
    )
with col8:
    drivewheel = st.selectbox(
        "Drive Wheel Type",
        options=df['drivewheel'].unique().tolist(),
        index=0
    )
with col9:
    compressionratio_bin = st.selectbox(
        "Compression Ratio (binned)",
        options=df['compressionratio_bin'].unique().tolist(),
        index=0
    )
with col10:
    symboling_binned = st.selectbox(
        "Insurance Risk Rating",
        options=df['symboling_binned'].unique().tolist(),
        index=2,
    )

st.divider()

# ---------------- Model Prediction ----------------

# Load model (update path and loader as needed)
@st.cache_resource
def load_model():
    return joblib.load("pages/model/trained_model.pkl")

model = load_model()

# Predict button
if st.button("🔮 Predict Price"):
    # Create example input DataFrame (adapt to your model’s feature names)
    input_data = pd.DataFrame([{
        "curbweight": curbweight,
        "horsepower": horsepower,
        "price_per_hp": price_per_hp,
        "wheelbase": wheelbase,
        "boreratio": boreratio,
        "power_to_weight_ratio": power_to_weight_ratio,
        "carbody": carbody,
        "drivewheel": drivewheel,
        "compressionratio_bin": compressionratio_bin,
        "symboling_binned": symboling_binned
    }]
)
    # Perform prediction
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"**Predicted Car Price:** ${prediction:,.0f}")
    except Exception as e:
        st.error("Prediction failed. Please verify the model input format.")
        st.exception(e)
else:
    st.info("Set your desired feature values and click **Predict Price** above to run the model.")