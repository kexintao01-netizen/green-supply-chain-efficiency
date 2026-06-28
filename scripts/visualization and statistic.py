import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind


# =========================
# 1. Load DEA results
# =========================

df = pd.read_excel(
    "dea_results_by_industry.xlsx"
)

df.columns = df.columns.str.strip()


# =========================
# 2. Descriptive statistics
# =========================

summary_stats = (
    df.groupby(["Industry Group", "Year"])["Efficiency"]
    .agg(["mean", "std", "min", "max", "median"])
    .reset_index()
)

summary_stats.columns = [
    "Industry",
    "Year",
    "Mean",
    "Standard Deviation",
    "Minimum",
    "Maximum",
    "Median"
]

print("\nSummary Statistics:")
print(summary_stats)


# =========================
# 3. Welch's t-test
# =========================

group_food = df[df["Industry Group"] == "Food"]["Efficiency"]
group_manufacturing = df[df["Industry Group"] == "Manufacturing"]["Efficiency"]

t_stat, p_val = ttest_ind(
    group_food,
    group_manufacturing,
    equal_var=False
)

print("\nWelch's t-test:")
print(f"T statistic: {t_stat:.4f}")
print(f"P-value: {p_val:.4f}")

if p_val < 0.05:
    print(
        "Significant difference: DEA efficiency differs significantly between the manufacturing and food industries."
    )
else:
    print(
        "No significant difference: DEA efficiency does not differ significantly between the manufacturing and food industries."
    )


# =========================
# 4. Visualization settings
# =========================

sns.set_theme(style="whitegrid", context="talk")


# =========================
# 5. Figure 1: Overall distribution
# =========================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="Industry Group",
    y="Efficiency",
    width=0.45,
    showfliers=False
)

sns.stripplot(
    data=df,
    x="Industry Group",
    y="Efficiency",
    jitter=0.22,
    alpha=0.45,
    size=4
)

plt.title("Distribution of DEA Efficiency Scores by Industry")
plt.xlabel("")
plt.ylabel("DEA Efficiency Score")
plt.ylim(0, 1.05)
plt.tight_layout()
plt.show()


# =========================
# 6. Figure 2: Distribution by year
# =========================

plt.figure(figsize=(12, 6))

sns.boxplot(
    data=df,
    x="Year",
    y="Efficiency",
    hue="Industry Group",
    width=0.6,
    showfliers=False
)

plt.title("DEA Efficiency Distribution by Industry and Year")
plt.xlabel("Year")
plt.ylabel("DEA Efficiency Score")
plt.ylim(0, 1.05)
plt.legend(title="Industry")
plt.tight_layout()
plt.show()


# =========================
# 7. Figure 3: Mean efficiency trend
# =========================

trend_df = (
    df.groupby(["Year", "Industry Group"])["Efficiency"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(9, 5))

sns.lineplot(
    data=trend_df,
    x="Year",
    y="Efficiency",
    hue="Industry Group",
    marker="o",
    linewidth=2.5
)

plt.title("Average DEA Efficiency Trend by Industry")
plt.xlabel("Year")
plt.ylabel("Average DEA Efficiency")
plt.xticks(sorted(df["Year"].dropna().unique()))
plt.ylim(0.45, 0.7)
plt.legend(title="Industry")
plt.tight_layout()
plt.show()


# =========================
# 8. Figure 4: Heatmap
# =========================

heatmap_df = trend_df.pivot(
    index="Industry Group",
    columns="Year",
    values="Efficiency"
)

plt.figure(figsize=(8, 3.8))

sns.heatmap(
    heatmap_df,
    annot=True,
    fmt=".3f",
    linewidths=0.5,
    cbar_kws={"label": "Mean DEA Efficiency"}
)

plt.title("Mean DEA Efficiency Heatmap")
plt.xlabel("Year")
plt.ylabel("")
plt.tight_layout()
plt.show()


# =========================
# 9. Figure 5: Representative enterprise comparison
# =========================

case_data = {
    "Enterprise": ["Moutai", "Bright Dairy"],
    "Carbon Emissions": [2357623 / 10000, 4558355 / 10000],
    "Operating Cost": [100896.3 / 10000, 220578.0 / 10000],
    "Total Assets": [254364.8 / 10000, 242273.2 / 10000],
    "Net Profit": [772541.6 / 10000, 83056.51 / 10000],
    "E Score": [4.35, 2.42],
    "ISO 14001 Certification": [0, 1]
}

case_df = pd.DataFrame(case_data)

case_long = case_df.melt(
    id_vars="Enterprise",
    var_name="Indicator",
    value_name="Value"
)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=case_long,
    x="Indicator",
    y="Value",
    hue="Enterprise"
)

plt.title("Comparison of Input and Output Indicators: Moutai vs. Bright Dairy")
plt.xlabel("")
plt.ylabel("Scaled Value")
plt.xticks(rotation=35, ha="right")
plt.legend(title="Enterprise")
plt.tight_layout()
plt.show()