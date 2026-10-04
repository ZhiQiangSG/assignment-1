from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import statsmodels.api as sm

df_hist_full = pd.read_excel("raw_data.xlsx", sheet_name="historical")
df_forecast = pd.read_excel("raw_data.xlsx", sheet_name="forecast")

# 1. Prepare historical data: 2013 onwards, excluding Covid years
df_hist = df_hist_full.loc[(df_hist_full["covid"] == 0) & (df_hist_full["year"] >= 2013)].copy()

# 2. Fit OLS linear time trend (levels): movements = intercept + slope * year
X_hist = sm.add_constant(df_hist[["year"]])
model = sm.OLS(df_hist["aircraft_movement"], X_hist).fit()
print(model.summary())

# 3. Forecast movements over the forecast horizon
X_fore = sm.add_constant(df_forecast[["year"]], has_constant="add")
X_fore = X_fore[X_hist.columns]
df_forecast["mov_hat"] = np.asarray(model.predict(X_fore), dtype=float)
df_forecast["mov_hat"] = df_forecast["mov_hat"].clip(lower=0)

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
    {"statistic": "nobs (2013+, covid==0 years)", "value": int(model.nobs)},
    {"statistic": "rsquared", "value": float(model.rsquared)},
    {"statistic": "rsquared_adj", "value": float(model.rsquared_adj)},
    {"statistic": "fvalue", "value": float(model.fvalue)},
    {"statistic": "f_pvalue", "value": float(model.f_pvalue)},
    {"statistic": "aic", "value": float(model.aic)},
    {"statistic": "bic", "value": float(model.bic)},
    {"statistic": "sample", "value": "year>=2013 & covid==0"},
    {"statistic": "method", "value": "OLS linear time trend (levels)"},
    {"statistic": "est_start_year", "value": int(df_hist["year"].min())},
    {"statistic": "est_end_year", "value": int(df_hist["year"].max())},
])

with pd.ExcelWriter(outputs_dir / f"{stem}.xlsx", engine="openpyxl") as writer:
    df_out.to_excel(writer, sheet_name="forecast", index=False)
    df_stats.to_excel(writer, sheet_name="regression_stats", index=False)
    df_fit.to_excel(writer, sheet_name="model_fit", index=False)

plt.show()
