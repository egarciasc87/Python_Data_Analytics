import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


#1. get and validate raw data
births = pd.read_csv("28_births.csv")
births["day"] = births["day"].fillna(0)
births["day"] = births["day"].astype(int)
#print(births.describe())
#print(births.isnull().sum())

#births_nan = births.loc[births["day"] == np.nan]
#print(births_nan)
print(births.head())


#2. data operation
births["decade"] = 10 * (births["year"] // 10)
sns.set()
birth_decade = births.pivot_table("births",
                   index="decade",
                   columns="gender",
                   aggfunc="sum")
print(birth_decade)
birth_decade.plot()
plt.ylabel("Total births per year")
#plt.show()

birth_group = births.groupby(["decade", "gender"])["births"].sum().reset_index()
print(birth_group)
fig = px.line(data_frame=birth_group,
              x="decade",
              y="births",
              color="gender",
              title="# of Births by Decade")
fig.update_layout(xaxis_title="Decade",
                  yaxis_title="Total Births")
#fig.show()

birth_avg = births.groupby(["decade", "gender"])["births"].mean().reset_index()
birth_avg["births"] = birth_avg["births"].round(0)
print(birth_avg)
fig = px.bar(birth_avg,
             x="decade",
             y="births",
             color="gender",
             title="Average Births by Decade")
fig.update_layout(xaxis_title="Decade",
                  yaxis_title="Avg Births")
#fig.show()

data_summary = birth_group.merge(birth_avg,
                                 on=["decade", "gender"])
data_summary.columns = ["decade", "gender", "Total Births", "Average Births"]
print(data_summary)

#3. frther data exploration
quartiles = np.percentile(births["births"], [25, 50, 75])
print(quartiles)
mu = quartiles[1]
sig = 0.74 * (quartiles[2] - quartiles[0])
