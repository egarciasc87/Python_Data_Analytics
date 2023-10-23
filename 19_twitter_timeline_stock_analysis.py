import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import math
pio.templates.default = "plotly_white"


#1. get raw data
file_name = "19_twitter_timeline.csv"
data = pd.read_csv(file_name)
print(data)
print(data.isnull().sum())
#print(data.info())

#data = data.replace(np.nan, 0)
#data = data.fillna(0)
data = data.dropna()
print(data)


#2. analyse data
fig = go.Figure(data=[go.Candlestick(x=data["Date"],
                                     open=data["Open"],
                                     high=data["High"],
                                     low=data["Low"],
                                     close=data["Close"])])
fig.update_layout(title="Twitter Stock Price over Time",
                  xaxis_rangeslider_visible=False)
#fig.show()

fig = px.bar(data,
             x="Date",
             y="Close",
             color="Close")
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(title="Twitter Stick Price",
                  xaxis_rangeslider_visible=False)
fig.update_xaxes(rangeselector=dict(buttons=list([
    dict(count=1, label="1m", step="month", stepmode="backward"),
    dict(count=6, label="6m", step="month", stepmode="backward"),
    dict(count=1, label="1y", step="year", stepmode="backward"),
    dict(count=2, label="2y", step="year", stepmode="backward"),
    dict(step="all")
])))
#fig.show()


#3. some operartions on the data
data["Year"] = pd.to_datetime(data["Date"]).dt.year
data["Month"] = pd.to_datetime(data["Date"]).dt.month
print(data)
data_high_per_year = data.groupby("Year")["Close"].max().reset_index()
print(data_high_per_year)
data_high_per_month = data.groupby(["Year", "Month"])["Close"].max().reset_index()
#data_high_per_month["Year"] = data_high_per_month["Year"].apply(str)
#data_high_per_month["Period"] = data_high_per_month["Month"].apply(str)
data_high_per_month["Period"] = data_high_per_month["Year"].apply(str) + "-" + data_high_per_month["Month"].apply(str)
#data_high_per_month["Period"] = data_high_per_month["Year"].to_string() + "-" + data_high_per_month["Month"].to_string()
print(data_high_per_month)

data_volumen_per_year = data.groupby("Year")["Volume"].sum().reset_index()
data_volumen_per_year["Volume"] = data_volumen_per_year["Volume"] / 1000000
data_volumen_per_year["Volume"] = data_volumen_per_year["Volume"].round(2)
print(data_volumen_per_year)

fig = px.pie(data_volumen_per_year,
             names="Year",
             values="Volume",
             color="Year",
             hole=0.5,
             color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(title="Volume Traded per Year")
fig.update_traces(textposition="inside",
                  textinfo="percent+label")
#fig.show()

fig = px.bar(data_volumen_per_year,
             x="Year",
             y="Volume",
             color="Volume")
fig.update_layout(title="Volume Traded per Year")
#fig.show()

data_high_per_month["Return"] = data_high_per_month["Close"].pct_change()
data_high_per_month["Return"] = (data_high_per_month["Return"] * 100).round(2)
print(data_high_per_month)

fig = px.bar(data_high_per_month,
             x="Period",
             y="Return",
             color="Return")
fig.update_layout(title="Stock Return over Time (%)")
fig.show()

