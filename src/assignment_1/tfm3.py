from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from timesfm3.torch.timesfm3_forecaster import TimesFM3Forecaster

df_hist_full = pd.read_excel("raw_data.xlsx", sheet_name="historical")
df_forecast = pd.read_excel("raw_data.xlsx", sheet_name="forecast")

# 1. Prepare historical data: 2013 onwards, excluding covid years (covid == 1)
df_hist = df_hist_full.loc[(df_hist_full["year"] >= 2013) & (df_hist_full["covid"] == 0)].copy()
df_hist["ln_gdp"] = np.log(df_hist["real_gdp"])
df_hist["ln_fuel"] = np.log(df_hist["jet_fuel_price"])

# 2. Build TimesFM3 inputs: target + past-future covariates (log econ + covid dummy)
df_forecast["ln_gdp"] = np.log(df_forecast["real_gdp"])
df_forecast["ln_fuel"] = np.log(df_forecast["jet_fuel_price"])
if "covid" not in df_forecast.columns:
    df_forecast["covid"] = 0

context = df_hist["aircraft_movement"].to_numpy(dtype=np.float32)
hist_cov = df_hist[["ln_gdp", "ln_fuel", "covid"]].to_numpy(dtype=np.float32)
fore_cov = df_forecast[["ln_gdp", "ln_fuel", "covid"]].to_numpy(dtype=np.float32)
past_future_cov = np.concatenate([hist_cov, fore_cov], axis=0).T  # (3, context + horizon)
horizon = len(df_forecast)

# 3. Forecast movements with TimesFM3 (zero-shot foundation model)
forecaster = TimesFM3Forecaster.from_pretrained(
    "google/timesfm-3.0-pytorch", device="cpu"
)
out = forecaster.predict(
    context,
    horizon=horizon,
    past_future_covariates=past_future_cov,
    make_positive=True,
)
df_forecast["mov_hat"] = np.asarray(out.forecast, dtype=float)

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
df_out.to_excel(outputs_dir / f"{stem}.xlsx", index=False)

plt.show()
