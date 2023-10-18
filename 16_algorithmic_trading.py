import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import numpy as np


def GetTickerData(ticker):
    #1. get trading data
    #ticker = "AAPL"
    stock = yf.Ticker(ticker)
    data = stock.history(period="10y")
    #print(data)
    data["Momentum"] = data["Close"].pct_change()
    #data = data.replace(np.nan, 0)
    #data = data.fillna(0)

    figure = make_subplots(rows=2,
                        cols=1)
    figure.add_trace(go.Scatter(x=data.index,
                                y=data["Close"],
                                name="Close Price"))
    figure.add_trace(go.Scatter(x=data.index,
                                y=data["Momentum"],
                                name="Momentum",
                                yaxis="y2"))

    figure.add_trace(go.Scatter(x=data.loc[data["Momentum"] > 0].index,
                                y=data.loc[data["Momentum"] > 0]["Close"],
                                mode="markers",
                                name="Buy",
                                marker=dict(color="green",
                                            symbol="triangle-up")))
    figure.add_trace(go.Scatter(x=data[data["Momentum"] < 0].index,
                                y=data[data["Momentum"] < 0]["Close"],
                                mode="markers",
                                name="Sell",
                                marker=dict(color="red",
                                            symbol="triangle-down")))

    figure.update_layout(title="Algorithmic Trading using Momentum",
                        xaxis_title="Date",
                        yaxis_title="Price")
    figure.update_yaxes(title="Momentum",
                        secondary_y=True)
    #figure.show()


    #2. some performance calculations
    data = data.reset_index()
    data = data.replace(np.nan, 0)
    data["Year"] = pd.to_datetime(data["Date"]).dt.year
    data = data.drop(columns=["Open", "Low", "High"])
    #print(data)

    avg_price = data.groupby("Year")["Close"].mean().reset_index()
    avg_price[ticker] = avg_price["Close"].pct_change()
    avg_price = avg_price.replace(np.nan, 0)
    avg_price[ticker] = avg_price[ticker] * 100
    avg_price = avg_price.drop(columns=["Close"])
    #print(avg_price)
    
    return avg_price


stock = "X"
stock_prices = pd.DataFrame()
stock_list = []

while (stock != ""):
    stock = input("Enter new ticker: ")

    if (stock == ""):
        break

    stock_list.append(stock)

    if (len(stock_prices.columns) == 0):
        stock_prices = GetTickerData(stock)
    else:
        temp_data = GetTickerData(stock)
        stock_prices = stock_prices.merge(temp_data, on="Year")
      
      
print(stock_prices)
fig = go.Figure()
count = 0

for item in stock_list:
    """ if (count == 0): 
        fig = go.Figure(go.Line(x=stock_prices["Year"],
                                y=stock_prices[item],
                                name=item))
        count += 1
    else: """
    fig.add_trace(go.Line(x=stock_prices["Year"],
                                y=stock_prices[item],
                                name=item))
fig.show()

