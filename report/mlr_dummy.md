# Methodology

1. The full historical dataset is retained (2005-2025, n=21). COVID-19 distortion is modelled explicitly via a dummy rather than by exclusion: covid = 1 for 2020-2023, 0 otherwise.
2. Compute the aircraft movement forecast by regressing log aircraft movements on log real GDP, log jet fuel price and the COVID dummy using Ordinary Least Square (OLS) Regression in log-log form: ln(movement) = const + b1*ln(gdp) + b2*ln(fuel) + b3*covid using the full historical dataset. Coefficients on ln(gdp) and ln(fuel) are elasticities; the covid coefficient is a proportional level shift during COVID years.
3. Forecast aircraft movements by setting covid = 0 over the forecast horizon (2026-2045), predicting ln(movement) from forecast real_gdp and jet_fuel_price, then exponentiating: mov_hat = exp(ln(mov)_hat).

# Assumptions

1. Aircraft movements follow a constant-elasticity function of real GDP and real jet fuel price, with COVID-19 acting as a pure intercept shift rather than changing slopes.
2. Real GDP and jet fuel price are exogenous; no other economic, operational, regulatory, or environmental factors are assumed to affect aircraft movements. Terminal passengers are deliberately excluded to give an unconditional forecast.
3. Standard OLS assumptions hold: linearity in logs, independent observations, homoscedasticity, and normally distributed residuals for inference.

# Results

1. ln(movement) = -24.4577 + 1.2815*ln(gdp) + 0.1545*ln(fuel) - 0.4440*covid, n=21. The COVID effect is exp(-0.4440)-1 = -35.9%, i.e. movements ~36% below the GDP/fuel-implied level when covid = 1.
2. Forecast Aircraft Movement: 264,725 in 2035, 351,081 in 2045.
3. Regression Statistics: R2=0.558, adj-R2=0.480, F=7.16 p=0.003, AIC -10.85, BIC -6.67, DW=0.802. covid is highly significant (p=0.0005), ln_gdp is significant (p=0.024), ln_fuel is not significant (p=0.249) and const is not significant (p=0.115).

# Growth Assessment

Growth is determined to be aggressive and not fully reasonable as a constrained forecast:
1. The GDP elasticity of 1.28 implies movements grow faster than GDP in proportional terms, while the fuel elasticity of +0.15 is small, positive, and statistically insignificant. Forecast growth is therefore driven almost entirely by assumed GDP growth, implying a CAGR of ~2.8% p.a. from 2026-2045 (2.9% p.a. from 2035-2045).
2. The forecast rises from 208,101 movements in 2026 to 264,725 in 2035 and 351,081 in 2045.
3. These projections are implausible as operational movements: 351,081 in 2045 exceeds the assumed runway capacity of 264,000 by ~33%, and the implied PATM falls from ~155 in 2035 to ~144 in 2045, reversing the historical rise in passengers per movement (113.7 in 2005 to 152.7 in 2025). They are best interpreted as an unconditional upper-bound demand indicator under the stated GDP/fuel assumptions, not a capacity-constrained forecast.

# Limitations
1. This model conditions only on GDP, fuel price, and a COVID intercept, and excludes other variables that may influence aircraft movements such as terminal passengers, fares, or supply constraints.
2. Assumes constant elasticities and a COVID effect confined to a level shift in 2020-2023, therefore cannot capture nonlinear responses, changing fuel sensitivity, or lingering post-COVID structural change.
3. The sample is small, n=21 with 4 estimated parameters and df=17, resulting in low statistical power and imprecise estimates (notably the wide CI on const and ln_gdp).
4. The model fit is modest: R^2=0.56, adj-R^2=0.48. ln_fuel is insignificant and positive, contrary to the expected negative price effect, suggesting omitted-variable or collinearity issues.
5. The Durbin–Watson statistic of 0.802 indicates positive autocorrelation, violating the independence assumption and potentially biasing standard errors and inference. Forecasts exponentiate fitted log values without smearing correction, introducing retransformation bias, and are fully conditional on external GDP/fuel forecasts.
