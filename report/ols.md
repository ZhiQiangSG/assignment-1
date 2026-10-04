# Methodology

1. The dataset is restricted to observations from 2013 onwards to reflect the change in ownership, which represents a structural break. Data points affected by Covid 19 are also excluded as they not representative of the general trend - including them will distort the trend and violate key OLS assumptions.
2. Compute the aircraft movement forecast by regressing time against aircraft movements using Ordinary Least Square (OLS) Regression: movement = const + slope*year using the historical dataset (2013-2019, 2024-2025).

# Assumptions

1. Aircraft movements follows a linear trend, increasing by a constant absolute amount each period.
2. Time is the sole explanatory variable; no other economic, operational, regulatory, or environmental factors are assumed to affect aircraft movements.
3. The COVID-19 period (2020-2023) is not representative of the underlying long-term trend and is therefore excluded. This also reduces the risk of OLS results being distorted by outliers.
4. Standard OLS assumptions hold: linearity, independent observations, homoscedasticity, and normally distributed residuals for inference.

# Results

1. movement = -7,490,840 + 3,802.5*year, n=9
2. Forecast Aircraft Movement: 247,273 in 2035, 285,298 in 2045.
3. Regression Statistics: R2=0.605, adj-R2=0.548, F=10.70 p=0.014, AIC 198.9, BIC 199.3, DW=0.538

# Growth Assessment

Growth is determined to be reasonable and plausible:
1. The linear trend implies a constant absolute increase of 3,802.5 aircraft movements per year. This produces a declining percentage growth rate over time, which is realistic for a mature aviation market.
2. The forecast rises from 247,273 movements in 2035 to 285,298 in 2045.
3. These projections are plausible under the stated model assumptions, but they should be interpreted with caution given the modest model fit and evidence of autocorrelation.

# Limitations
1. This model is a time-only extrapolation and excludes other econometric variables that may influence aircraft movements such as GDP.
2. Assumes a constant absolute trend, therefore cannot capture nonlinear growth, seasonality, cyclicality, or structural breaks.
3. The sample is very small, n=9 and df=7, resulting in low statistical power and imprecise estimates.
4. The model fit is modest: R^2=0.61
5. The Durbin–Watson statistic of 0.538 indicates strong positive autocorrelation, violating the independence assumption and potentially biasing standard errors and inference.