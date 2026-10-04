from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

df_hist_full = pd.read_excel("raw_data.xlsx", sheet_name="historical")
df_forecast = pd.read_excel("raw_data.xlsx", sheet_name="forecast")

# 1. Compute CAGR for passenger growth over 2026-2045 (from forecast sheet)
pax_start_year, pax_end_year = 2026, 2045
pax_start = df_forecast.loc[df_forecast["year"] == pax_start_year, "terminal_passengers"].iloc[0]
pax_end = df_forecast.loc[df_forecast["year"] == pax_end_year, "terminal_passengers"].iloc[0]
n_pax = pax_end_year - pax_start_year
cagr_pax = (pax_end / pax_start) ** (1 / n_pax) - 1
print(f"Passenger CAGR {pax_start_year}-{pax_end_year}: {cagr_pax * 100:.4f}%")

# 2. Forecast movements: Mov2025 * (1 + CAGR_pax) ^ t
mov_base_year = 2025
mov_base = df_hist_full.loc[df_hist_full["year"] == mov_base_year, "aircraft_movement"].iloc[0]
df_forecast["mov_hat"] = mov_base * (1 + cagr_pax) ** (df_forecast["year"] - mov_base_year)

# Implied smooth passenger path (audit only, anchored at 2026 to reproduce endpoints)
df_forecast["pax_hat"] = pax_start * (1 + cagr_pax) ** (df_forecast["year"] - pax_start_year)

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
    "pax_hat": df_forecast["pax_hat"],
})
df_params = pd.DataFrame([
    {"parameter": "cagr_pax", "value": float(cagr_pax)},
    {"parameter": "pax_start_2026", "value": float(pax_start)},
    {"parameter": "pax_end_2045", "value": float(pax_end)},
    {"parameter": "n_years", "value": int(n_pax)},
    {"parameter": "mov_base_2025", "value": float(mov_base)},
])

with pd.ExcelWriter(outputs_dir / f"{stem}.xlsx", engine="openpyxl") as writer:
    df_out.to_excel(writer, sheet_name="forecast", index=False)
    df_params.to_excel(writer, sheet_name="params", index=False)

plt.show()
