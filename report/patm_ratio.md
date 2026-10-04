# Methodology

1. Compute historical Passengers Air Traffic Movement (PATM) across 2005-2025.
PATM = terminal_passengers / aircraft_movement
2. Linearly extrapolate PATM through 2045
Use Ordinary Least Squares (OLS) to fit a simple linear trend: OLS: patm = intercept + slope * year on covid==0 only, i.e. drops 2020-2023, keeps 2005-2019 + 2024-2025, n=17.
Extrapolate patm_hat(y) = intercept + slope*y for 2026-2045
3. Compute the aircraft movement forecast using mov_hat = forecast terminal_passengers / patm_hat.

# Assumptions

1. Linear PATM continues for another 20 years - through increase in load factor or aircraft seat capacity.
2. Terminal passenger forecast is correct.
3. Data points affected by Covid are from 2020-2023 - where aircraft movements in 2024 exceeds the 2019 (pre-covid) level.

# Results

1. PATM = -4007.34 + 2.0538 * year, R2=0.9685, n=17, 2005-2025 ex-COVID.
2. Historical PATM: 113.7 in 2005, 140.7 in 2019, 147.7 in 2024, 152.7 in 2025.
3. Forecast PATM: 153.6 in 2026 -> 192.6 in 2045, +25% in 20y.
4. Forecast Aircraft Movement: 238715 in 2035 -> 262,997 in 2045.
5. Projected growth rate: 1.51% p.a. (CAGR 2025-2045).

# Growth Assessment

Growth is determined to be reasonable and plausible:
1. PATM is 192.6 pax/movement in 2045, which is in line with the increase in seat capacities across major airlines operating in London's Stansted Airport through new plane orders.
2. Projected aircraft movement in 2045 (262997) is quite close to the their internal projection (258060).

# Limitations
1. This model is a time-only extrapolation and excludes other econometric variables that may influence aircraft movements such as GDP.
2. Hinges that passenger forecast is accurate.