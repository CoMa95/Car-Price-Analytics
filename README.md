# 🚗 Car Price Analysis Dashboard

Car Price Analysis Dashboard is an interactive data exploration and hypothesis testing tool built using Streamlit.The app allows users to explore relationships between car specifications and prices, validate hypotheses, and visualise insights through interactive charts. It was developed as part of the Code Institute Hackathon – Dashboard Essentials, using Python and data analytics techniques to produce actionable insights.

# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)


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
*Validation:* M linear regression model trained on key numerical predictors to assess variable importance.

## Project Plan
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

## The rationale to map the business requirements to the Data Visualisations
* List your business requirements and a rationale to map them to the Data Visualisations

## Analysis techniques used
* List the data analysis methods used and explain limitations or alternative approaches.
* How did you structure the data analysis techniques. Justify your response.
* Did the data limit you, and did you use an alternative approach to meet these challenges?
* How did you use generative AI tools to help with ideation, design thinking and code optimisation?

## Ethical considerations
* Were there any data privacy, bias or fairness issues with the data?
* How did you overcome any legal or societal issues?

## Dashboard Design
* List all dashboard pages and their content, either blocks of information or widgets, like buttons, checkboxes, images, or any other item that your dashboard library supports.
* Later, during the project development, you may revisit your dashboard plan to update a given feature (for example, at the beginning of the project you were confident you would use a given plot to display an insight but subsequently you used another plot type).
* How were data insights communicated to technical and non-technical audiences?
* Explain how the dashboard was designed to communicate complex data insights to different audiences. 

## Unfixed Bugs
* Please mention unfixed bugs and why they were not fixed. This section should include shortcomings of the frameworks or technologies used. Although time can be a significant variable to consider, paucity of time and difficulty understanding implementation are not valid reasons to leave bugs unfixed.
* Did you recognise gaps in your knowledge, and how did you address them?
* If applicable, include evidence of feedback received (from peers or instructors) and how it improved your approach or understanding.

## Development Roadmap
* What challenges did you face, and what strategies were used to overcome these challenges?
* What new skills or tools do you plan to learn next based on your project experience? 

## Deployment
### Heroku

* The App live link is: https://YOUR_APP_NAME.herokuapp.com/ 
* Set the runtime.txt Python version to a [Heroku-20](https://devcenter.heroku.com/articles/python-support#supported-runtimes) stack currently supported version.
* The project was deployed to Heroku using the following steps.

1. Log in to Heroku and create an App
2. From the Deploy tab, select GitHub as the deployment method.
3. Select your repository name and click Search. Once it is found, click Connect.
4. Select the branch you want to deploy, then click Deploy Branch.
5. The deployment process should happen smoothly if all deployment files are fully functional. Click now the button Open App on the top of the page to access your App.
6. If the slug size is too large then add large files not required for the app to the .slugignore file.


## Main Data Analysis Libraries
* Here you should list the libraries you used in the project and provide an example(s) of how you used these libraries.


## Credits 

* In this section, you need to reference where you got your content, media and extra help from. It is common practice to use code from other repositories and tutorials, however, it is important to be very specific about these sources to avoid plagiarism. 
* You can break the credits section up into Content and Media, depending on what you have included in your project. 

### Content 

- The text for the Home page was taken from Wikipedia Article A
- Instructions on how to implement form validation on the Sign-Up page was taken from [Specific YouTube Tutorial](https://www.youtube.com/)
- The icons in the footer were taken from [Font Awesome](https://fontawesome.com/)

### Media

- The photos used on the home and sign-up page are from This Open-Source site
- The images used for the gallery page were taken from this other open-source site



## Acknowledgements (optional)
* Thank the people who provided support through this project.