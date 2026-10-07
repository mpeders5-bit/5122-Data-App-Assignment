import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, due on Oct 6th.")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('ME')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
# (1) Dropdown for Category
selected_category = st.selectbox(
    "Select a Category",
    df["Category"].unique()
)

# (2) Multiselect for Sub_Category within the selected Category
subcategory_options = df[
    df["Category"] == selected_category
]["Sub_Category"].unique()

selected_subcategories = st.multiselect(
    "Select Sub-Categories",
    subcategory_options,
    default=subcategory_options
)

# Filter the dataframe based on the user's selections
filtered_df = df[
    (df["Category"] == selected_category) &
    (df["Sub_Category"].isin(selected_subcategories))
]

# (3) Line chart of sales for selected Sub-Categories
st.write("### Sales Over Time")

if len(selected_subcategories) > 0:

    sales_by_subcategory = (
        filtered_df
        .groupby([pd.Grouper(freq="M"), "Sub_Category"])["Sales"]
        .sum()
        .unstack(fill_value=0)
    )

    st.line_chart(sales_by_subcategory)

    # (4) Calculate metrics
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()

    if total_sales != 0:
        profit_margin = (total_profit / total_sales) * 100
    else:
        profit_margin = 0

    # (5) Overall profit margin for all products/categories
    overall_profit_margin = (
        df["Profit"].sum() / df["Sales"].sum()
    ) * 100

    margin_difference = profit_margin - overall_profit_margin

    # Display the three metrics
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
    st.info("Select at least one Sub-Category to display the results.")
