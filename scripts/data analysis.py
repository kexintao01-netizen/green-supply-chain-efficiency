import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pulp

# DEA-CCR function
def dea_ccr(dmu_index, inputs, outputs):
    n_dmu = inputs.shape[0]
    n_inputs = inputs.shape[1]
    n_outputs = outputs.shape[1]

    model = pulp.LpProblem("DEA_CCR", pulp.LpMinimize)
    lambdas = [pulp.LpVariable(f"lambda_{j}", lowBound=0) for j in range(n_dmu)]
    theta = pulp.LpVariable("theta", lowBound=0)

    model += theta

    for i in range(n_inputs):
        model += (
            pulp.lpSum([lambdas[j] * inputs.iloc[j, i] for j in range(n_dmu)])
            <= theta * inputs.iloc[dmu_index, i]
        )

    for r in range(n_outputs):
        model += (
            pulp.lpSum([lambdas[j] * outputs.iloc[j, r] for j in range(n_dmu)])
            >= outputs.iloc[dmu_index, r]
        )

    model.solve()

    return {
        "Company": inputs.index[dmu_index],
        "Efficiency": theta.varValue if model.status == 1 else None,
        "Status": pulp.LpStatus[model.status]
    }


# Dynamic DEA
def dynamic_dea(df_all, input_cols, output_cols, year_col='Year', dmu_col='ID'):
    results = []

    for year, df_year in df_all.groupby(year_col):

        df_year = df_year.set_index(dmu_col)

        inputs = df_year[input_cols]
        outputs = df_year[output_cols]

        industry_info = df_year["Industry"]

        for i in range(len(df_year)):
            res = dea_ccr(i, inputs, outputs)

            res["Year"] = year
            res["Industry"] = industry_info.iloc[i]

            results.append(res)

    return pd.DataFrame(results)


# Load dataset
df_all = pd.read_excel(
    "dea_analysis_dataset.xlsx"
)

df_all.columns = df_all.columns.str.strip()


# Remove missing and invalid observations
df_all = df_all[
    (df_all["Net Profit (10k RMB)"] > 0)
    & (df_all["Total Assets (10k RMB)"] > 0)
]

df_all = df_all.dropna(
    subset=[
        "E Score",
        "Net Profit (10k RMB)",
        "Total Assets (10k RMB)"
    ]
)


# DEA variables
input_cols = [
    "Operating Cost (10k RMB)",
    "Total Assets (10k RMB)",
    "Total Carbon Emissions (t)"
]

output_cols = [
    "Net Profit (10k RMB)",
    "E Score",
    "ISO 14001 Certification"
]


# Min-Max normalization
scaler = MinMaxScaler()

cols_to_normalize = [
    "Operating Cost (10k RMB)",
    "Total Assets (10k RMB)",
    "Total Carbon Emissions (t)",
    "Net Profit (10k RMB)",
    "E Score"
]

df_all[cols_to_normalize] = scaler.fit_transform(
    df_all[cols_to_normalize]
)


# Food industry codes
food_codes = ["C13", "C14", "C15"]

# Manufacturing industry codes
manufacturing_codes = ["C17", "C18", "C19", "C20", "C22", "C24"]


# Filter food industry
df_food = df_all[df_all["Industry"].isin(food_codes)]

# Filter manufacturing industry
df_manufacturing = df_all[
    df_all["Industry"].isin(manufacturing_codes)
]


# Run DEA
result_food = dynamic_dea(
    df_food,
    input_cols,
    output_cols
)

result_food["Industry Group"] = "Food Industry"

result_manufacturing = dynamic_dea(
    df_manufacturing,
    input_cols,
    output_cols
)

result_manufacturing["Industry Group"] = "Manufacturing"


# Merge results
result_all = pd.concat(
    [result_food, result_manufacturing],
    ignore_index=True
)


# Export results
result_all.to_excel(
    "C:/Users/matth/Desktop/新建文件夹/dea_results_by_industry.xlsx",
    index=False
)