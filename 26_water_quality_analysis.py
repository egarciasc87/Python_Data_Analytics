import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import plotly.express as px
import seaborn as sns

from pycaret.classification import *
import pycaret.classification as pyc


#1. get & verify raw data
data = pd.read_csv("26_water_potability.csv")
#print(data[["Sulfate", "Trihalomethanes"]])
#print(data.describe())
print("Columns: \n", data.columns)
#print(data.isnull().sum())

data = data.dropna()
#data = data.reset_index()
#print(data["Potability"])
#print(data.Potability)
#print(data.isnull().sum())


#2 some graphic & stats
potability = data.groupby("Potability")["Sulfate"].count().reset_index()
potability["Potability"] = potability["Potability"].apply(lambda x: "Si" if x == 1 else "No")
potability.columns = ["Potability", "Total"]
print("Potability: \n", potability)

fig = px.bar(potability,
             x="Potability",
             y="Total",
             color="Potability",
             title="Total Potable Samples")
#fig.show()

fig = px.histogram(data,
                   x="ph",
                   color="Potability",
                   title="Factor that affect water quality: PH")
#fig.show()

fig = px.histogram(data,
                   x="Hardness",
                   color="Potability",
                   title="Factor that affect water quality: Hardness")
#fig.show()

fig = px.histogram(data,
                   x="Solids",
                   color="Potability",
                   title="Factors affecting water quality: Solids")
#fig.show()

fig = px.histogram(data,
                   x="Chloramines",
                   color="Potability",
                   title="Factors affecting water quality: Chloramines")
#fig.show()

fig = px.histogram(data,
                   x="Sulfate",
                   color="Potability",
                   title="Factors affecting water quality: Sulfate")
#fig.show()


correlation = data.corr()
corr_ph = correlation["ph"].sort_values(ascending=False)
print(corr_ph)

clf = pyc.setup(data, 
            target="Potability",
            verbose=False,
            session_id=786)
compare_models()

model = create_model("rf")
predict = predict_model(model, 
                        data=data)
predict.head()

