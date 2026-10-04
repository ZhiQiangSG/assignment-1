from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

df_hist_full = pd.read_excel("raw_data.xlsx", sheet_name="historical")
df_forecast = pd.read_excel("raw_data.xlsx", sheet_name="forecast")

# 1. Historical PATM, excluding covid-distorted years (covid == 1)
df_hist = df_hist_full[df_hist_full["covid"] == 0].copy()
df_hist["patm"] = df_hist["terminal_passengers"] / df_hist["aircraft_movement"]

# 2. Linear extrapolation of PATM through 2045 (OLS: patm = intercept + slope * year)
slope, intercept = np.polyfit(df_hist["year"].to_numpy(dtype=float), df_hist["patm"].to_numpy(dtype=float), 1)
df_forecast["patm_hat"] = intercept + slope * df_forecast["year"]

# Goodness of fit on estimation sample (audit only)
patm_fitted = intercept + slope * df_hist["year"]
ss_res = float(np.sum((df_hist["patm"] - patm_fitted) ** 2))
ss_tot = float(np.sum((df_hist["patm"] - df_hist["patm"].mean()) ** 2))
r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
print(f"PATM trend (covid==0, n={len(df_hist)}): patm = {intercept:.4f} + {slope:.4f} * year (R2={r_squared:.4f})")

# 3. Forecast movements: forecast terminal passengers / projected PATM
df_forecast["mov_hat"] = df_forecast["terminal_passengers"] / df_forecast["patm_hat"]

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
    "movements": df_forecast["mov_hat"],
    "patm_hat": df_forecast["patm_hat"],
    "terminal_passengers": df_forecast["terminal_passengers"],
})
df_params = pd.DataFrame([
    {"parameter": "slope", "value": float(slope)},
    {"parameter": "intercept", "value": float(intercept)},
    {"parameter": "r_squared", "value": float(r_squared)},
    {"parameter": "n_obs", "value": int(len(df_hist))},
    {"parameter": "sample", "value": "covid==0"},
    {"parameter": "est_start_year", "value": int(df_hist["year"].min())},
    {"parameter": "est_end_year", "value": int(df_hist["year"].max())},
])

with pd.ExcelWriter(outputs_dir / f"{stem}.xlsx", engine="openpyxl") as writer:
    df_out.to_excel(writer, sheet_name="forecast", index=False)
    df_params.to_excel(writer, sheet_name="params", index=False)

plt.show()
