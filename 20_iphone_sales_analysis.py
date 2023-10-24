import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


#1. get raw data
file_name = "20_apple_products.csv"
data = pd.read_csv(file_name)
print(data)
#print(data.isnull().sum())
print(data.columns)
#print(data.info())

#data = data.fillna(0)
#data = data.replace(np.nan, 0)


#2. rating & reviews stats
highest_rated = data.sort_values(by=["Star Rating"],
                                 ascending=False)
highest_rated = highest_rated.head(10)
print("Top rated products: \n", highest_rated[["Product Name", "Star Rating", "Number Of Ratings", "Number Of Reviews"]])

fig = px.bar(highest_rated,
             x="Product Name",
             y="Number Of Ratings")
fig.update_layout(title="Number of Ratings of Highest Rated iPhones")
#fig.show()

iphones = highest_rated["Product Name"].value_counts()
print(iphones)

fig = px.bar(highest_rated,
             x="Product Name",
             y="Number Of Reviews")
fig.update_layout(title="Number of Reviews of Highest Rated iPhones")
#fig.show()

fig = px.scatter(data,
                 x="Number Of Ratings",
                 y="Sale Price",
                 size="Discount Percentage",
                 trendline="ols",
                 title="Relationship between Sale Price and Number of Ratings")
#fig.show()

fig = px.scatter(data,
                 x="Number Of Ratings",
                 y="Discount Percentage",
                 size="Sale Price",
                 trendline="ols",
                 title="Relationship between Number of Ratings and Discount Percentage")
#fig.show()


#3. other stats abour ram
sales_by_ram = data.groupby("Ram")["Number Of Ratings", "Number Of Reviews"].sum().reset_index()
print(sales_by_ram)
#print(type(sales_by_ram))

fig = go.Figure()
fig.add_trace(go.Bar(x=sales_by_ram["Ram"],
                     y=sales_by_ram["Number Of Ratings"],
                     marker_color="blue",
                     name="Number of Ratings"))
fig.add_trace(go.Bar(x=sales_by_ram["Ram"],
                     y=sales_by_ram["Number Of Reviews"],
                     marker_color="red",
                     name="Number of Reviews"))
fig.update_layout(barmode="group",
                  title="Ratings & Reviews")
fig.show()


