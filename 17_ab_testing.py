import numpy as np
import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_white"


#1. get raw data
control_data = pd.read_csv("17_control_group.csv", sep=";")
test_data = pd.read_csv("17_test_group.csv", sep=";")

control_data.columns = ["Campaign Name", "Date", "Amount Spent", 
                        "Number of Impressions", "Reach", "Website Clicks", 
                        "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"]

test_data.columns = ["Campaign Name", "Date", "Amount Spent", 
                        "Number of Impressions", "Reach", "Website Clicks", 
                        "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"]

print(control_data.head())
#print(control_data.isnull().sum())
#print(control_data.columns)
#print(test_data.head())
#print(test_data.isnull().sum())
#print(test_data.columns)


list_column_na = ["Number of Impressions", "Reach", "Website Clicks", "Searches Received", "Added to Cart", "Purchases", "Content Viewed"]

for item in list_column_na:
    #control_data[item] = control_data[item].replace(np.nan, control_data[item].mean())
    control_data[item].fillna(value=control_data[item].mean(),
                              inplace=True)

#print(control_data.isnull().sum())


#2. stats and graphs 
ab_data = control_data.merge(test_data,
                             how="outer").sort_values(["Date"])
ab_data = ab_data.reset_index(drop=True)
ab_data_count = ab_data.groupby("Campaign Name")["Date"].count().reset_index()
#ab_data = ab_data.sort_values(["Campaign Name", "Date"])
print(ab_data.head())
#print(ab_data["Campaign Name"].value_counts())
#print(ab_data_count)

fig = px.scatter(data_frame=ab_data,
                 x="Number of Impressions",
                 y="Amount Spent",
                 size="Amount Spent",
                 color="Campaign Name",
                 trendline="ols")
#fig.show()

#total searches
list_columns = ["Searches Received", "Content Viewed", 
                "Website Clicks", "Added to Cart",
                "Amount Spent", "Purchases"]
ab_data_total = ab_data.groupby("Campaign Name")[list_columns].sum().reset_index()
print("Control vs test: total stats: \n", ab_data_total)

for item in list_columns:
    fig = px.pie(ab_data_total,
                 values=item,
                 names="Campaign Name",
                 hole=0.5,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textinfo="percent+label",
                      textposition="inside")
    fig.update_layout(title="Test vs Control: " + item)
    #fig.show()


fig = px.scatter(ab_data,
                 x="Content Viewed",
                 y="Website Clicks",
                 size="Website Clicks",
                 color="Campaign Name",
                 trendline="ols")
#fig.show()

fig = px.scatter(ab_data,
                 x="Added to Cart",
                 y="Content Viewed",
                 size="Content Viewed",
                 color="Campaign Name",
                 trendline="ols")
#fig.show()

fig = px.scatter(ab_data,
                 x="Purchases",
                 y="Added to Cart",
                 size="Added to Cart",
                 color="Campaign Name",
                 trendline="ols")
fig.show()



# ab_data_total_searches = ab_data.groupby("Campaign Name")["Searches Received"].sum().reset_index()
# print(ab_data_total_searches)

# fig = px.pie(ab_data_total_searches,
#              names="Campaign Name",
#              values="Searches Received",
#              hole=0.5,
#              color_discrete_sequence=px.colors.qualitative.Pastel)
# fig.update_traces(textinfo="percent+label",
#                   textposition="inside")
# fig.update_layout(title="Total Searches")
# #fig.show()

# #total clicks
# ab_data_total_clicks = ab_data.groupby("Campaign Name")["Website Clicks"].sum().reset_index()
# print(ab_data_total_clicks)

# fig = px.pie(ab_data_total_clicks,
#              values="Website Clicks",
#              names="Campaign Name",
#              hole=0.5,
#              color_discrete_sequence=px.colors.qualitative.Pastel)
# fig.update_traces(textinfo="percent+label",
#                   textposition="inside")
# #fig.show()

# #content viewed
# ab_data_total_viewed = ab_data.groupby("Campaign Name")["Content Viewed"].sum().reset_index()
# print(ab_data_total_viewed)

# fig = px.pie(ab_data_total_viewed,
#              values="Content Viewed",
#              names="Campaign Name",
#              hole=0.5,
#              color_discrete_sequence=px.colors.qualitative.Pastel)
# fig.update_traces(textposition="inside",
#                   textinfo="percent+label")
# #fig.show()



