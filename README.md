# DEA Green Supply Chain Efficiency Analysis

## Project Overview

This project evaluates the green supply chain efficiency of Chinese listed companies in the manufacturing and food industries using the Data Envelopment Analysis (DEA-CCR) model.

The study compares efficiency performance across industries and over time (2021–2023), aiming to identify industry heterogeneity in green supply chain cost-effectiveness. The analysis combines financial, environmental, and ESG-related indicators to evaluate enterprise efficiency under a multi-input, multi-output framework.

---

## Objectives

* Compare the green supply chain efficiency of manufacturing and food industries.
* Evaluate enterprise efficiency using the DEA-CCR model.
* Examine industry heterogeneity from 2021 to 2023.
* Conduct statistical tests to determine whether efficiency differences are significant.
* Visualize efficiency distributions and industry trends.

---

## Dataset

The dataset is constructed using financial and environmental information collected from Chinese listed companies.

### Input Variables

* Operating Cost
* Total Assets
* Total Carbon Emissions

### Output Variables

* Net Profit
* Environmental (E) Score
* ISO 14001 Certification

Data preprocessing includes:

* Missing value removal
* Filtering invalid observations
* Min-Max normalization
* Industry classification

---

## Methodology

The project follows the workflow below:

```
Raw Data
    ↓
Data Cleaning & Preprocessing
    ↓
DEA Dataset Construction
    ↓
DEA-CCR Efficiency Analysis
    ↓
Industry Comparison
    ↓
Welch's t-test
    ↓
Visualization & Statistical Analysis
```

The DEA model is implemented using linear programming with the PuLP library.

---

## Repository Structure

```
DEA_Green_Supply_Chain_Efficiency/

│── data/
│   ├── raw_data.xlsx
│   ├── company_year_full_data.xlsx
│   ├── dea_analysis_dataset.xlsx
│   └── dea_results_by_industry.xlsx
│
│── scripts/
│   ├── 01_data_preprocessing.py
│   ├── 02_dea_analysis.py
│   └── 03_visualization_and_statistics.py
│
│── figures/
│   ├── efficiency_distribution.png
│   ├── efficiency_distribution_by_year.png
│   ├── efficiency_trend.png
│   ├── efficiency_heatmap.png
│   └──Representative enterprise comparison
│
├── README.md
└── requirements.txt
```

---

## Key Results

* Manufacturing firms achieved higher average DEA efficiency than food industry firms.
* Welch's t-test indicated a statistically significant difference between the two industries (p = 0.0464).
* Manufacturing efficiency increased between 2021 and 2022 before declining in 2023.
* The food industry exhibited a relatively stable but slightly downward efficiency trend during the study period.
* Firms with stronger environmental performance generally demonstrated higher DEA efficiency.

---

## Visualizations

The project includes:

* Distribution of DEA efficiency scores by industry
* Industry comparison using boxplots
* Annual efficiency trend analysis
* Heatmap of average DEA efficiency
* Representative enterprise comparison

---

## Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* PuLP
* SciPy
* Matplotlib
* Seaborn

---

## Future Improvements

Potential future work includes:

* Applying the BCC DEA model to evaluate pure technical efficiency.
* Calculating the Malmquist Productivity Index for dynamic efficiency analysis.
* Incorporating additional ESG indicators and carbon intensity metrics.
* Expanding the analysis to more manufacturing subsectors.

---

