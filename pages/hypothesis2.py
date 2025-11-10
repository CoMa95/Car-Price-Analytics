import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu

# Configure the Streamlit page
st.title("Car Price Analytics Dashboard")
st.caption("This dashboard provides insights into Western car prices through filtering, summarizing, visualization, and price prediction. Built with Streamlit + pandas + matplotlib.")

def show_hypothesis_statement():
    st.markdown("### Hypothesis 2: Fuel Efficiency Correlates with Car Price")
    st.latex(r"""
    \begin{align*}
    H_0 &: \text{No correlation between fuel efficiency and car price} \\
    H_1 &: \text{Significant correlation between fuel efficiency and car price}
    \end{align*}
    """)

def show_scatterplot(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=df, x="avg_mpg", y="price", ax=ax)
    sns.regplot(data=df, x="avg_mpg", y="price", scatter=False, color="red", ax=ax)
    ax.set_title("Price vs Fuel Efficiency (Average MPG)")
    ax.set_xlabel("Fuel Efficiency (avg_mpg)")
    ax.set_ylabel("Price (£)")
    st.pyplot(fig)

def show_correlation_results(df):
    # --- Correlation Tests ---
    pearson_corr = df["avg_mpg"].corr(df["price"], method="pearson")
    spearman_corr = df["avg_mpg"].corr(df["price"], method="spearman")

    # --- t-test and Mann–Whitney U Test ---
    median_eff = df["avg_mpg"].median()
    low_eff = df[df["avg_mpg"] <= median_eff]["price"]
    high_eff = df[df["avg_mpg"] > median_eff]["price"]

    t_stat, t_pval = ttest_ind(high_eff, low_eff, equal_var=False)
    u_stat, u_pval = mannwhitneyu(high_eff, low_eff, alternative="two-sided")

    st.markdown("### Statistical Test Results")

    col1, col2 = st.columns(2)
    col1.metric(
        label="Pearson Correlation",
        value=f"{pearson_corr:.3f}",
        delta="Negative" if pearson_corr < 0 else "Positive"
    )
    col2.metric(
        label="Spearman Correlation",
        value=f"{spearman_corr:.3f}",
        delta="Negative" if spearman_corr < 0 else "Positive"
    )

    col5, col6 = st.columns(2)
    col5.metric(
        label="t-test statistic",
        value=f"{t_stat:.3f}",
        delta=None
    )
    col6.metric(
        label="Mann–Whitney U statistic",
        value=f"{u_stat:.3f}",
        delta=None
    )

    col3, col4 = st.columns(2)
    col3.metric(
        label="t-test p-value",
        value=f"{t_pval:.4f}",
        delta="Significant" if t_pval < 0.05 else "Not Significant"
    )
    col4.metric(
        label="Mann–Whitney p-value",
        value=f"{u_pval:.4f}",
        delta="Significant" if u_pval < 0.05 else "Not Significant"
    )

def show_interpretation(df):
    # --- Correlation Tests ---
    pearson_corr = df["avg_mpg"].corr(df["price"], method="pearson")
    spearman_corr = df["avg_mpg"].corr(df["price"], method="spearman")

    # --- t-test and Mann–Whitney U Test ---
    median_eff = df["avg_mpg"].median()
    low_eff = df[df["avg_mpg"] <= median_eff]["price"]
    high_eff = df[df["avg_mpg"] > median_eff]["price"]

    t_stat, t_pval = ttest_ind(high_eff, low_eff, equal_var=False)
    u_stat, u_pval = mannwhitneyu(high_eff, low_eff, alternative="two-sided")


    # --- Interpretation Section ---
    st.markdown("---")
    st.markdown("### Interpretation")

    if (pearson_corr < 0) and (t_pval < 0.05 or u_pval < 0.05):
        st.success("""
    **Summary:**  
    - Both correlation coefficients are **negative**, showing an inverse relationship between fuel efficiency and price.  
    - Both t-test and Mann–Whitney U test show **p-values < 0.05**, confirming a **statistically significant difference** in prices.  
    - **Conclusion:** Cars with higher fuel efficiency (higher MPG) tend to have **lower prices**, supporting the alternative hypothesis (H₁).
    """)
    else:
        st.info("""
    **Summary:**  
    The results do not show a consistent or statistically significant inverse relationship 
    between fuel efficiency and car price. The null hypothesis (H₀) cannot be rejected.
    """)

    # --- Show test table for reference ---
    with st.expander("View Test Summary Table"):
        results_df = pd.DataFrame({
            "Test": ["Pearson correlation", "Spearman correlation", "t-test", "Mann–Whitney U"],
            "Statistic": [pearson_corr, spearman_corr, t_stat, u_stat],
            "p-value": [None, None, t_pval, u_pval]
        })
        st.dataframe(results_df.style.format({"Statistic": "{:.3f}", "p-value": "{:.4f}"}))

def run_page(df):
    show_hypothesis_statement()
    show_scatterplot(df)
    show_correlation_results(df)
    show_interpretation(df)

run_page(st.session_state['filtered_df'])
