
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


#1. get raw data
data = pd.read_csv("mtcars.csv")
data = data.rename(columns={"Unnamed: 0": "model"})
data.index = data.model
del data["model"]
print(data.head())
#print(data.isnull().count())
#print(data.shape)


#2. statisticas on data
print(data.describe())

#two ways to calcuate same average
print(data.mean())
#print(data.mean(axis=0))

print(data.median())
data_temp = data[["mpg"]].reset_index()
data_temp["Above_Below"] = np.where(data_temp["mpg"] > 19.2, "Above", "Below")
#data_group = data_temp.groupby("Above_Below")["mpg"].count().reset_index()
#print(data_group)


#3. dataframes with data randomly created
norm_data = pd.DataFrame(np.random.normal(size=100000))
print("\n\nValues:\n", norm_data)
print("mean:\n", norm_data.mean())
print("median:\n", norm_data.median())
norm_data.plot(kind="density",
               figsize=(10,10))
plt.vlines(norm_data.mean(),
           ymin=0,
           ymax=0,
           linewidth=0.5)
plt.vlines(norm_data.median(),
           ymin=0,
           ymax=0.4,
           linewidth=2.0,
           color="red")
#plt.show()

skewed_data = pd.DataFrame(np.random.exponential(size=100000))
print("\n\nValues:\n", skewed_data)
print("mean:\n", skewed_data.mean())
print("median:\n", skewed_data.median())
skewed_data.plot(kind='density',
                 figsize=(10,10),
                 xlim=(-1,5))
plt.vlines(skewed_data.mean(),
           ymin=0,
           ymax=0.8,
           linewidth=5.0,
           color='green')
plt.vlines(skewed_data.median(),
           ymin=0,
           ymax=0.8,
           linewidth=2.0,
           color='red')
#plt.show()

norm_data = np.random.normal(size=50)
outliers = np.random.normal(15, size=3)
combined_data = pd.DataFrame(np.concatenate(
    (norm_data, outliers), axis=0))
print("\n\nValues:\n", combined_data)
print("mean:\n", combined_data.mean())
print("median:\n", combined_data.median())
combined_data.plot(kind='density',
                   figsize=(10,10),
                   xlim=(-5,20))
plt.vlines(combined_data.mean(),    
           ymin=0, 
           ymax=0.2,
           linewidth=5.0,
           color='green')
plt.vlines(combined_data.median(),
           ymin=0, 
           ymax=0.2, 
           linewidth=2.0,
           color="red")
#plt.show()


#4. review measures of spread
print("\n\n")
print("mpg mean: ", data["mpg"].mean())
print("mpg meadian: ", data["mpg"].median())
print("mpg max: ", data["mpg"].max(), " - ", max(data["mpg"]))
print("mpg min: ", data["mpg"].min(), " - ", min(data["mpg"]))
print(data.describe())
list_quantile = [data["mpg"].quantile(0.25),
                 data["mpg"].quantile(0.5),
                 data["mpg"].quantile(0.75)]
print(list_quantile)

data.boxplot(column="mpg",
               return_type='axes',
               figsize=(8,8))

plt.text(x=0.74, y=22.25, s="3rd Quartile")
plt.text(x=0.8, y=18.75, s="Median")
plt.text(x=0.75, y=15.5, s="1st Quartile")
plt.text(x=0.9, y=10, s="Min")
plt.text(x=0.9, y=33.5, s="Max")
plt.text(x=0.7, y=19.5, s="IQR", rotation=90, size=25);
plt.show()


#5. skewness and kurtosis
print("\n\n")
print("skewness: ", data["mpg"].skew())
print("kurtosis: ", data["mpg"].kurt())

norm_data = np.random.normal(size=100000)
skewed_data = np.concatenate((np.random.normal(size=35000)+2, 
                             np.random.exponential(size=65000)), 
                             axis=0)
uniform_data = np.random.uniform(0,2, size=100000)
peaked_data = np.concatenate((np.random.exponential(size=50000),
                             np.random.exponential(size=50000)*(-1)),
                             axis=0)

data_df = pd.DataFrame({"norm":norm_data,
                       "skewed":skewed_data,
                       "uniform":uniform_data,
                       "peaked":peaked_data})
data_df.plot(kind="density",
            figsize=(10,10),
            xlim=(-5,5))


