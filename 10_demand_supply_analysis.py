import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"


#1. collect raw data
file_name = "10_demand_supply_analysis.csv"
data = pd.read_csv(file_name)
#print(data.head(12))
#print(data.describe())
#print(data.isnull().sum())
data = data.dropna()
data ["Factor Demand/Supply"] = data["Riders Active Per Hour"] / data["Drivers Active Per Hour"]
#print(data)


#2. relationship between drivers and riders active per hour
demand = data["Drivers Active Per Hour"]
supply = data["Riders Active Per Hour"]
fig = px.scatter(data,
                 x="Drivers Active Per Hour",
                 y="Riders Active Per Hour",
                 title="Demand and Supply Analysis",
                 trendline="ols")
#fig.show()

avg_demand = data["Riders Active Per Hour"].mean()
avg_supply = data["Drivers Active Per Hour"].mean()
pct_change_demand = (max(data["Riders Active Per Hour"]) - min(data["Riders Active Per Hour"])) / avg_demand
pct_change_supply = (max(data["Drivers Active Per Hour"]) - min(data["Drivers Active Per Hour"])) / avg_supply
elasticity = pct_change_demand / pct_change_supply
print("Elasticity of demand with respect to the number of active drivers per hour: {:.2f}".format(elasticity))
data["Supply Ratio"] = data["Rides Completed"] / data["Drivers Active Per Hour"]

level_demand = ["Very Low", "Low", "Medium", "High"]
data["Level Demand"] = pd.cut(data["Factor Demand/Supply"],
                              bins=4,
                              labels=level_demand)
print(data)
level_demand_count = data.groupby("Level Demand")["Rides Completed"].count().reset_index()
level_demand_count = level_demand_count.rename(columns={"Rides Completed": "Total"})
print(level_demand_count)
fig = px.pie(level_demand_count,
             values="Total",
             names="Level Demand",
             hole=0.5,
             title="Level of Demand vs Supply",
             color_discrete_sequence=px.colors.qualitative.Pastel)
fig.show()




