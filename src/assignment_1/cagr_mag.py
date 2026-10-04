from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

df_hist_full = pd.read_excel("raw_data.xlsx", sheet_name="historical")
df_forecast = pd.read_excel("raw_data.xlsx", sheet_name="forecast")

# 1. Compute CAGR for aircraft movement over 2013-2025
start_year, end_year = 2013, 2025
v_start = df_hist_full.loc[df_hist_full["year"] == start_year, "aircraft_movement"].iloc[0]
v_end = df_hist_full.loc[df_hist_full["year"] == end_year, "aircraft_movement"].iloc[0]
n = end_year - start_year
cagr = (v_end / v_start) ** (1 / n) - 1
print(f"CAGR {start_year}-{end_year}: {cagr * 100:.4f}%")

# 2. Forecast movements: V2025 * (1 + CAGR) ^ t
df_forecast["mov_hat"] = v_end * (1 + cagr) ** (df_forecast["year"] - end_year)

# 3. Plot and export
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
})
df_params = pd.DataFrame([
    {"parameter": "cagr", "value": float(cagr)},
    {"parameter": "mov_start_2013", "value": float(v_start)},
    {"parameter": "mov_end_2025", "value": float(v_end)},
    {"parameter": "n_years", "value": int(n)},
    {"parameter": "mov_base_2025", "value": float(v_end)},
])

with pd.ExcelWriter(outputs_dir / f"{stem}.xlsx", engine="openpyxl") as writer:
    df_out.to_excel(writer, sheet_name="forecast", index=False)
    df_params.to_excel(writer, sheet_name="params", index=False)

plt.show()
