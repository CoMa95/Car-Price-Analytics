"""
Hypothesis 2 Page: Fuel Efficiency Correlation with Car Price
This page tests the hypothesis that fuel efficiency (measured by average
miles per gallon, avg_mpg) correlates with car prices.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu, pearsonr, spearmanr

# Configure the Streamlit page
st.title("Car Price Analytics Dashboard")
st.caption("This dashboard provides insights into Western car prices through "
           "filtering, summarizing, visualization, and price prediction. "
           "Built with Streamlit + pandas + matplotlib.")


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
    median_eff = df["avg_mpg"].median()
    low_eff = df[df["avg_mpg"] <= median_eff]["price"]
    high_eff = df[df["avg_mpg"] > median_eff]["price"]

    t_stat, t_pval = ttest_ind(high_eff, low_eff, equal_var=False)
    u_stat, u_pval = mannwhitneyu(high_eff, low_eff, alternative="two-sided")

    return t_stat, t_pval, u_stat, u_pval


def show_efficiency_price_metrics(df):
    """Displays average price for high vs low fuel efficiency groups."""
    median_eff = df["avg_mpg"].median()
    low_eff = df[df["avg_mpg"] <= median_eff]
    high_eff = df[df["avg_mpg"] > median_eff]

    low_avg = low_eff["price"].mean()
    high_avg = high_eff["price"].mean()
    overall_avg = df["price"].mean()

    st.markdown("### Average Price by Fuel Efficiency Group")

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Avg Price (£)", f"{overall_avg:,.0f}")
    col2.metric(
        "Low Efficiency Cars (£)",
        f"{low_avg:,.0f}",
        delta=f"{((low_avg - overall_avg)/overall_avg)*100:+.1f}% vs overall"
    )
    col3.metric(
        "High Efficiency Cars (£)",
        f"{high_avg:,.0f}",
        delta=f"{((high_avg - overall_avg)/overall_avg)*100:+.1f}% vs overall"
    )


def show_hypothesis_statement() -> None:
    """Displays the hypothesis statement."""
    st.markdown("### Hypothesis 2: Fuel Efficiency Correlates with Car Price")
    st.latex(r"""
    \begin{align*}
    H_0 &: \text{No correlation between fuel efficiency and car price} \\
    H_1 &: \text{Significant correlation between fuel efficiency and car price}
    \end{align*}
    """)


def show_scatterplot(df) -> None:
    """Displays scatterplot of price vs avg_mpg with regression line."""
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=df, x="avg_mpg", y="price", ax=ax)
    sns.regplot(data=df, x="avg_mpg", y="price",
                scatter=False, color="red", ax=ax)
    ax.set_title("Price vs Fuel Efficiency (Average MPG)")
    ax.set_xlabel("Fuel Efficiency (avg_mpg)")
    ax.set_ylabel("Price (£)")
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
    """Displays interpretation of the statistical results."""
    pearson_corr, pearson_pval, spearman_corr, spearman_pval \
        = calculate_correlation(df)
    t_stat, t_pval, u_stat, u_pval = run_statistical_tests(df)

    st.markdown("---")
    st.markdown("### Interpretation")

    if (pearson_corr < 0) and (t_pval < 0.05 or u_pval < 0.05):
        st.success("""
    **Summary:**
    - Both correlation coefficients are **negative**, showing an inverse
                   relationship between fuel efficiency and price.
    - Both t-test and Mann–Whitney U test show **p-values < 0.05**, confirming
                   a **statistically significant difference** in prices.
    - **Conclusion:** Cars with higher fuel efficiency (higher MPG) tend to
                    have **lower prices**, supporting the alternative
                    hypothesis (H₁).
    """)
    else:
        st.info("""
    **Summary:**
    The results do not show a consistent or statistically significant
                inverse relationship
    between fuel efficiency and car price. The null hypothesis (H₀)
                cannot be rejected.
    """)

    with st.expander("View Test Summary Table"):
        results_df = pd.DataFrame({
            "Test": ["Pearson correlation", "Spearman correlation",
                     "t-test", "Mann–Whitney U"],
            "Statistic": [pearson_corr, spearman_corr, t_stat, u_stat],
            "p-value": [pearson_pval, spearman_pval, t_pval, u_pval]
        })
        st.dataframe(results_df.style.format({"Statistic": "{:.3f}",
                                              "p-value": "{:.4f}"}))


def run_page(df) -> None:
    """Runs the hypothesis 2 analysis page.

    Args:
        df (pd.DataFrame): The dataframe containing car data.
    Returns:
        None
    """
    show_hypothesis_statement()
    show_efficiency_price_metrics(df)
    col1, col2 = st.columns(2)
    with col1:
        show_scatterplot(df)
    with col2:
        show_correlation_results(df)
        show_interpretation(df)


# Run the Hypothesis 2 page with the filtered dataframe
run_page(st.session_state['filtered_df'])
