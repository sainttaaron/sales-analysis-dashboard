from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


FINDINGS = [
    "Aggressive Discounting is the Root Cause of Massive Losses",
    "Furniture is the Most Fragile Category (Category-Specific Discount Risk)",
    "High Sales Volume Does Not Equal High Profit ",
    "Severe Seasonality Causes a dip in Profitability in Q1",
    "Revenue is Driven by a Broad Base, Not Just a Few 'Whales'",
]

RECOMMENDATIONS = [
    "Implement a Discounting Policy to Protect Profit Margins",
    "Optimize Pricing Strategies for Different Customer Segments",
    "Audit Loss-Making Regions and Adjust Logistics Pricing"
]

# Page setup
st.set_page_config(page_title="Sales Analysis Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "superstore_clean.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["Order Date", "Ship Date"],
        keep_default_na=False,
    )
    df["Discount Band"] = pd.Categorical(
        df["Discount Band"],
        categories=["None", "Low", "Medium", "High"],
        ordered=True,
    )
    return df


if not DATA_PATH.exists():
    st.error(f"Data file not found: {DATA_PATH}")
    st.stop()

df = load_data()

# ------------------------------------------------------------------
# Title
# ------------------------------------------------------------------
st.title("Sales Analysis Dashboard")
st.caption(
    "Superstore is a fictional sample dataset. "
    f"Orders from {df['Order Date'].min():%b %Y} to {df['Order Date'].max():%b %Y}."
)

# ------------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------------
st.sidebar.header("Filters")

years = sorted(df["Order Year"].unique().tolist())
regions = sorted(df["Region"].unique().tolist())
categories = sorted(df["Category"].unique().tolist())
segments = sorted(df["Segment"].unique().tolist())

selected_years = st.sidebar.multiselect("Year", years, default=years)
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)

filtered = df[
    df["Order Year"].isin(selected_years)
    & df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & df["Segment"].isin(selected_segments)
]

if filtered.empty:
    st.warning("No data for these filters. Select at least one option in each filter.")
    st.stop()

# ------------------------------------------------------------------
# KPIs
# ------------------------------------------------------------------
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
margin = total_profit / total_sales * 100
orders = filtered["Order ID"].nunique()
customers = filtered["Customer ID"].nunique()
avg_order_value = filtered.groupby("Order ID")["Sales"].sum().mean()

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Sales", f"${total_sales:,.0f}")
k2.metric("Total Profit", f"${total_profit:,.0f}")
k3.metric("Profit Margin", f"{margin:.1f}%")
k4.metric("Orders", f"{orders:,}")
k5.metric("Customers", f"{customers:,}")
k6.metric("Avg Order Value", f"${avg_order_value:,.0f}")

# ------------------------------------------------------------------
# Trend over time
# ------------------------------------------------------------------
st.subheader("Sales and profit over time")

month = filtered["Order Date"].dt.to_period("M").dt.to_timestamp()
monthly = filtered.groupby(month)[["Sales", "Profit"]].sum().reset_index()

fig_trend = px.line(
    monthly,
    x="Order Date",
    y=["Sales", "Profit"],
    title="Monthly sales and profit (US dollars)",
    labels={"Order Date": "Month", "value": "US dollars", "variable": ""},
)

st.plotly_chart(fig_trend)

seasonal = filtered.groupby("Order Month")["Sales"].sum().reset_index()
seasonal["Month"] = pd.to_datetime(seasonal["Order Month"], format="%m").dt.strftime("%b")

fig_seasonal = px.bar(
    seasonal,
    x="Month",
    y="Sales",
    title="Total sales by month, all years (US dollars)",
)
st.plotly_chart(fig_seasonal)



# ------------------------------------------------------------------
# Sub-category and region
# ------------------------------------------------------------------
st.subheader("Where is the money made and lost?")
left, right = st.columns(2)

sub = filtered.groupby("Sub-Category")["Profit"].sum().reset_index()
sub["Result"] = sub["Profit"].apply(lambda x: "Loss" if x < 0 else "Profit")

fig_sub = px.bar(
    sub,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    color="Result",
    color_discrete_map={"Loss": "#d62728", "Profit": "#2ca02c"},
    title="Total profit by sub-category (US dollars)",
)
fig_sub.update_layout(yaxis={"categoryorder": "total ascending"})
left.plotly_chart(fig_sub)

region = filtered.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
region["Margin"] = region["Profit"] / region["Sales"] * 100
region["Label"] = region["Margin"].round(1).astype(str) + "% margin"

fig_region = px.bar(
    region,
    x="Region",
    y="Profit",
    text="Label",
    title="Total profit by region (US dollars)",
)
right.plotly_chart(fig_region)

# ------------------------------------------------------------------
# Discounts
# ------------------------------------------------------------------
st.subheader("Discounts and profit")

discount = filtered.groupby("Discount Band", observed=True).agg(
    avg_profit=("Profit", "mean"),
    loss_share=("Is Loss", "mean"),
).reset_index()
discount["loss_share"] = discount["loss_share"] * 100

d1, d2 = st.columns(2)

fig_avg = px.bar(
    discount,
    x="Discount Band",
    y="avg_profit",
    title="Average profit per order line (US dollars)",
    labels={"avg_profit": "Average profit"},
)
d1.plotly_chart(fig_avg)

fig_loss = px.bar(
    discount,
    x="Discount Band",
    y="loss_share",
    title="Share of order lines that lost money (%)",
    labels={"loss_share": "Loss-making lines (%)"},
)
d2.plotly_chart(fig_loss)

st.caption(
    "Bands: None = 0%, Low = up to 20%, Medium = 20-40%, High = above 40%. "
    "This shows an association between discounts and losses. "
    "It does not prove that discounts alone cause them."
)

# ------------------------------------------------------------------
# Products
# ------------------------------------------------------------------
st.subheader("Best-selling products that lose money")

product = filtered.groupby("Product Name")[["Sales", "Profit"]].sum()
losers = product[product["Profit"] < 0].nlargest(10, "Sales").round(2)

if losers.empty:
    st.info("No loss-making products for these filters.")
else:
    st.dataframe(losers)

# ------------------------------------------------------------------
# Findings
# ------------------------------------------------------------------
st.subheader("Key findings")
st.caption("These come from the full dataset and do not change with the filters.")
for finding in FINDINGS:
    st.markdown("- " + finding)

st.subheader("Recommendations")
for recommendation in RECOMMENDATIONS:
    st.markdown("- " + recommendation)
