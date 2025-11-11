import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os

st.markdown("""
## Hypothesis 04 – Drive Wheel Type vs Car Price

**Hypothesis:**  
Front-wheel drive (FWD) cars are generally cheaper than rear-wheel drive (RWD) cars.

In the Streamlit app, this page:

1. **Checks the data file**  
   - Uses `os.listdir("data/final")` to make sure that `car_prices.csv` exists in the correct folder.

2. **Loads the cleaned dataset**  
   - Reads `data/final/car_prices.csv` into a pandas DataFrame.

3. **Explores drive wheel vs price**  
   - Shows a sample of the `drivewheel` and `price` columns.  
   - Displays the average price for each drive type (FWD, RWD, 4WD).  
   - Visualises the relationship using bar and box plots.

4. **Performs a statistical test (t-test)**  
   - Compares prices between FWD and RWD cars.  
   - Uses the p-value to decide whether the hypothesis is supported.

The goal is to see if drive wheel configuration has a clear impact on car prices,  
and whether FWD cars are indeed cheaper than RWD cars.
""")
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import os

# -----------------------------
# Step 0: Check that the data file exists
# -----------------------------
st.markdown("### Data Check")

files = os.listdir("data/final")
st.write("Files in `data/final`:", files)

if "car_prices.csv" not in files:
    st.error("❌ 'car_prices.csv' not found in 'data/final' – please check the path.")
    st.stop()  # stop the app if file is missing
else:
    st.success("✅ 'car_prices.csv' found. Proceeding with analysis.")

# -----------------------------
# Step 1: Load data (cached)
# -----------------------------
@st.cache_data
def load_data():
    """Load the car prices dataset."""
    return pd.read_csv("data/final/car_prices.csv")

df = load_data()
# -----------------------------
# Step 2: Page title & description
# -----------------------------
st.title("Hypothesis 04: Drive Wheel Type vs Car Price")

st.markdown("""
**Hypothesis:** Front-wheel drive (FWD) cars are generally cheaper than rear-wheel drive (RWD) cars.

This page analyses the relationship between the `drivewheel` variable and `price`.
""")

with st.expander("🔍 Show sample of data"):
    st.write(df[["drivewheel", "price"]].head())

# -----------------------------
# Step 3: Average price by drivewheel (bar plot)
# -----------------------------
st.subheader("Average Price by Drive Wheel Type")

avg_price = (
    df.groupby("drivewheel")["price"]
      .mean()
      .reset_index()
      .sort_values("price", ascending=False)
)

st.dataframe(avg_price, use_container_width=True)

fig_bar, ax_bar = plt.subplots(figsize=(7, 4))
sns.barplot(data=avg_price, x="drivewheel", y="price", ax=ax_bar, palette="pastel")
ax_bar.set_xlabel("Drive Wheel Type")
ax_bar.set_ylabel("Average Price")
ax_bar.set_title("Average Car Price by Drive Wheel Type")
st.pyplot(fig_bar)

# -----------------------------
# Step 4: Price distribution (box plot)
# -----------------------------
st.subheader("Price Distribution by Drive Wheel Type")

fig_box, ax_box = plt.subplots(figsize=(7, 4))
sns.boxplot(data=df, x="drivewheel", y="price", ax=ax_box)
ax_box.set_xlabel("Drive Wheel Type")
ax_box.set_ylabel("Price")
ax_box.set_title("Price Distribution by Drive Wheel Type")
st.pyplot(fig_box)

# -----------------------------
# Step 5: T-test – FWD vs RWD
# -----------------------------
st.subheader("T-test: FWD vs RWD Prices")

fwd_prices = df[df["drivewheel"] == "fwd"]["price"]
rwd_prices = df[df["drivewheel"] == "rwd"]["price"]

st.write(f"Number of FWD cars: **{len(fwd_prices)}**")
st.write(f"Number of RWD cars: **{len(rwd_prices)}**")

t_stat, p_value = ttest_ind(fwd_prices, rwd_prices, equal_var=False)

st.write(f"**T-test statistic:** {t_stat:.3f}")
st.write(f"**P-value:** {p_value:.4f}")

if p_value < 0.05:
    st.success(
        "✅ There is a statistically significant difference in price between FWD and RWD cars. "
        "This supports the hypothesis that drive wheel type affects car price and that FWD cars tend to be cheaper."
    )
else:
    st.info(
        "ℹ️ There is no statistically significant difference in price between FWD and RWD cars. "
        "The data does not strongly support the hypothesis."
    )
