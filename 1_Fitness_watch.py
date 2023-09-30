import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_white"
import plotly.express as px

def CreateFigure(data, 
                 AxisX,
                 AxisY,
                 title):
    fig = px.line(data,
                  x=AxisX,
                  y=AxisY,
                  title=title)
    fig.show()


#1. read row data
file_name = "1_Apple-Fitness-Data.csv"
data = pd.read_csv(file_name)
#print(data)
print(data.columns)
#print(data.isnull().sum())


#2. create graphs with simple data
#CreateFigure(data, "Time", "Step Count", "Step count over time")
#CreateFigure(data, "Time", "Distance", "Distance over time")
#CreateFigure(data, "Time", "Energy Burned", "Energy burned over time")
#CreateFigure(data, "Time", "Walking Speed", "Walking speed over time")


#3. create graph with average
average_step = pd.DataFrame()
average_step["Date"] = data["Date"]
average_step["Step Count"] = data["Step Count"]
print(average_step.head())
average_step = average_step.groupby(["Date"]).mean().reset_index()
print(average_step)
#CreateFigure(average_step, "Date", "Step Count", "Avg step count by date")


#4. create graph about efficiency
data_efficiency = pd.DataFrame()
data_efficiency["Efficiency"] = data["Distance"]/data["Step Count"]
data_efficiency["Time"] = data["Time"]
#CreateFigure(data_efficiency, "Time", "Efficiency", "Walking efficiency over time")


#5. create graph about variations
time_intervals = pd.cut(pd.to_datetime(data["Time"]).dt.hour,
                        bins=[0, 12, 18, 24],
                        labels=["Morning", "Afternoon", "Evening"],
                        right=False)
data["Time Interval"] = time_intervals
print(data.head())

fig7 = px.scatter(data,
                  x="Step Count",
                  y="Walking Speed",
                  color="Time Interval",
                  title="Step count and walking speed variations",
                  trendline="ols")
fig7.show()


#6. create graph for daily averages
metrics_to_visualize = ["Step Count", 
                        "Distance",
                        "Energy Burned",
                        "Flights Climbed",
                        "Walking Double Support Percentage",
                        "Walking Speed"]
daily_avg = data.groupby("Date").mean().reset_index()
print(daily_avg)

daily_avg_melted = daily_avg.melt(id_vars=["Date"],
                                  value_vars=metrics_to_visualize)
print(daily_avg_melted)
fig8 = px.treemap(daily_avg_melted,
                  path=["variable"],
                  values="value",
                  color="variable",
                  hover_data=["value"],
                  title="Daily averages for different matrics")
fig8.show()

 
#7. create another graph for daily averages
metrics_to_visualize = ["Distance", "Energy Burned", 
                        "Flights Climbed",
                        "Walking Double Support Percentage",
                        "Walking Speed"]
daily_metrics_melted = daily_avg.melt(id_vars=["Date"],
                                      value_vars=metrics_to_visualize)

fig9 = px.treemap(daily_metrics_melted,
                  path=["variable"],
                  values="value",
                  color="variable",
                  hover_data=["value"],
                  title="Daily average for different metrics (exc. Step Count)")
fig9.show()
