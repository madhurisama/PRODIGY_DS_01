import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


csv_file = "API_SP.POP.TOTL_DS2_en_csv_v2_127039.csv"
df = pd.read_csv(csv_file, skiprows=4)


year_cols = [col for col in df.columns if col.isdigit()]
latest_year = None
for year in reversed(year_cols):
    if df[year].notna().sum() > 100:   
        latest_year = year
        break

print(f"Using year: {latest_year}")



top15 = (
    df[["Country Name", latest_year]]
    .dropna()
    .sort_values(latest_year, ascending=False)
    .head(15)
)
top15.columns = ["Country", "Population"]
top15["Population_Billions"] = top15["Population"] / 1e9


all_pops = df[["Country Name", latest_year]].dropna()
all_pops = all_pops.rename(columns={latest_year: "Population"})
all_pops["Population_Millions"] = all_pops["Population"] / 1e6

print(f"Total countries loaded: {len(all_pops)}")


plt.figure(figsize=(14, 7))
colors = sns.color_palette("viridis", 15)

bars = plt.bar(
    top15["Country"],
    top15["Population_Billions"],
    color=colors,
    edgecolor="white",
    linewidth=0.8
)

for bar, val in zip(bars, top15["Population_Billions"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        f"{val:.2f}B",
        ha="center", va="bottom", fontsize=9, fontweight="bold"
    )

plt.title(f"Top 15 Most Populous Countries ({latest_year})",
          fontsize=16, fontweight="bold", pad=15)
plt.xlabel("Country", fontsize=12)
plt.ylabel("Population (Billions)", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.tight_layout()
plt.savefig("bar_chart.png", dpi=150)
plt.show()
print("Bar chart saved!")


plt.figure(figsize=(12, 6))

plt.hist(
    all_pops["Population_Millions"],
    bins=40,
    color="#4C72B0",
    edgecolor="white",
    linewidth=0.6
)

median_val = all_pops["Population_Millions"].median()
plt.axvline(
    median_val,
    color="red", linestyle="--", linewidth=1.5,
    label=f"Median: {median_val:.1f}M"
)

plt.title(f"Distribution of Country Populations ({latest_year})",
          fontsize=16, fontweight="bold", pad=15)
plt.xlabel("Population (Millions)", fontsize=12)
plt.ylabel("Number of Countries", fontsize=12)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig("histogram.png", dpi=150)
plt.show()
print("Histogram saved!")