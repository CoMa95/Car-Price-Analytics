# 🚗 Car Price Analysis Dashboard

Car Price Analysis Dashboard is an interactive data exploration and hypothesis testing tool built using Streamlit.The app allows users to explore relationships between car specifications and prices, validate hypotheses, and visualise insights through interactive charts. It was developed as part of the Code Institute Hackathon – Dashboard Essentials, using Python and data analytics techniques to produce actionable insights.

## ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

## 📊 Dataset Content

The dataset used in this project is sourced from the  [Car Price Prediction Dataset on Kaggle](https://www.kaggle.com/datasets/hellbuoy/car-price-prediction).

It contains detailed information about various car models, including:

- **Specifications:** horsepower, engine size, wheelbase, weight, and dimensions
- **Categorical attributes:** fuel type, drive wheel, body style, manufacturer, and engine type
- **Target variable:** price (in USD)

After cleaning and feature engineering, the dataset included several derived variables such as:

- `price_per_hp` – price per horsepower
- `power_to_weight_ratio` – horsepower divided by curb weight
- `engine_efficiency` – horsepower divided by engine size
- `avg_mpg` – combined fuel efficiency based on city and highway mileage

## 💼 Business Requirements

The primary business goal is to identify which factors most strongly influence car prices and provide an interactive tool for exploring these relationships.

Specific business requirements include:

1. Understand price drivers – Determine which car features (engine size, horsepower, fuel type, etc.) have the greatest impact on price.
2. Compare fuel efficiency and cost – Analyse whether more fuel-efficient cars are cheaper or more expensive.
3. Identify manufacturer trends – Compare average prices, engine efficiency, and performance metrics across manufacturers.
4. Provide an interactive dashboard – Allow users to apply filters and drill down into subsets of data to explore patterns dynamically.

## 🧠 Hypotheses and Validation

The following hypotheses were tested using statistical and visual analysis:

1. Fuel type impacts car price.\
*Validation:* Independent samples T-test and boxplots comparing average prices between fuel types (petrol vs diesel).
2. Fuel efficiency is inversely correlated with price.\
*Validation:* Correlation analysis, scatter plots, and Mann–Whitney U test on high vs low efficiency groups.
3. Car body style influences car price.\
*Validation:* ANOVA and boxplots comparing mean prices across body types (sedan, hatchback, convertible, etc.).
4. Front wheel drive cars are cheaper than rear wheel drive cars.\
*Validation:* T-test and group comparisons using bar and box plots.
5. Top predictors of price can be identified through regression modelling.\
*Validation:* Multiple linear regression model trained on key numerical predictors to assess variable importance.

## 🧩 Project Plan

### High-level Steps

1. Data Collection – Load dataset from Kaggle (car_prices.csv).
2. Data Cleaning – Handle missing values, remove duplicates, and standardise categorical values (e.g. convert “gas” → “petrol”).
3. Exploratory Data Analysis (EDA) – Explore distributions, correlations, and outliers.
4. Feature Engineering – Create derived variables for improved interpretability.
5. Hypothesis Testing – Perform statistical tests and visual validation for each hypothesis.
6. Model Building – Train and evaluate a regression model to identify top predictors of car price.
7. Dashboard Development – Build an interactive Streamlit app with filters and visualisations.
8. Deployment – Deploy final dashboard to Streamlit Cloud.

### Methodology Rationale

- **Python (pandas, numpy)** for data cleaning and transformation.
- **Statistical testing (scipy)** for hypothesis validation.
- **Plotly and Seaborn** for high-quality, interactive visualisation.
- **scikit-learn** for regression modelling and predictor ranking.
- **Streamlit** for interactivity and communication of results.

## 🧭 Mapping Business Requirements to Visualisations

| Business Requirement        | Visualisation Type | Rationale |
|-----------------------------|--------------------|-----------|
| Fuel type impacts car price | Boxplot & T-test   | Compare price distributions by fuel type |
| Fuel efficiency vs price | Scatter plot & correlation |Show inverse trend between price and efficiency |
| Car body style influences price | Boxplot & ANOVA | Compare price averages across body styles |
| Drive type comparison | Grouped bar chart & T-test | Show whether FWD cars are cheaper than RWD |
| Identify top predictors | Feature importance plot | Show which variables most strongly predict price |
| Interactive dashboard | Streamlit filters & plots | Allow user-driven data exploration |

## 🔍 Analysis Techniques Used

- Descriptive statistics – means, medians, and spreads for numeric variables.
- Correlation analysis – Pearson and Spearman coefficients.
- Inferential tests – T-tests, Mann–Whitney U tests, and ANOVA for categorical group comparisons.
- Regression modelling – Multiple linear regression to identify predictors.
- Visual analytics – Heatmaps, scatter plots, boxplots, and bar charts.

### Limitations

- Dataset size limited the complexity of models used.
- Price data may not account for regional or inflationary effects.
- Some body styles and drive types had few examples, limiting test power.

### Generative AI Contributions

- Helped draft hypotheses, optimise code, and streamline dashboard layout.
- Supported the creation of structured test scripts and markdown documentation.

## ⚖️ Ethical Considerations

- Data privacy: Dataset is anonymised and publicly available.
- Bias: Some manufacturers are overrepresented, possibly biasing results.
- Fairness: Non-parametric tests were used to handle unequal variances.
- Transparency: All cleaning and transformation steps are documented in the notebooks.

## 🖥️ Dashboard Design

### Dashboard Pages

1. **Overview**
    - Dataset summary and KPIs (e.g., average price, average MPG).
    - Correlation heatmap of numeric features.
2. **Hypothesis 1: Fuel Type Comparison**
    - Box Plot showing the distribution of prices by fuel type.
    - Violin Plot illustrating the spread of price by fuel type.
    - KDE Plot showing the density distribution of car prices by fuel
        type, highlighting where price values are most concentrated
        and how they differ between fuel types.
    - T-Test and Mann–Whitney U Test conducted to assess whether price differences between fuel types are statistically significant.
    - Pearson and Spearman correlation tests performed to examine the strength and direction of relationships between fuel type and price.
    - Summary statistics (mean and median prices) used to contextualise the findings.
3. Hypothesis 2: Fuel Efficiency and Price Relationship
    - Scatter Plot with regression line showing the relationship between fuel efficiency (average MPG) and car price, illustrating the strength and direction of correlation.
    - Heatmap visualising correlations between key numerical features, highlighting how fuel efficiency relates to price and other performance variables.
    - Bubble Plot displaying the combined effect of fuel efficiency, engine size, and price, providing a multivariate view of how these factors interact.
    - Pearson and Spearman correlation tests conducted to evaluate both linear and monotonic relationships between fuel efficiency and price.
    - T-Test and Mann–Whitney U Test performed to determine whether price differences between cars with varying fuel efficiency levels are statistically significant.
    - Descriptive statistics (mean MPG and average price) used to support and contextualise findings.
4. Hypothesis 3: Car body style influences car price
    - Hidaia please write your description here.
5. Hypothesis 4: Front wheel drive cars are cheaper thatn rear wheel drive
    - Hidaia please write you description of page here.
6. Hypothesis 5: What are features which highly predict price?
    - Cosmin please write your description here.
7. Price Predictor Page
    - Cosmin please put your description here.
8. Insights Page
    - Key takeaways and conclusions from all analyses.

### Communication

- Interactive visuals (Plotly) allow exploration by non-technical users.
- Technical insights are summarised with statistical output text and markdown explanations.

## Unfixed Bugs

**NaN Error When Filters Exclude a Group:**\
On both hypothesis pages, when user-applied filters remove all records for a category (e.g. one fuel type, drive wheel, or body style), the corresponding statistical test or group mean calculation can return NaN or raise a ValueError.

This happens because functions such as ttest_ind() and groupby().mean() require non-empty sample groups to operate correctly.
The planned fix is to add a validation step that checks whether both comparison groups contain data before running the test, and display a user-friendly message if one group is empty.
This issue does not affect other dashboard functionality or visuals.

## Development Roadmap

### Challenges

- **Repository Desynchronisation:** \
    One team member’s local repository fell significantly behind the others, causing version conflicts and missing updates. This required coordinated effort to resynchronise branches, rebase changes, and ensure all code and data files were correctly aligned before deployment. The team used GitHub’s pull request history and commit comparison tools to identify discrepancies and restore consistency. Although it delayed some progress, it improved everyone’s understanding of version control best practices.
- **Filter-Related NaN Errors:**\
    Filters excluding all records from one group on hypothesis pages caused NaN or empty sample errors during statistical tests. This will be resolved in future updates by validating group data before running tests.
- **Streamlit Session State Management:**\
    Maintaining consistent filters across multiple pages introduced complexity. The team used `st.session_state` to store global filters, though further optimisation is planned.
- **Responsive Layout and Performance:**\
    Some larger visualisations caused temporary lag or layout stretching on smaller screens. Future iterations will include layout tuning and caching improvements.

### Next Steps and Skills to Learn

- **Version Control Mastery:**\
    Continue improving Git and GitHub collaboration practices — particularly resolving merge conflicts, using branching workflows, and managing pull requests effectively.
- **Advanced Streamlit Techniques:**\
    Learn more about session state optimisation, dynamic page navigation, and responsive dashboard design.
- **Machine Learning Modelling:**\
    Build on the regression model by experimenting with tree-based or ensemble models (e.g., Random Forest, XGBoost) to improve prediction accuracy.
- **Performance Optimisation:**\
    Explore caching strategies, modularisation, and profiling to make Streamlit apps faster and more scalable.

## Deployment

### Streamlit Cloud

The app was deployed using [Streamlit Cloud](https://streamlit.io).

Live Link: [https://car-analytics-codeinstitute.streamlit.app/](https://car-analytics-codeinstitute.streamlit.app/)

(Replace with your actual Streamlit deployment link)

#### Deployment Steps

1. Push project repository to GitHub.
2. Log in to Streamlit Cloud.
3. Create a new app, select your repository and main branch.
4. Set the entry point to dashboard_app.py.
5. Include all dependencies in requirements.txt.
6. Deploy the app — Streamlit builds and hosts automatically.

## 🧰 Main Data Analysis Libraries

| Library        | Purpose              | Example Usage                                      |
|----------------|----------------------|----------------------------------------------------|
| pandas         | Data manipulation    | ```df.groupby('fueltype')['price'].mean()```       |
| numpy          | Numeric operations   | ```np.log(df['price'])```                          |
| matplotlib     | Static plots         | ```plt.hist(df['price'], bins=20)```               |
| seaborn        | Statistical plots    | ```sns.boxplot(x='fueltype', y='price', data=df)```|
| plotly.express | Interactive visuals  | ```px.scatter(df, x='horsepower', y='price')```    |
| scipy.stats    | Hypothesis testing   | ```ttest_ind(group1, group2)```                    |
| scikit-learn   | Regression modelling | ```LinearRegression().fit(X_train, y_train)```     |
| streamlit      | Dashboard interface  | ```st.plotly_chart(fig)```                         |

## 🙏 Credits

### Content

- Dataset: [Car Price Prediction Dataset – Kaggle](https://www.kaggle.com/datasets/hellbuoy/car-price-prediction)
- Code Institute Hackathon project structure
- Streamlit and Plotly documentation
- Stack Overflow for troubleshooting Streamlit state management
- Assistance and co-authoring support by ChatGPT (OpenAI GPT-5), ideation, code optimisation, hypothesis design, documentation checking, and Streamlit integration support

## 💬 Acknowledgements

Special thanks to:

- Code Institute Hackathon mentors for their guidance and feedback
- Team members for collaboration, testing, and deployment
- OpenAI ChatGPT (GPT-5) for providing technical writing, code refinement, and analytical assistance
