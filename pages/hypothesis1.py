import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu

# Configure the Streamlit page
st.session_state["current_page"] = "Hypothesis 1"
st.title("Car Price Analytics Dashboard")
st.caption("This dashboard provides insights into Western car prices through filtering, summarizing, visualization, and price prediction. Built with Streamlit + pandas + matplotlib.")

# --- Define or import your section functions ---
def show_hypothesis_statement():
    st.markdown("### Hypothesis 1: Fuel Type Impacts Car Price")
    st.latex(r"""
    \begin{align*}
    H_0 &: \text{Fuel type has no effect on car price} \\
    H_1 &: \text{Fuel type significantly affects car price}
    \end{align*}
    """)

def plot_boxplot(df):
    st.markdown("### Price Distribution by Fuel Type")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x='fueltype', y='price', data=df, palette='Set2', ax=ax)
    st.pyplot(fig)

def run_tests(df):
    """Performs t-test and Mann–Whitney."""
    petrol = df[df['fueltype'] == 'petrol']['price']
    diesel = df[df['fueltype'] == 'diesel']['price']

    t_stat, t_pval = ttest_ind(diesel, petrol, equal_var=False)
    u_stat, u_pval = mannwhitneyu(diesel, petrol, alternative='two-sided')

    return t_pval, u_pval

def show_result_cards(t_pval, u_pval):
    col1, col2 = st.columns(2)
    col1.metric("t-test p-value", f"{t_pval:.4f}",
                delta="Significant" if t_pval < 0.05 else "Not Significant")
    col2.metric("Mann–Whitney p-value", f"{u_pval:.4f}",
                delta="Significant" if u_pval < 0.05 else "Not Significant")

    st.divider()
    if t_pval < 0.05 or u_pval < 0.05:
        st.success("✅ Fuel type has a significant effect on car price.")
    else:
        st.info("ℹ️ No statistically significant difference found.")

def run_page(df):
    show_hypothesis_statement()
    plot_boxplot(df)
    t_pval, u_pval = run_tests(df)
    show_result_cards(t_pval, u_pval)


# Load filtered dataframe from session state
run_page(st.session_state['filtered_df'])

