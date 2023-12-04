import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import plotly.express as px


#1. get and validate raw data
data = pd.read_csv("29_california_cities.csv")

list_cols = data.columns
new_list_col = []
new_list_col.append("Index")
for item in list_cols[1:]:
    new_list_col.append(item)
data.columns = new_list_col
#data = data.drop(columns="Index")
#print(data)
#print(data.describe())
#print(data.isnull().sum())
print(data.columns)


#2. statistics about population, area and water
data_temp = data[["city", "population_total", "area_total_km2", "area_water_km2"]]
data_temp["population/km2"] = (data_temp["population_total"]/data_temp["area_total_km2"]).round(0)
data_temp["km2_water/100Kpeople"] = (data_temp["area_water_km2"] * 100000 /data_temp["population_total"])
print(data_temp.head())

data_temp_fig = data_temp.sort_values(by="population/km2", ascending=False)
#print(data_temp_fig.head())
fig = px.bar(data_temp_fig.head(10),
             x="city",
             y="population/km2",
             title="Population by Km2")
fig.update_layout(xaxis_title="City",
                  yaxis_title="Population")
#fig.show()

data_temp_fig = data_temp.sort_values(by="population_total", ascending=False)
fig = px.pie(data_temp_fig.head(10),
             names="city",
             values="population_total",
             title="Population Distribution by City")
#fig.show()


#3. scatter the point
latitude, longitude = data["latd"], data["longd"]
population, area = data["population_total"], data["area_total_km2"]
#print(latitude.head())
#print(longitude.head())
#print(population.head())
#print(area.head())

""" 
seaborn.set()
plt.scatter(longitude, latitude, label=None, c=np.log10(population),
            cmap='viridis', s=area, linewidth=0, alpha=0.5)
plt.axis(aspect='equal')
plt.xlabel('Longitude')
plt.ylabel('Longitude')
plt.colorbar(label='log$_{10}$(population)')
plt.clim(3, 7)

for area in [100, 300, 500]:
    plt.scatter([], [], c='k', alpha=0.3, s=area, label=str(area) + 'km$^2$')
plt.legend(scatterpoints=1, frameon=False, labelspacing=1, title='City Areas')
plt.title("Area and Population of California Cities")
plt.show()
 """
