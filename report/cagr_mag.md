# Methodology

1.  The dataset is restricted to observations from 2013 onwards to reflect the change in ownership, which represents a structural break. There are multiple reasons why I think it represents a structural break: 
- Aircraft movements have falling for five successive years after the 2007 peak until MAG became the owner in 2013.
- There is a significant shift in commercial strategy, airline relationships, movement trajectory from 2013 onwards.
2. A compound annual growth rate (CAGR) was calculated using two aircraft movement data points, 2013 and 2025, and this rate was applied to forecast future aircraft movements.

# Assumptions

1. 2013-2025 growth rate persists through 2045.
2. Time is the sole explanatory variable; no other economic, operational, regulatory, or environmental factors are assumed to affect aircraft movements.

# Results

1. CAGR 2013-2025: 2.4168%
2. Forecast Aircraft Movement: 247,446 in 2035, 314,190 in 2045.

# Growth Assessment

Growth is determined to be neither reasonable and plausible because using CAGR produces exponential growth — that is, aircraft movements increasing by 2.4168% every year without limit. This is highly unlikely for a maturing airport such as Stansted. Perpetual exponential growth is therefore unrealistic.
Hence, the 2035 and 2045 forecasts should be treated as upper-bound projections rather than baseline forecasts. 

# Limitations
1. This model is a time-only extrapolation and excludes other econometric variables that may influence aircraft movements such as GDP.
2. The technique does not account for intermediate cycles or events, including COVID-19.
3. The CAGR is based on only two endpoints, 2013 and 2025, making it sensitive to the choice of base and end years.
4. The forecast assumes that the post-2013 growth regime remains stable and does not model capacity constraints, changes in airline strategy, or regulatory shifts.
