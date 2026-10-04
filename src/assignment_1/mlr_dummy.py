from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import statsmodels.api as sm

df_hist_full = pd.read_excel("raw_data.xlsx", sheet_name="historical")
df_forecast = pd.read_excel("raw_data.xlsx", sheet_name="forecast")

# 1. Prepare historical data (keep all years; covid distortion modelled via dummy)
# NOTE: ln_pax excluded vs mlr_dummy.py -> unconditional on pax (only gdp + fuel + covid).
df_hist = df_hist_full.copy()
df_hist["ln_mov"] = np.log(df_hist["aircraft_movement"])
df_hist["ln_gdp"] = np.log(df_hist["real_gdp"])
df_hist["ln_fuel"] = np.log(df_hist["jet_fuel_price"])

# 2. Estimate multi-linear regression (log-log OLS) on full sample (all Covid points included)
X_hist = sm.add_constant(df_hist[["ln_gdp", "ln_fuel", "covid"]])
model = sm.OLS(df_hist["ln_mov"], X_hist).fit()

# 3. Forecast movements: predict ln(mov), then exponentiate
# Forecast covid = 0 (ensure column exists; raw forecast sheet already has covid = 0).
df_forecast["ln_gdp"] = np.log(df_forecast["real_gdp"])
df_forecast["ln_fuel"] = np.log(df_forecast["jet_fuel_price"])
if "covid" not in df_forecast.columns:
    df_forecast["covid"] = 0
X_fore = sm.add_constant(df_forecast[["ln_gdp", "ln_fuel", "covid"]], has_constant="add")
# Ensure column order matches estimation (add_constant may reorder if already constant)
X_fore = X_fore[X_hist.columns]
df_forecast["mov_hat"] = np.exp(model.predict(X_fore).to_numpy(dtype=float))

# 4. Plot and export
outputs_dir = Path(__file__).resolve().parents[2] / "outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)
stem = Path(__file__).stem

plt.figure(figsize=(10, 6))
plt.plot(df_hist_full["year"], df_hist_full["aircraft_movement"], label="Historical")
plt.plot(df_forecast["year"], df_forecast["mov_hat"], label="Forecast", zorder=5)
plt.xlabel("Year")
plt.ylabel("Aircraft Movements")
ax = plt.gca()
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
plt.legend(loc="lower right")
plt.subplots_adjust(left=0.14, right=0.96, top=0.92, bottom=0.14)
plt.savefig(outputs_dir / f"{stem}.png", dpi=300)

df_out = pd.DataFrame({
    "year": df_forecast["year"],
    "movements": df_forecast["mov_hat"]
})

# Regression statistics sheet (coefficients + model fit)
conf = model.conf_int(alpha=0.05)
df_stats = pd.DataFrame({
    "coef": model.params,
    "std_err": model.bse,
    "t": model.tvalues,
    "p_value": model.pvalues,
    "ci_lower_95": conf[0],
    "ci_upper_95": conf[1],
}).reset_index().rename(columns={"index": "variable"})
df_fit = pd.DataFrame([
    {"statistic": "nobs (full sample, incl. covid)", "value": int(model.nobs)},
    {"statistic": "rsquared", "value": float(model.rsquared)},
    {"statistic": "rsquared_adj", "value": float(model.rsquared_adj)},
    {"statistic": "fvalue", "value": float(model.fvalue)},
    {"statistic": "f_pvalue", "value": float(model.f_pvalue)},
    {"statistic": "aic", "value": float(model.aic)},
    {"statistic": "bic", "value": float(model.bic)},
])

with pd.ExcelWriter(outputs_dir / f"{stem}.xlsx", engine="openpyxl") as writer:
    df_out.to_excel(writer, sheet_name="forecast", index=False)
    df_stats.to_excel(writer, sheet_name="regression_stats", index=False)
    df_fit.to_excel(writer, sheet_name="model_fit", index=False)

print(model.summary())

plt.show()
