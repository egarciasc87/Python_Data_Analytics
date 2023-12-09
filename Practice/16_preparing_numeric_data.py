
import numpy as np
import pandas as pd
import matplotlib
import plotly.express as px
from sklearn import preprocessing
#from sklearn.preprocessing import Imputer
#from pandas.tools.plotting import scatter_matrix
#%matplotlib inline


#1. get raw data
data = pd.read_csv("mtcars.csv")
#print(data.head(10))
#print(data.describe())
#print(data.isnull().count())
list_col = data.columns
new_list_col = ["model"]
for item in list_col[1:]:
    new_list_col.append(item)
data.columns = new_list_col
#print(data.head())


#2. oparetae on data
data.index = data.model
del data["model"]
print(data.head())

colmeans = data.sum()/data.shape[0]
#print(colmeans)
#print(data.shape)

centered = data - colmeans
print(centered.describe())

scaled_data = preprocessing.scale(data)
#print(scaled_data)
scaled_data = pd.DataFrame(scaled_data,
                           index=data.index,
                           columns=data.columns)
print(scaled_data.describe())


#3. randomly generated numbers
normally_distributed = np.random.normal(size=10000)
normally_distributed = pd.DataFrame(normally_distributed)
normally_distributed.columns = ["Value"]
#print(normally_distributed)

fig = px.histogram(data_frame=normally_distributed,
                   x="Value",
                   title="Value Distribution")
#fig.show()
normally_distributed.hist(figsize=(8,8),
                          bins=30)

skewed = np.random.exponential(scale=2,
                               size=10000)
skewed = pd.DataFrame(skewed)
skewed.columns = ["Value"]
#print(skewed)
fig = px.histogram(data_frame=skewed,
                   x="Value",
                   title="Value Distribution")
#fig.show()
skewed.hist(figsize=(8,8),
            bins=50)


#4. other operations on data
#two diffetent ways to calculate sqrt on dataframe column
skewed_sqrt = skewed.apply(np.sqrt)
print(skewed_sqrt)
skewed_sqrt = skewed
skewed_sqrt["Value"] = skewed_sqrt["Value"].pow(0.5)
print(skewed_sqrt)

fig = px.histogram(data_frame=skewed_sqrt,
                   x="Value",
                   title="Value Distribution")
#fig.show()

log_transformed = (skewed+1).apply(np.log)
print(log_transformed)
fig = px.histogram(data_frame=log_transformed,
                   x="Value",
                   title="Value Distribution")
#fig.show()

data_corr = data.iloc[:,0:6].corr()
print(data_corr)
print(data.corr().iloc[:6,:6])

data["mpg"] = np.where(data["mpg"] > 22, np.nan, data["mpg"])
print(data)
data["mpg"] = data["mpg"].replace(np.nan, data["mpg"].mean())
print(data)


