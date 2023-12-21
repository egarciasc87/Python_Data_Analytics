import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


#1. get raw data
data = pd.read_csv("diamonds.csv")
print(data)
#print(data.isnull().sum())
#print(data.shape)

data = data.drop(columns={"Unnamed: 0"})
print(data)


#2. graphics
data.hist(column="carat",
          figsize=(8,8),
          color="blue")


fig = px.histogram(data,
                   x="carat",
                   title="Distribution by Carat")
#fig.show()

plt.hist(data=data,
         x="carat",
         color="blue",
         bins=50)
#plt.show()

print(data[data["carat"] > 3.5])

data.boxplot(column="carat");




