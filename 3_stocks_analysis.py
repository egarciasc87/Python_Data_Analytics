import pandas as pd
import yfinance as yf
from datetime import datetime
import plotly.express as px

start_date = datetime.now() - pd.DateOffset(months=3)
end_date = datetime.now()
tickers = ["AAPL", "MSFT", "NFLX", "GOOG"]
dict_tickers = {"AAPL": "Apple", "MSFT": "Microsoft", "NFLX": "Netflix", "GOOG": "Google"}
df_list = []

#print(start_date)
#print(end_date)
#print(datetime.now().hour)
#print(datetime.now().day)


#1. Get stock data
for ticker in tickers:
    print("Getting data from {}...".format(ticker))
    data = yf.download(ticker, start_date, end_date)
    data["Ticker"] = dict_tickers[ticker]
    df_list.append(data)
    #print(data.head()) 

#df = pd.concat(df_list, keys=tickers, names=["Ticker", "Date"])
df = pd.concat(df_list)
df = df.reset_index()
print("\n")
print(df)


#2. Now let’s have a look at the performance in the 
# stock market of all the companies:
fig = px.line(df,
              x="Date",
              y="Close",
              title="Stock performance",
              color="Ticker")
fig.update_layout(xaxis_title="Trading date",
                  yaxis_title="Stock close price")
#fig.show()


#3.Now let’s look at the faceted area chart
fig = px.area(df,
              x="Date",
              y="Close",
              facet_col="Ticker",
              color="Ticker",
              title="Stock prices",
              labels={"Date": "Date", "Close": "Closing price", "Ticker": "Company"})
#fig.show()


#4.Calculate moving averages of the stock prices
#df_ = df.groupby("Ticker")["Close", "Adj Close"].mean()
#df_ = df_.reset_index()
#df_.columns = ["Company", "Close", "Adj Close"]
df["MA3"] = df.groupby("Ticker")["Close"].rolling(window=3).mean().reset_index(0, drop=True)
df["MA10"] = df.groupby("Ticker")["Close"].rolling(window=10).mean().reset_index(0, drop=True)
df["MA20"] = df.groupby("Ticker")["Close"].rolling(window=20).mean().reset_index(0, drop=True)
print(df[["Date", "Ticker", "Close", "MA3", "MA10", "MA20"]])

for ticker, group in df.groupby("Ticker"):
    fig = px.line(group,
                  x="Date",
                  y=["Close", "MA3", "MA10", "MA20"],
                  title="{} Moving averages".format(ticker))
    #fig.show()


#5. Now let's analyze the volatility
df["Volatility"] = df.groupby("Ticker")["Close"].pct_change().rolling(window=10).std().reset_index(0, drop=True)
print(df[["Date", "Ticker", "Close", "MA3", "MA10", "MA20", "Volatility"]])
fig = px.line(df,
              x="Date",
              y="Volatility",
              color="Ticker",
              title="Volatility of all companies")
#fig.show()


#Calculate correlation between AAPL and MSFT
apple = df.loc[df["Ticker"] == "Microsoft", ["Date", "Close"]]
apple = apple.rename(columns={"Close": "AAPL"})
#print(apple)
microsoft = df.loc[df["Ticker"] == "Microsoft", ["Date", "Close"]]
microsoft = microsoft.rename(columns={"Close": "MSFT"})
#print(microsoft)
df_corr = pd.merge(apple, microsoft, on="Date")
print(df_corr)

fig = px.scatter(df_corr,
                 x="AAPL",
                 y="MSFT",
                 trendline="ols",
                 title="Correlation between Apple and Microsoft")
fig.show()
