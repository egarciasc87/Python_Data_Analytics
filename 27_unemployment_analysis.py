import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


#1. get and validate raw data
url = "https://raw.githubusercontent.com/amankharwal/Website-data/master/unemployment.csv"
data = pd.read_csv(url)
print(data)
#print(data.columns)

list_cols_new = []
for item in data.columns:
    item = item[1:] if item[0] == " " else item 
    list_cols_new.append(item)

data.columns = list_cols_new
print(data.columns)
#print(data.isnull().sum())
#print(data.info())


#2. visualizations
plt.style.use("seaborn-whitegrid")
plt.figure(figsize=(12, 10))
sns.heatmap(data.corr())
#plt.show()

plt.title("Indian Unemployment")
sns.histplot(x="Estimated Employed", hue="Region", data=data)
#plt.show()


column_1 = "Estimated Unemployment Rate (%)"
column_2 = "Estimated Labour Participation Rate (%)"
data_unemploy_rate_avg = data.groupby("Region.1")[column_1].mean().reset_index()
print(data_unemploy_rate_avg)

fig = px.bar(data_unemploy_rate_avg,
             x = "Region.1",
             y = column_1,
             title = "Unemployment Rate Average (%) by Region")
fig.update_layout(xaxis_title = "Region", yaxis_title = "Average Rate")
#fig.show()

data_unemploy_rate_avg = data.groupby("Region")[column_1].mean().reset_index()
#print(data_unemploy_rate_avg)

fig = px.bar(data_unemploy_rate_avg,
             x = "Region",
             y = column_1,
             title = "Unemployment Rate Average (%) by State")
fig.update_layout(xaxis_title = "State", yaxis_title = "Average Rate")
#fig.show()



unemployment = data[["Region", "Region.1", column_1]]
unemployment.columns = ["State", "Region", column_1]
fig = px.sunburst(unemployment,
                  path=["Region", "State"],
                  values=column_1,
                  width=700,
                  height=700,
                  color_continuous_scale="RdY1Gn",
                  title="Unemployment Rate in Indica")
#fig.show()


data_avg = data.groupby("Region.1")[[column_1, column_2]].mean().reset_index()
data_avg[column_1] = data_avg[column_1].round(2)
data_avg[column_2] = data_avg[column_2].round(2)
print(data_avg)
fig = px.bar(data_avg,
             x="Region.1",
             y=[column_1, column_2],
             title="Unemployment vs Labor Participation by Region")
fig.update_layout(xaxis_title="Region", yaxis_title="Average (%)")
fig.show()





