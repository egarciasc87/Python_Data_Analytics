import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


#1. get raw data
file_name = "14_accelerometer_data_analysis.csv"
data = pd.read_csv(file_name)
#print(data)
#print(data.describe())
#print(data.isnull().sum())
#print(data.info())


#2. some figures
fig = px.line(data,
              x="Date",
              y=["accel_x", "accel_y", "accel_z"],
              title="Acceleration data over time")
#fig.show()

data["hour"] = pd.to_datetime(data["Time"]).dt.hour
data["day_of_week"] = pd.to_datetime(data["Date"]).dt.day_of_week
print(data)

agg_data = data.pivot_table(index="hour",
                            columns="day_of_week",
                            #values="accel_x",
                            values=["accel_x", "accel_y"],
                            aggfunc="mean")
print(agg_data)

fig = go.Figure(go.Heatmap(x=agg_data.columns.levels[1],
                           y=agg_data.index,
                           z=agg_data.values,
                           xgap=1,
                           ygap=1,
                           colorbar=dict(title="Average Acceleration")))
fig.update_layout(title="Average acceleration by hour of the day")
#fig.show()

data["accel_mag"] = (data["accel_x"] ** 2 + data["accel_y"] ** 2 + data["accel_z"] ** 2) ** 0.5
print(data)

fig = px.scatter(data,
                 x="Time",
                 y="accel_mag",
                 title="Magnitude of acceleration over time")
#fig.show()

fig = px.scatter_3d(data,
                    x="accel_x",
                    y="accel_y",
                    z="accel_z",
                    title="Acceleration in 3D space")
#fig.show()

fig = px.histogram(data,
                   x="accel_mag",
                   nbins=50,
                   title="Acceleration magnitud histogram")
fig.show()


