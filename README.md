# Sales Analysis Dashboard

An interactive Streamlit dashboard that shows where a retail store makes and loses money, with a focus on how discounts relate to profit.

**Live demo:** [https://sainttaaron-sales-analysis-dashboard-appapp-lkbi0l.streamlit.app/]

![Dashboard overview](images/dashboard.png)

---

## Key Findings



1. [Finding 1, Aggressive Discounting is the Root Cause of Massive Losses.]
2. [Finding 2, "Furniture" is the Most Fragile Category (Category-Specific Discount Risk).]
3. [Finding 3, Severe Seasonality Causes a dip in Profitability in Q1 .]
4. [Finding 4,  Revenue is Driven by a Broad Base, Not Just a Few "Whales".]


## Recommendations

1. [ review discounts on Furniture, where most losses come from heavy discounting.]
2. [implement a Hard Cap on Discounts.]
3.  **Investigate the loss-making states before changing prices.**
   Six states (Texas, Ohio, Pennsylvania, Illinois, North Carolina and Colorado) generated about $533K in sales but lost about $85K, a combined margin of -15.9%. Texas alone lost about $25.7K on $170K in sales. Check whether heavy discounting or a weak product mix explains the losses, then adjust accordingly.

The discount result is an association in the data. It does not prove that discounts alone cause the losses.

---

## Dataset

This project uses the **Superstore Sales** dataset by Ishan Shrivastava. It is a fictional sample dataset, not data from a real company.

- **Source:** https://www.kaggle.com/datasets/ishanshrivastava28/superstore-sales
- **License:** Database Contents License (DbCL) v1.0 — https://opendatacommons.org/licenses/dbcl/1-0/
- **Size:** 9,994 order lines (5,009 unique orders) and 21 columns
- **Period:** orders from January 2011 to December 2014

### Data in this repository

The cleaned dataset (`data/processed/superstore_clean.csv`) is included so the dashboard can run. The original file is not included. To start from the raw data, download it from the Kaggle link above and place `Superstore.csv` in `data/raw/`.

---

## How I Built It

The project follows the full data workflow: **Data Collection → Cleaning → Exploratory Analysis → Visualization → Dashboard**

| Step | Notebook / file | What it does |
|---|---|---|
| 1. Inspect | `notebooks/01_inspect_data.ipynb` | Looks at the raw data and records what is unusual |
| 2. Clean | `notebooks/02_cleaning.ipynb` | Validates the data, fixes types, adds helper columns, saves the cleaned file |
| 3. Analyse | `notebooks/03_analysis.ipynb` | Answers the business questions with tables and charts |
| 4. Dashboard | `app/app.py` | Interactive Streamlit app with filters, KPIs and charts |

### Data quality notes

- No missing values and no duplicate rows were found.
- Dates were stored as text and were converted to real dates.
- 1,871 order lines have negative profit. They were kept, because they are real losses and part of the analysis.
- Discounts reach up to 80%. This is within a valid range, so it was investigated and not removed.
- A row is one order line, not one order, so order-level numbers are calculated by grouping on Order ID first.
- Profit margin for any group is total profit divided by total sales.

---

## Run It Locally

```bash
git clone [YOUR REPO URL]
cd [YOUR REPO FOLDER]
python -m venv .venv
```

Activate the environment:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Mac / Linux
source .venv/bin/activate
```

Install the packages and start the app:

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

The app opens at `http://localhost:8501`.

To rebuild the cleaned data from the raw file, place `Superstore.csv` in `data/raw/` and run the notebooks in order (01, 02, 03).

---

## Project Structure

```
sales-analysis-dashboard/
├── app/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
│       └── superstore_clean.csv
├── images/
├── notebooks/
│   ├── 01_inspect_data.ipynb
│   ├── 02_cleaning.ipynb
│   └── 03_analysis.ipynb
├── README.md
└── requirements.txt
```

---

## Limitations and Next Steps

- The data is fictional, so the findings show the method and not real business results.
- The analysis is descriptive. It shows patterns and associations, not causes.
- Possible next steps: customer segmentation (RFM), a profit map by state, and sales forecasting.

---

## What I Practised

- Data cleaning and validation with Pandas
- Exploratory data analysis and business-focused questions
- Interactive dashboards with Streamlit and Plotly
- Version control with Git and GitHub

---

## Author

**Aaron  Kwadwo Adom Osei**
Computer Science and Engineering Student
Aspiring AI Engineer and Data Analytics Learner