import pandas as pd
import re

file_path = "raw data.xlsx"

excel_file = pd.ExcelFile(file_path)
df2 = excel_file.parse('Wind')

report_years = ['2020', '2021', '2022', '2023']

indicator_keywords = [
    'Operating Revenue',
    'Operating Cost',
    'Net Profit',
    'Total Assets',
    'Fixed Assets',
    'Number of Employees'
]

records = []

for i, company in enumerate(df2['Company Name']):
    for col in df2.columns:
        year_match = next((y for y in report_years if y in str(col)), None)
        if not year_match:
            continue

        indicator = next((key for key in indicator_keywords if key in str(col)), None)
        if not indicator:
            continue

        value = df2.loc[i, col]
        if pd.isna(value):
            continue

        if indicator in ['Operating Revenue', 'Operating Cost']:
            value = value / 1e8

        records.append({
            "Company": company,
            "Year": int(year_match),
            "Indicator": indicator,
            "Value": value
        })

df_report = pd.DataFrame(records)

pivot_df = (
    df_report
    .pivot_table(
        index=["Company", "Year"],
        columns="Indicator",
        values="Value",
        aggfunc="first"
    )
    .reset_index()
)

static_cols = [
    col for col in df2.columns
    if not any(year in str(col) for year in report_years)
]

static_df = df2[static_cols].copy()
static_df.rename(columns={'Company Name': 'Company'}, inplace=True)

final_df = pivot_df.merge(static_df, on="Company", how="left")

output_path = "C:/Users/matth/Desktop/新建文件夹/company_year_full_data.xlsx"

final_df.to_excel(output_path, index=False)

print("File saved to:", output_path)