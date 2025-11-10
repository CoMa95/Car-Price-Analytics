"""
Hypothesis 1 Page: Fuel Type Impact on Car Price

This page tests the hypothesis that fuel type (petrol vs diesel) has a
significant effect on car prices.

It includes visualizations and statistical tests (pearson, spearman, t-test
and Mann–Whitney U test) to analyze the impact of fuel type on car prices.
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu, pearsonr, spearmanr


# Configure the Streamlit page
st.title("Car Price Analytics Dashboard")
st.caption("This dashboard provides insights into Western car prices through"
           " filtering, summarizing, visualization, and price prediction."
           " Built with Streamlit + pandas + matplotlib.")


def calculate_correlation(df) -> tuple:
    """
    Calculates Pearson and Spearman correlation between avg_mpg and price.
    Args:
        df (pd.DataFrame)
    Returns:
        tuple: pearson_corr, pearson_pval, spearman_corr, spearman_pval
    """
    pearson_corr, pearson_pval = pearsonr(df["avg_mpg"], df["price"])
    spearman_corr, spearman_pval = spearmanr(df["avg_mpg"], df["price"])
    return pearson_corr, pearson_pval, spearman_corr, spearman_pval


def run_statistical_tests(df) -> tuple:
    """
    Performs t-test and Mann–Whitney U test on price grouped by fuel
    efficiency.
    Args:
        df (pd.DataFrame)
    Returns:
        tuple: t_stat, t_pval, u_stat, u_pval
    """
    petrol = df[df['fueltype'] == 'petrol']['price']
    diesel = df[df['fueltype'] == 'diesel']['price']

    t_stat, t_pval = ttest_ind(diesel, petrol, equal_var=False)
    u_stat, u_pval = mannwhitneyu(diesel, petrol, alternative='two-sided')

    return t_stat, t_pval, u_stat, u_pval


def show_price_metrics(df):
    """Displays average price overall, for diesel, and for petrol cars."""
    overall_avg = df["price"].mean()
    diesel_avg = df[df["fueltype"] == "diesel"]["price"].mean()
    petrol_avg = df[df["fueltype"] == "petrol"]["price"].mean()

    st.markdown("### Average Car Prices by Fuel Type")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="Overall Average Price (£)",
        value=f"{overall_avg:,.0f}"
    )
    col2.metric(
        label="Average Diesel Price (£)",
        value=f"{diesel_avg:,.0f}",
        delta=f"{((diesel_avg - overall_avg) / overall_avg) * 100:+.1f}% vs\
              overall"
    )
    col3.metric(
        label="Average Petrol Price (£)",
        value=f"{petrol_avg:,.0f}",
        delta=f"{((petrol_avg - overall_avg) / overall_avg) * 100:+.1f}% vs\
              overall"
    )


def show_hypothesis_statement():
    """Displays the hypothesis statement for Hypothesis 1."""
    st.markdown("### Hypothesis 1: Fuel Type Impacts Car Price")
    st.latex(r"""
    \begin{align*}
    H_0 &: \text{Fuel type has no effect on car price} \\
    H_1 &: \text{Fuel type significantly affects car price}
    \end{align*}
    """)


def plot_boxplot(df):
    """Displays boxplot of price by fuel type."""
    st.markdown("### Price Distribution by Fuel Type")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x='fueltype', y='price', data=df, palette='Set2', ax=ax)
    st.pyplot(fig)


def show_correlation_results(df) -> None:
    """Displays correlation and statistical test results in metric cards."""
    pearson_corr, pearson_pval, spearman_corr, spearman_pval\
        = calculate_correlation(df)
    t_stat, t_pval, u_stat, u_pval = run_statistical_tests(df)

    st.markdown("### Statistical Test Results")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        label="Pearson Correlation",
        value=f"{pearson_corr:.3f}",
        delta="Negative" if pearson_corr < 0 else "Positive"
    )
    col2.metric(
        label="Pearson p-value",
        value=f"{pearson_pval:.4f}",
        delta="Significant" if pearson_pval < 0.05 else "Not Significant"
    )
    col3.metric(
        label="Spearman Correlation",
        value=f"{spearman_corr:.3f}",
        delta="Negative" if spearman_corr < 0 else "Positive"
    )
    col4.metric(
        label="Spearman p-value",
        value=f"{spearman_pval:.4f}",
        delta="Significant" if spearman_pval < 0.05 else "Not Significant"
    )
    col5, col6, col7, col8 = st.columns(4)
    col5.metric(
        label="t-test statistic",
        value=f"{t_stat:.3f}",
        delta="Positive effect" if t_stat > 0 else "Negative effect"
    )
    col6.metric(
        label="t-test p-value",
        value=f"{t_pval:.4f}",
        delta="Significant" if t_pval < 0.05 else "Not Significant"
    )
    col7.metric(
        label="Mann–Whitney U statistic",
        value=f"{u_stat:.3f}",
        delta="Positive effect" if u_stat > 0 else "Negative effect"
    )
    col8.metric(
        label="Mann–Whitney p-value",
        value=f"{u_pval:.4f}",
        delta="Significant" if u_pval < 0.05 else "Not Significant"
    )


def show_interpretation(df) -> None:
    """Displays interpretation of the statistical results for Hypothesis 1."""
    pearson_corr, pearson_pval, spearman_corr, spearman_pval \
        = calculate_correlation(df)
    t_stat, t_pval, u_stat, u_pval = run_statistical_tests(df)

    st.markdown("---")
    st.markdown("### Interpretation")

    if (t_pval < 0.05 or u_pval < 0.05):
        st.success("""
        **Summary:**
        - The p-values for both the t-test and Mann–Whitney U test are below
            0.05, indicating a **statistically significant difference** in car
            prices between petrol and diesel vehicles.
        - This supports the **alternative hypothesis (H₁)** that fuel type
          **significantly affects car price**.
        - Correlation results show that fuel type is related to price
            variation, suggesting manufacturers may price diesel and petrol
            cars differently due to performance, efficiency, or market demand.
        """)
    else:
        st.info(
        """
        **Summary:**
        - The p-values for both the t-test and Mann–Whitney U test are above
            0.05, meaning there is **no statistically significant difference**
                in prices between petrol and diesel cars.
        - Therefore, we **cannot reject the null hypothesis (H₀)** — fuel type
            does not appear to significantly influence price in this dataset.
        """
        )

    with st.expander("View Test Summary Table"):
        import pandas as pd
        results_df = pd.DataFrame({
            "Test": ["Pearson correlation", "Spearman correlation",
                     "t-test", "Mann–Whitney U"],
            "Statistic": [pearson_corr, spearman_corr, t_stat, u_stat],
            "p-value": [pearson_pval, spearman_pval, t_pval, u_pval]
        })
        st.dataframe(results_df.style.format({"Statistic": "{:.3f}",
                                              "p-value": "{:.4f}"}))


def run_page(df):
    """Runs the Hypothesis 1 page with all components."""
    show_hypothesis_statement()
    show_price_metrics(df)
    col1, col2 = st.columns(2)
    with col1:
        plot_boxplot(df)
    with col2:
        show_correlation_results(df)
        show_interpretation(df)


run_page(st.session_state['filtered_df'])
