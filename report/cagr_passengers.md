# Methodology

1. Calculate the implied compound annual growth rate (CAGR) of terminal passengers using Manchester Airports Group’s (MAG) 2026–2045 passenger projection: Aircraft movement's CAGR = (PAX2045/PAX2026)^(1/19)-1
2. Apply that growth rate to aircraft movement forecast from 2025-2045.

# Assumptions

1. Passengers Air Traffic Movement (PATM) - PATM = terminal_passengers / aircraft_movement - remains constant. 
2. Aircraft movements grow at same rate as forecast passengers through 2045.

# Results

1. Terminal Passenger CAGR 2026-2045: 2.0895%
2. Forecast Aircraft Movement: 239,651 in 2035, 294,706 in 2045.

# Growth Assessment

Growth is determined to be neither reasonable and plausible because using CAGR produces exponential growth — that is, aircraft movements increasing by 2.0895% every year without limit. This is highly unlikely for a maturing airport such as Stansted. Perpetual exponential growth is therefore unrealistic.
Hence, the 2035 and 2045 forecasts should be treated as upper-bound projections rather than baseline forecasts. 

# Limitations
1. This model is a time-only extrapolation and excludes other econometric variables that may influence aircraft movements such as GDP.
2. This model hinges that passenger forecast is accurate.
3. The technique does not account for intermediate cycles or events, including COVID-19.
4. The CAGR is based on only two endpoints, 2013 and 2025, making it sensitive to the choice of base and end years.
5. The forecast assumes that the post-2013 growth regime remains stable and does not model capacity constraints, changes in airline strategy, or regulatory shifts.
6. Holding PATM constant ignores possible changes in aircraft size, load factors, route mix, and airline operations.