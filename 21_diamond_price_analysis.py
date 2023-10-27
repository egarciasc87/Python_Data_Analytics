import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px


#1. get raw data
file_name = "21_diamond_price.csv"
data = pd.read_csv(file_name)
#print(data.head())
data["size"] = data["x"] * data["y"] * data["z"]
data = data.drop("Unnamed: 0", axis=1)
print(data.head())
#print(data.tail(10))
#print(data[0:5])
#print(data[:11])
#print(data.isnull().sum())
#print(data.columns)


#2. analyze price
fig = px.scatter(data,
                 x="carat",
                 y="price",
                 size="depth",
                 color="cut",
                 trendline="ols")
#fig.show()

fig = px.scatter(data,
                 x="size",
                 y="price",
                 color="cut",
                 size="size",
                 trendline="ols")
fig.show()


#3. analysis by 
fig = px.line(data,
              x="size",
              y="price",
              color="cut")
fig.show()
