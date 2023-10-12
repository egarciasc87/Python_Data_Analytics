import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.colors as colors
pio.templates.default = "plotly_white"


#1. get raw data
file_name = "12_sales_profit_analysis.csv"
data = pd.read_csv(file_name, encoding="latin-1")
#print(data)
#print(data.isnull().sum())
#print(data.describe())

data["Order Date"] = pd.to_datetime(data["Order Date"])
data["Ship Date"] = pd.to_datetime(data["Ship Date"])
data["Order Month"] = data["Order Date"].dt.month
data["Order Year"] = data["Order Date"].dt.year
data["Order Day of Week"] = data["Order Date"].dt.day_of_week
#print(data)
print(data.columns)


#2. stats about sales
sales_by_month = data.groupby("Order Month")["Sales"].sum().reset_index()
print("sales by month: \n", sales_by_month)
fig_sale_month = px.bar(sales_by_month,
              x="Order Month",
              y="Sales",
              title="Sales Analysis by Month")
#fig_sale_month.show()

sales_by_category = data.groupby("Category")["Sales"].sum().reset_index()
print("sales by category: \n", sales_by_category)
fig_sale_cat = px.pie(sales_by_category,
             values="Sales",
             names="Category",
             hole=0.5,
             color_discrete_sequence=px.colors.qualitative.Pastel,
             title="Sales Analysis by Category")
fig_sale_cat.update_traces(textposition="inside",
                  textinfo="percent+label")
#fig_sale_cat.show()

sales_by_subcategory = data.groupby("Sub-Category")["Sales"].sum().reset_index()
print("sales by sub-category: \n", sales_by_subcategory)
fig = px.bar(sales_by_subcategory,
             x="Sub-Category",
             y="Sales",
             title="Sales by Sub-Category")
#fig.show()

sales_by_category_subcategory = data.groupby(["Category", "Sub-Category"])["Sales"].sum().reset_index()
print("sales by category & sub-category: \n", sales_by_category_subcategory)


#3. stats about profit
profit_by_month = data.groupby("Order Month")["Profit"].sum().reset_index()
print("profit by month: \n", profit_by_month)
fig_prof_month = px.bar(profit_by_month,
              x="Order Month",
              y="Profit",
              title="Profit Analysis by Month")
#fig_prof_month.show()

profit_by_category = data.groupby("Category")["Profit"].sum().reset_index()
print("profit by category: \n", profit_by_category)
fig_prof_cat = px.pie(profit_by_category,
             names="Category",
             values="Profit",
             hole=0.5,
             color_discrete_sequence=px.colors.qualitative.Pastel,
             title="Profit Analysis by Category")
fig_prof_cat.update_traces(textposition="inside",
                  textinfo="percent+label")
#fig_prof_cat.show()

profit_by_subcategory = data.groupby("Sub-Category")["Profit"].sum().reset_index()
print("profit by sub-category: \n", profit_by_subcategory)
fig = px.bar(profit_by_subcategory,
             x="Sub-Category",
             y="Profit",
             title="Profit Analysis by Sub-Category")
#fig.show()

profit_by_category_subcategory = data.groupby(["Category", "Sub-Category"])["Profit"].sum().reset_index()
print("profit by category/sub-category: \n", profit_by_category_subcategory)


#4. mix sales and profit stats
color_palette = colors.qualitative.Pastel
summary_sales_profit_category = sales_by_category.merge(profit_by_category, on="Category")
print("Profit & Sales Analysis by Category: \n", summary_sales_profit_category)

sales_by_time = data.groupby(["Order Year", "Order Month"])["Sales"].sum().reset_index()
profit_by_time = data.groupby(["Order Year", "Order Month"])["Profit"].sum().reset_index()
summary_by_time = sales_by_time.merge(profit_by_time, on=["Order Year", "Order Month"])
print("summary by time: \n", summary_by_time)


fig = go.Figure()
fig.add_trace(go.Bar(x=sales_by_category["Category"],
                     y=sales_by_category["Sales"],
                     name="Sales",
                     marker_color=color_palette[0]))
fig.add_trace(go.Bar(x=profit_by_category["Category"],
                     y=profit_by_category["Profit"],
                     name="Profit",
                     marker_color=color_palette[1]))
#fig.show()


