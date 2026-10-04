# Methodology

Context: TimesFM3 is a zero-shot forecasting model. It requires only the historical input series; no task-specific training, fine-tuning, or manual parameter estimation is performed. Once the input series is provided, the model generates the forecast automatically.

1. The dataset is restricted to observations from 2013 onwards to reflect the change in ownership, which represents a structural break. Data points affected by Covid 19 are also excluded as they not representative of the general trend - including them will distort the trend. The retained observations—for example, 2013–2019 and 2024–2025—are then concatenated into a single historical series for input to the model.
2. The prepared historical aircraft movement series is supplied as input to TimesFM3. The model returns the aircraft movement forecast automatically.

# Assumptions

1. The model's zero-shot capabilities generalise sufficiently to aircraft movement frequency without additional training or calibration.
2. Non-contiguous retained periods can be treated as a single contiguous input series.
3. Excluded years do not contain essential temporal information and that concatenation does not introduce material bias or inaccuracy.
3. The post-2013 ownership regime is assumed to be sufficiently stable for forecasting, and no further major structural breaks occur over the forecast horizon.
4. No major exogenous shocks—such as pandemics, wars, regulatory changes, fuel crises, or significant capacity constraints—that would materially alter aircraft movement trends.

# Results

1. Forecast Aircraft Movement: 217,627 in 2035, 287,658 in 2045.
As it is zero-shot model, it does not provide additional inferential statistics, such as confidence intervals, p-values, or feature importances. The results should therefore be interpreted as point forecasts.

# Growth Assessment

Growth is determined to be reasonable and plausible:
1. Stansted is looking increase its passenger limit up to 51 million, from 29.7 million in 2025. Even though it plans to rely on larger aircraft rather than more flights, this still supports moderate growth in aircraft movements, consistent with the forecast.
2. The growth is not exponential. The forecast implies a CAGR of approximately 2.8% for aircraft movements between 2035 and 2045, below Stansted’s post-2013 historical growth of approximately 5.3%. This is consistent with maturing, capacity-constrained growth.

# Limitations
1. Lack of interpretability, i.e., a black box; non-reproducible without pinned weights/seed; version-sensitive.
2. TimesFM3 is not aviation-specific and may not capture sector-specific dynamics as effectively as a domain-calibrated model.
3. Excluding COVID-19 years and concatenating non-contiguous periods may distort temporal dependencies and reduce the model’s ability to capture long-term dynamics.