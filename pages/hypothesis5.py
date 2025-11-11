"""
Hypothesis 5 Page: "There is at least 1 feature with a statistically significant correlation to Price"

This page documents the process through which we investigated the above hypothesis and discovered a 
set of promising predictors.

It includes visualizations and statistical tests.
"""

# import libraries
import streamlit as st
import pandas as pd
from scipy.stats import spearmanr, mannwhitneyu, kruskal
from pathlib import Path

# ---------------- Page config ----------------
st.title("Western Car Price System Analysis")
st.caption("This dashboard provides insights into Western car prices through "
           "filtering, summarizing, visualization, and price prediction. "
           "Built with Streamlit + pandas + matplotlib.")

# ---------------- Hypothesis Statement ----------------
st.markdown("### Hypothesis 5: There is at least 1 feature with a statistically significant correlation to Price")
st.latex(r"""
\begin{align*}
H_0 &: \text{No feature presents with a statistically significant correlation to Price} \\
H_1 &: \text{At least one feature presents with a statistically significant correlation to Price}
\end{align*}
""")

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

# declare the categorical and continuous variables
cats = ['symboling', 'fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel', 'enginetype', 
        'cylindernumber', 'fuelsystem', 'manufacturer', 'compressionratio_bin']
conts = ['wheelbase', 'carlength', 'carwidth', 'carheight','curbweight', 'enginesize','boreratio', 
        'stroke', 'horsepower', 'peakrpm', 'citympg', 'highwaympg', 'price_per_hp', 
        'power_to_weight_ratio','engine_efficiency', 'avg_mpg', 'price_per_mpg']
target = 'price'

# separate cats into binary and multi-category
cats_binary = [cat for cat in cats if df[cat].nunique() == 2]
cats_multi = [cat for cat in cats if df[cat].nunique() > 2]

# drop manufacurturer due to high cardinality
cats_multi.remove('manufacturer')

# ---------------- Define statistical tests ----------------

# function to compute Spearman correlation
def spearman_feature_test(df, predictors, target):
    """
    Computes Spearman rank correlation between each predictor and target.

    Parameters:
        df : pd.DataFrame
            Input dataframe containing predictors and target.
        predictors : list
            List of predictor variable names (continuous or ordinal).
        target : str
            Target variable name (continuous).

    Returns:
        pd.DataFrame
            DataFrame with columns: ['feature', 'spearman_corr', 'p_value']
    """
    results = []

    for feature in predictors:
        # Drop NA pairs to avoid alignment issues
        valid = df[[feature, target]].dropna()

        # Compute Spearman correlation
        corr, pval = spearmanr(valid[feature], valid[target])

        results.append({
            'feature': feature,
            'spearman_corr': round(corr, 3),
            'p_value': round(pval, 3)
        })

    results_df = pd.DataFrame(results).sort_values(by='spearman_corr', ascending=False).reset_index(drop=True)
    return results_df

# function to perform non-parametric tests for categorical features
def categorical_feature_tests(df, binary_features, multi_features, target):
    """
    Performs non-parametric tests (Mann-Whitney U and Kruskal-Wallis)
    between categorical predictors and a continuous target variable.

    Parameters
        df : pd.DataFrame
            Input dataframe containing all variables.
        binary_features : list
            List of binary categorical feature names (must have exactly 2 unique values).
        multi_features : list
            List of multi-level categorical feature names (3 or more unique values).
        target : str
            Name of the continuous target variable.

    Returns
        pd.DataFrame
            DataFrame with columns: ['feature', 'test', 'statistic', 'p_value', 'n_levels']
    """
    results = []

    # for binary features (Mann-Whitney U test)
    for feature in binary_features:
        valid = df[[feature, target]]
        groups = valid.groupby(feature)[target].apply(list)

        stat, p = mannwhitneyu(groups.iloc[0], groups.iloc[1], alternative='two-sided')
        results.append({
            'feature': feature,
            'test': 'Mann-Whitney U',
            'statistic': round(stat, 3),
            'p_value': round(p, 3)
        })


    # for multi-level features (Kruskal-Wallis H test) 
    for feature in multi_features:
        valid = df[[feature, target]]
        groups = valid.groupby(feature)[target].apply(list)

        stat, p = kruskal(*groups)
        results.append({
            'feature': feature,
            'test': 'Kruskal-Wallis H',
            'statistic':round(stat, 3),
            'p_value': round(p, 3)
        })

    results_df = pd.DataFrame(results)
    return results_df

# ---------------- Run statistical tests ----------------

spearman_results = spearman_feature_test(df, conts, target)
cat_results_df = categorical_feature_tests(df, cats_binary, cats_multi, target)


# ---------------- Continuous Features Section ----------------
st.subheader("Part 1: Continuous Features")

st.markdown(
    """
    As car price and several other continuous variables were not normally distributed, 
    the relationship between these was assessed using
    the :green[**Spearman rank correlation test**], due to its non-parametric nature.  
    The Spearman coefficient (ρ) measures monotonic relationships, making it
    suitable even when variables are not linearly related.
    """
)

# Display table
st.dataframe(
    spearman_results.head(50), 
    use_container_width=True,
    height=200
)

# table description
st.markdown(
    """
    **Table 1.** All continuous features were ranked by their Spearman correlation with price. Features with
    a p-value < 0.05 are considered to have a statistically significant correlation with price
    """
)

# Add figure with context
st.markdown(
    """
    :orange[**Multicollinearity**] - Many continuous features were highly correlated with each other, which can affect model performance and interpretation. Features were
    eliminated based on domain knowledge and correlation strength to reduce redundancy.
    The correlation heatmap below shows the final selection of continuous variables against price.
    """
)
st.image('figures/corr_mat_final_selection.png', use_container_width=True, caption=None)

# Add figure with context
st.markdown(
    """
    **Figure 1.** Correlation heatmap of selected continuous.  
    Darker colors indicate stronger correlations (both positive and negative).
    """
)

st.divider()  # visual separator between sections

# ---------------- Categorical Features Section ----------------
st.subheader("Part 2: Categorical Features")

st.markdown(
    """
    For categorical features, non-parametric tests were used to assess their relationship with price.  
    The :green[**Mann-Whitney U test**] was applied to binary categorical features, while the  
    :green[**Kruskal-Wallis H test**] was used for multi-class categorical features.
    The table below summarizes the results of **statistical tests for categorical features**,  
    including both binary and multi-class variables.
    """
)

# Display table
st.dataframe(
    cat_results_df.head(50),
    use_container_width=True,
    height=200
)

# Add figure with context
st.markdown(
    """
    :orange[**Class Imbalances**] - Many categorical features presented with very imbalanced classes, which can affect the reliability of statistical tests and any conclusions drawn.
    Thus, such features were excluded from further analysis.
    The violin plots below show the final selection of categorical variables.
    """
)

# Add figure with context
st.markdown(
    """
    **Figure 2.** Visualization of categorical feature effects on car price, using violin plots.  
    Wider sections represent higher density of observations; median lines indicate price centers per group.
    """
)
st.image('figures/categorical_violin_final_selection.png', use_container_width=True, caption=None)

st.divider()

# ---------------- Conclusion ----------------
st.subheader("Conclusion")

st.markdown(
    """
    *After feature engineering, the dataset contained over 30 predictor features. Through a 
    thorough statistical and visual analysis, a selection of relevant predictors was created. 
    Further curation to address the issues of multicollinearity and class imbalances have
    narrowed the feature set to just 10 features:*
    """
)
st.success("'curbweight', 'horsepower', 'price_per_hp', 'wheelbase', 'boreratio', " \
"'power_to_weight_ratio', 'carbody', 'drivewheel', 'compressionratio_bin', 'symboling_binned'")

