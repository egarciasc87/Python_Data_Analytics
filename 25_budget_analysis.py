import pandas as pd
import numpy as np
import plotly.express as px

#1. get raw data
file_name = "25_budget_analysis.csv"
data = pd.read_csv(file_name)

title = data.columns[0]
#data[title] = data[title].replace(np.nan, "XXX")
#data = data.loc[data[title] != "XXX"]

data = data.dropna()
#data.columns = ["Area"]
#print(data.describe())


#2. order data into department & ministry
data = data.iloc[[0,8,11,14,18,23,41,42,43],:]
row = {'Department /Ministry': 'OTHERS', 'Fund allotted(in ₹crores)': 592971.0800000001}
data = data.append(row, ignore_index = True)
data.columns = ["Ministry", "Budget"]
print(data)


fig = px.bar(data,
             x="Ministry",
             y="Budget",
             title="Total Budget by Ministry")
#fig.show()

fig = px.pie(data,
             names="Ministry",
             values="Budget",
             title="Budget distribution")
#fig.show()


