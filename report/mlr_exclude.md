# Methodology

1. The dataset is restricted to non-Covid observations (covid == 0), giving an estimation sample of 2005-2019 and 2024-2025 (n=17). Data points affected by Covid 19 (2020-2023) are excluded as they are not representative of the general trend - including them will distort the estimates and violate key OLS assumptions.
2. Compute the aircraft movement forecast by regressing log aircraft movements on log real GDP and log jet fuel price using Ordinary Least Square (OLS) Regression in log-log form: ln(movement) = const + b1*ln(gdp) + b2*ln(fuel) using the historical dataset (2005-2019, 2024-2025). Forecasts are obtained by predicting ln(movements) from the forecast GDP and fuel price paths and then exponentiating. The specification is unconditional on passengers (only gdp + fuel).

# Assumptions

1. Aircraft movements follow a log-linear relationship with real GDP and jet fuel price, i.e. constant elasticities: a 1% increase in GDP increases movements by b1%, and a 1% increase in fuel price changes movements by b2%, holding the other factor constant.
2. Real GDP and jet fuel price are exogenous drivers; no other economic, operational, regulatory, or environmental factors are assumed to affect aircraft movements beyond these two variables, and passenger volumes are excluded from the conditioning set.
3. The COVID-19 period (2020-2023) is not representative of the underlying long-term relationship and is therefore excluded. This also reduces the risk of OLS results being distorted by outliers.
4. Standard OLS assumptions hold on the log scale: linearity in logs, independent observations, homoscedasticity, exogenous regressors, and normally distributed residuals for inference. Forecast GDP and fuel price paths are assumed given and measured without error.

# Results

1. ln(movement) = 2.972 + 0.3268*ln(gdp) - 0.1519*ln(fuel), n=17 (GDP p=0.484, fuel p=0.252, const p=0.822; neither slope coefficient is statistically significant at 5%).
2. Forecast Aircraft Movement: 204,867 in 2035, 213,519 in 2045 (from 199,638 in 2026).
3. Regression Statistics: R2=0.242, adj-R2=0.133, F=2.23 p=0.144, AIC -20.5, BIC -18.0, DW=0.360

# Growth Assessment

Growth is determined to be reasonable and plausible:
1. The log-log specification implies constant elasticities (GDP +0.33, fuel -0.15) rather than a constant absolute increment, so forecast growth responds to the assumed GDP and fuel price paths. The low GDP elasticity damps the effect of assumed GDP growth, producing a flat trajectory with a CAGR of only ~0.35% p.a. from 2026-2045 (0.41% p.a. from 2035-2045).
2. The forecast rises from 199,638 movements in 2026 to 204,867 in 2035 and 213,519 in 2045.
3. These projections are plausible under the stated model assumptions as a capacity-consistent, conservative path - 213,519 in 2045 remains well within the assumed runway capacity of 264,000 - but they should be interpreted with caution given the weak model fit, statistically insignificant coefficients, and evidence of autocorrelation. The implied PATM of ~201 in 2035 rising to ~237 in 2045 also assumes continued strong upgauging beyond the extrapolated PATM trend (~193 in 2045).

# Limitations
1. This model conditions only on GDP and fuel price and excludes other econometric variables that may influence aircraft movements such as passenger demand, fares, or capacity decisions.
2. Assumes constant elasticities over the full horizon, therefore cannot capture nonlinear effects, interactions, seasonality, cyclicality, or structural breaks.
3. The sample is small, n=17 and df=14, resulting in low statistical power and imprecise estimates; both slope coefficients are statistically insignificant and the F-test fails to reject at 5% (p=0.144).
4. The model fit is weak: R^2=0.24, adj-R^2=0.13.
5. The Durbin–Watson statistic of 0.360 indicates strong positive autocorrelation, violating the independence assumption and potentially biasing standard errors and inference.
