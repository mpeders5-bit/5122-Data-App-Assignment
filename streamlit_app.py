import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, due on Oct 6th.")

st.write("### Input Data and Examples")

# Load the Superstore data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)

st.dataframe(df)

# This bar chart will not have solid bars--but lines--because
# the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas
# This results in a chart with solid bars
st.dataframe(df.groupby("Category").sum())

# Using as_index=False here preserves Category as a column
st.bar_chart(
    df.groupby("Category", as_index=False).sum(),
    x="Category",
    y="Sales",
    color="#04f"
)

# ---------------------------------------------------------
# Aggregating by time
# ---------------------------------------------------------

# Ensure Order_Date is in datetime format
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Set Order_Date as the dataframe index
df.set_index("Order_Date", inplace=True)

# Group sales by month
# "ME" means Month End in newer versions of Pandas
sales_by_month = (
    df.filter(items=["Sales"])
    .groupby(pd.Grouper(freq="ME"))
    .sum()
)

st.dataframe(sales_by_month)

# The grouped months are the index and are automatically
# used for the x-axis
st.line_chart(sales_by_month, y="Sales")


# =========================================================
# YOUR ADDITIONS
# =========================================================

st.write("## Your additions")


# ---------------------------------------------------------
# (1) Add a dropdown for Category
# ---------------------------------------------------------

selected_category = st.selectbox(
    "Select a Category",
    df["Category"].unique()
)


# ---------------------------------------------------------
# (2) Add a multiselect for Sub_Category
#     within the selected Category
# ---------------------------------------------------------

subcategory_options = df[
    df["Category"] == selected_category
]["Sub_Category"].unique()

selected_subcategories = st.multiselect(
    "Select Sub-Categories",
    subcategory_options,
    default=subcategory_options
)


# Filter the dataframe using the Category and
# Sub-Categories selected by the user
filtered_df = df[
    (df["Category"] == selected_category)
    & (df["Sub_Category"].isin(selected_subcategories))
]


# ---------------------------------------------------------
# (3) Show a line chart of sales for the selected items
# ---------------------------------------------------------

st.write("### Sales Over Time")

if len(selected_subcategories) > 0:

    sales_by_subcategory = (
        filtered_df
        .groupby(
            [
                pd.Grouper(freq="ME"),
                "Sub_Category"
            ]
        )["Sales"]
        .sum()
        .unstack(fill_value=0)
    )

    st.line_chart(sales_by_subcategory)


    # -----------------------------------------------------
    # (4) Calculate Total Sales, Total Profit,
    #     and Overall Profit Margin
    # -----------------------------------------------------

    total_sales = filtered_df["Sales"].sum()

    total_profit = filtered_df["Profit"].sum()

    if total_sales != 0:
        profit_margin = (
            total_profit / total_sales
        ) * 100
    else:
        profit_margin = 0


    # -----------------------------------------------------
    # (5) Calculate overall profit margin for ALL
    #     products across ALL categories
    # -----------------------------------------------------

    overall_profit_margin = (
        df["Profit"].sum()
        / df["Sales"].sum()
    ) * 100


    # Difference between the selected items'
    # profit margin and the overall profit margin
    margin_difference = (
        profit_margin - overall_profit_margin
    )


    # -----------------------------------------------------
    # Display the three metrics
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

    col2.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

    col3.metric(
        "Overall Profit Margin",
        f"{profit_margin:.2f}%",
        delta=f"{margin_difference:.2f}%"
    )


else:

    st.info(
        "Select at least one Sub-Category to display the results."
    )
