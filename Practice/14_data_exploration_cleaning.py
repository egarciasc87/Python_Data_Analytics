
"""Exploratory analysis
- read data & explore variables
- categorical variables -> fixed number of unique cateogries (sex: male/female)
"""

import pandas as pd
import numpy as np
import os
import plotly.express as px


#1. get raw data
data = pd.read_csv("Titanic-Dataset.csv")
#print(data.head(10))
col_type_object = data.dtypes[data.dtypes == 'object'].index
print(data[col_type_object].head(10))
#print(data.columns)
#print(data.shape)
#print(data.dtypes)
#print(data.describe())
#print(data[col_type_object].describe())


#2. categorial and  not categorial variables
del data["PassengerId"]
del data["Ticket"]
print(data.head(10))

new_survived = pd.Categorical(data["Survived"])
new_survived = new_survived.rename_categories(["Died", "Survived"])
print(new_survived.describe())

new_class = pd.Categorical(data["Pclass"])
#print(new_class)
new_class = new_class.rename_categories(["Class1", "Class2", "Class3"])
data["Pclass"] = new_class
print(new_class.describe())

#print(data["Cabin"].unique())
char_cabin = data["Cabin"].astype(str)
new_cabin = np.array([cabin[0] for cabin in char_cabin])
new_cabin = pd.Categorical(new_cabin)
data["Cabin"] = new_cabin
print(new_cabin.describe())


#3. handle missing data and outliers
#data_stat = data.groupby(["Survived", "Cabin"])["Cabin"].aggregate("count")
data_stat = data.groupby(["Survived", "Cabin"])["Cabin"].count()
print(data_stat)
#print(data["Age"].describe())

missing = np.where(data["Age"].isnull() == True)
#print(missing)
#print(len(missing[0]))

data_missing_age = data.loc[data["Age"].isnull() == True]
#print(data_missing_age.head(10))

data.hist(column="Age",
          figsize=(9,6),
          bins=20)

fig = px.histogram(data_frame=data,
                   x="Age",
                   title="Age Distribution")
#fig.show()

new_age_var = np.where(data["Age"].isnull(),
                       28,
                       data["Age"])
data["Age"] = new_age_var
data["Age"] = data["Age"].replace(np.nan, 28)
print(data["Age"].describe())
fig = px.histogram(data_frame=data,
                   x="Age",
                   title="Age Distribution")
#fig.show()

data["Fare"].plot(kind="box",
                  figsize=(9,9))

index = np.where(data["Fare"] == max(data["Fare"]))
print(index)
print(data.loc[index])

data["Family"] = data["SibSp"] + data["Parch"]
most_family = np.where(data["Family"] == max(data["Family"]))
print(data.loc[most_family])


