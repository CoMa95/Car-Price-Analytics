"""
Hypothesis 03 - Car Body Type vs Price

This page analyzes how car body types (such as sedan, hatchback, convertible, etc.)
affect car prices. It loads filtered data from the dashboard, summarizes average prices
for each body type, and visualizes the results using bar and box plots.
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def run_page(df: pd.DataFrame):
    # Page title
    st.title("Hypothesis 03 - Car Body Type vs Price")

    st.markdown("""
    *Hypothesis:*  
    Some car body types (e.g., sedan, hatchback, SUV) have systematically higher prices than others.

    This page analyzes the relationship between **car body type (carbody)** and *price*.
    """)

    # Show sample of data
    with st.expander("Show sample of data"):
        st.write(df[["carbody", "price"]].head())

    # Summary statistics
    st.subheader("Summary statistics by car body type")

    body_summary = (
        df.groupby("carbody")["price"]
          .agg(["count", "mean", "median", "min", "max"])
          .reset_index()
          .sort_values("mean", ascending=False)
    )

    st.dataframe(body_summary)

    # Bar plot - Average Price by Body Type
    st.subheader("Average Car Price by Body Type")

    fig_bar, ax_bar = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x="carbody",
        y="mean",
        data=body_summary,
        ax=ax_bar,
        palette="pastel"
    )
    ax_bar.set_xlabel("Car Body Type")
    ax_bar.set_ylabel("Average Price")
    ax_bar.set_title("Average Car Price by Body Type")
    ax_bar.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    st.pyplot(fig_bar)

    # Box plot - Price Distribution
    st.subheader("Price Distribution by Car Body Type")

    fig_box, ax_box = plt.subplots(figsize=(8, 5))
    sns.boxplot(
        x="carbody",
        y="price",
        data=df,
        ax=ax_box,
        palette="Set3"
    )
    ax_box.set_xlabel("Car Body Type")
    ax_box.set_ylabel("Price")
    ax_box.set_title("Price Distribution by Car Body Type")
    ax_box.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    st.pyplot(fig_box)

    # Footer
    st.markdown("---")
    st.caption("Page created by Hidaia")


# Run page using filtered data if available
if "filtered_df" in st.session_state:
    run_page(st.session_state["filtered_df"])
else:
    df_full = pd.read_csv("data/final/car_prices.csv")
    run_page(df_full)