import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"


#1. get raw data
file_name = "11_recession_analysis.csv"
data = pd.read_csv(file_name)
#print(data)
#print(data.isnull())
#print(data.isnull().sum())


#2. create some heatmaps from GDP growth
fig = go.Figure(data=go.Heatmap(
    z=[data["GDP Growth"]],
    x=data.index,
    y=["GDP Growth"],
    colorscale="Viridis"))
fig.update_layout(title="GDP Growth over time",
                  xaxis_title="Time Period",
                  yaxis_title="")
#fig.show()

fig = px.bar(data,
                         x = data.index,
                         y = "GDP Growth",
                         title = "GRP Growth over time")
fig.update_layout(title="GDP Growth over time",
                  xaxis_title="Time Period",
                  yaxis_title="")
#fig.show()


#3.some statistics about GPD Growth 
data["Result"] = np.where(data["GDP Growth"] > 0, "Positive Growth", "Negative Growth")
gpd_growth_count = data.groupby("Result")["GDP Growth"].count().reset_index()
#print(data)
print(gpd_growth_count)

fig = px.pie(gpd_growth_count,
             values="GDP Growth",
             names="Result",
             title="Positive vs Negative GDP Growth",
             color_discrete_sequence=px.colors.qualitative.Pastel)
#fig.show()

fig = px.line(data,
              x=data.index,
              y="GDP Growth",
              title="GPD Growth over time")
#fig.show()


#4. get quarterly GDP Growth
data["Time Period"] = pd.to_datetime(data["Time Period"], format="/%m/%Y")
data.set_index("Time Period", inplace=True)
quarterly_data = data.resample("Q").mean()
#print(quarterly_data)
#print(data.resample("Q").sum())

quarterly_data['Recession'] = ((quarterly_data['GDP Growth'] < 0) & 
                               (quarterly_data['GDP Growth'].shift(1) < 0))
quarterly_data["Recession"].fillna(False, inplace=True)
print(quarterly_data)

fig = go.Figure()
fig.add_trace(go.Scatter(x=quarterly_data.index,
                         y=quarterly_data["GDP Growth"],
                         name="GDP Growth",
                         line=dict(color="green", width=2)))
fig.add_trace(go.Scatter(x=quarterly_data[quarterly_data['Recession']].index, 
                         y=quarterly_data[quarterly_data['Recession']]['GDP Growth'], 
                         name='Recession', line=dict(color='red', width=2)))
#fig.show()

quarterly_data['Recession Start'] = quarterly_data['Recession'].ne(quarterly_data['Recession'].shift()).cumsum()
recession_periods = quarterly_data.groupby('Recession Start')
recession_duration = recession_periods.size()
recession_severity = recession_periods['GDP Growth'].sum()

fig = go.Figure()
fig.add_trace(go.Bar(x=recession_duration.index, y=recession_duration,
                     name='Recession Duration'))
fig.add_trace(go.Bar(x=recession_severity.index, y=recession_severity,
                     name='Recession Severity'))

fig.update_layout(title='Duration and Severity of Recession',
                  xaxis_title='Recession Periods',
                  yaxis_title='Duration/Severity')

fig.show()

