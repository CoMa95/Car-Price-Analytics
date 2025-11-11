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
import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu, pearsonr, spearmanr


# Configure the Streamlit page
st.title("Car Price Analytics Dashboard")
st.caption("This dashboard provides insights into Western car prices through"
           " filtering, summarizing, visualization, and price prediction."
           " Built with Streamlit + pandas + matplotlib.")


def calculate_correlation(df) -> tuple:
    '''Calculates Pearson and Spearman correlation between fueltype and price.

    Args:
        df (pd.DataFrame)

    Returns: tuple: pearson_corr, pearson_pval, spearman_corr, spearman_pval
    '''

    df['fueltype_encoded'] = df['fueltype'].map({'petrol': 0, 'diesel': 1})
    pearson_corr, pearson_pval = pearsonr(df["fueltype_encoded"], df["price"])
    spearman_corr, spearman_pval = spearmanr(df["fueltype_encoded"], df["price"])
    return pearson_corr, pearson_pval, spearman_corr, spearman_pval


def run_statistical_tests(df) -> tuple:
    """Performs t-test and Mann–Whitney U test on price grouped by fuel
    type.

    Args:
        df (pd.DataFrame)

    Returns: tuple: t_stat, t_pval, u_stat, u_pval
    """
    petrol = df[df['fueltype'] == 'petrol']['price']
    diesel = df[df['fueltype'] == 'diesel']['price']

    t_stat, t_pval = ttest_ind(diesel, petrol, equal_var=False)
    u_stat, u_pval = mannwhitneyu(diesel, petrol, alternative='two-sided')

    return t_stat, t_pval, u_stat, u_pval


def show_price_metrics(df):
    """
    Displays average price overall, for diesel, and for petrol cars.

    Args:
        df (pd.DataFrame)

    Returns: None
    """
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


def show_hypothesis_statement() -> None:
    """Displays the hypothesis statement for Hypothesis 1.

    Returns: None
    """
    st.markdown("### Hypothesis 1: Fuel Type Impacts Car Price")
    st.latex(r"""
    \begin{align*}
    H_0 &: \text{Fuel type has no effect on car price} \\
    H_1 &: \text{Fuel type significantly affects car price}
    \end{align*}
    """)


def plot_boxplot(df) -> None:
    """Displays boxplot of price by fuel type.

    Args:
        df (pd.DataFrame)

    Returns: None"""
    st.markdown("### Price Distribution by Fuel Type")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x='fueltype', y='price', data=df, palette='Set2', ax=ax)
    st.pyplot(fig)
    st.markdown("**Explanation:** The boxplot shows the price distribution by "
                "fuel type. Diesel cars typically have a higher median price "
                "and wider range than petrol cars, suggesting greater "
                "variation among diesel models.")


def plot_violin(df) -> None:
    """Displays violin plot of price by fuel type.

    Args:
        df (pd.DataFrame)

    Returns: None"""
    st.markdown("### Price Distribution by Fuel Type")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.violinplot(x='fueltype', y='price', data=df, palette='Set2', ax=ax)
    st.pyplot(fig)
    st.markdown("**Explanation:** The violin plot reveals that petrol prices "
                "are more tightly clustered, while diesel prices are more "
                "spread out, indicating a broader pricing range.")


def plot_kde(df) -> None:
    """Displays KDE plot of price by fuel type.

    Args:
        df (pd.DataFrame)

    Returns: None"""
    st.markdown("### Price Distribution by Fuel Type")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.kdeplot(data=df, x='price', hue='fueltype', fill=True,
                common_norm=False, palette='Set2', alpha=0.5, ax=ax)
    st.pyplot(fig)
    st.markdown("**Explanation:** This shows that diesel cars are generally "
                "priced higher than petrol cars, with noticeable overlap "
                "in the mid-range price band.")


def show_correlation_results(df) -> None:
    """Displays correlation and statistical test results in metric cards.

    Args:
        df (pd.DataFrame)

    Returns: None
    """
    pearson_corr, pearson_pval, spearman_corr, spearman_pval\
        = calculate_correlation(df)
    t_stat, t_pval, u_stat, u_pval = run_statistical_tests(df)

    st.markdown("### Statistical Test Results")

    # Display correlation and statistical test results
    col1, col2, col3, col4 = st.columns(4)
    # Display Pearson correlation results
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
    # Display Spearman correlation results
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
    # Display t-test and Mann–Whitney U test results
    col5, col6, col7, col8 = st.columns(4)
    # Display t-test statistic
    col5.metric(
        label="t-test statistic",
        value=f"{t_stat:.3f}",
        delta="Positive effect" if t_stat > 0 else "Negative effect"
    )
    # Display t-test p-value
    col6.metric(
        label="t-test p-value",
        value=f"{t_pval:.4f}",
        delta="Significant" if t_pval < 0.05 else "Not Significant"
    )
    # Display Mann–Whitney U test statistic
    col7.metric(
        label="Mann–Whitney U statistic",
        value=f"{u_stat:.3f}",
        delta="Positive effect" if u_stat > 0 else "Negative effect"
    )
    # Display Mann–Whitney U test p-value
    col8.metric(
        label="Mann–Whitney p-value",
        value=f"{u_pval:.4f}",
        delta="Significant" if u_pval < 0.05 else "Not Significant"
    )


def show_interpretation(df) -> None:
    """Displays interpretation of the statistical results for Hypothesis 1.

    Args:
        df (pd.DataFrame)

    Returns: None
    """
    pearson_corr, pearson_pval, spearman_corr, spearman_pval \
        = calculate_correlation(df)
    t_stat, t_pval, u_stat, u_pval = run_statistical_tests(df)

    st.markdown("---")
    st.markdown("### Interpretation")

    if (t_pval < 0.05 or u_pval < 0.05):
        st.success("""
        **Summary:**
        - The p-values for either the t-test and Mann–Whitney U test are below
            0.05, indicating a **statistically significant difference** in car
            prices between petrol and diesel vehicles.
        - This supports the **alternative hypothesis (H₁)** that fuel type
          **significantly affects car price**.
        - Correlation results show that fuel type is related to price
            variation, suggesting manufacturers may price diesel and petrol
            cars differently due to performance, efficiency, or market demand.
        """)
    else:
        st.info("""
        **Summary:**
        - The p-values for both the t-test and Mann–Whitney U test are above
            0.05, meaning there is **no statistically significant difference**
            in prices between petrol and diesel cars.
        - Therefore, we **cannot reject the null hypothesis (H₀)** — fuel type
            does not appear to significantly influence price in this
            dataset.""")

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
    """Runs the Hypothesis 1 page with all components.

    Args:
        df (pd.DataFrame): The dataframe containing car data.

    Returns: None
    """
    show_hypothesis_statement()  # Display hypothesis statement
    show_price_metrics(df)  # Show average price metrics
    col1, col2 = st.columns(2)  # Create two columns for layout
    with col1:
        tab1, tab2, tab3 = st.tabs(["Boxplot", "Violin", "KDE"])
        with tab1:
            plot_boxplot(df)  # Plot boxplot of price by fuel type
        with tab2:
            plot_violin(df)  # Plot violin plot of price by fuel type
        with tab3:
            plot_kde(df)  # Plot KDE of price by fuel type
    with col2:
        show_correlation_results(df)  # Show correlation and test results
        show_interpretation(df)  # Show interpretation


# Execute the page with filtered data
run_page(st.session_state['filtered_df'])
