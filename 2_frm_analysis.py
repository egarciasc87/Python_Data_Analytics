import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import plotly.colors
from datetime import datetime
pio.templates.default = "plotly_white"


def DataGrouping():
    data_1 = pd.DataFrame()
    data_1["Location"] = data["Location"]
    data_1["TransactionAmount"] = data["TransactionAmount"]
    print(data_1.groupby("Location").mean().reset_index())
    print(data_1.groupby("Location").sum().reset_index())


file_name = "2_rfm_data.csv"
data = pd.read_csv(file_name)
print(data)
#print(data.columns)


#DataGrouping()

#Calcular Recency, Frequency and Monetary values
data["PurchaseDate"] = pd.to_datetime(data["PurchaseDate"])
data["Recency"] = (datetime.now().date() - data["PurchaseDate"].dt.date).dt.days
frequency_data = data.groupby("CustomerID")["OrderID"].count().reset_index()
frequency_data.rename(columns={"OrderID": "Frequency"}, inplace=True)
data = data.merge(frequency_data, on="CustomerID", how="left")

monetary_data = data.groupby("CustomerID")["TransactionAmount"].sum().reset_index()
monetary_data.rename(columns={"TransactionAmount": "MonetaryValue"}, inplace=True)
data = data.merge(monetary_data, on="CustomerID", how="left")
print(data)


#Calculare Recency, Frequency, Monetary and RFM scores
recency_scores = [5, 4, 3, 2, 1] #higher score for lower recency
frequency_scores = [1, 2, 3, 4, 5] #higher score for higher frequency
monetary_scores = [1, 2, 3, 4, 5] #higher score for higher monetary value

data["RecencyScore"] = pd.cut(data["Recency"], 
                              bins=5, 
                              labels=recency_scores)
data["FrequencyScore"] = pd.cut(data["Frequency"],
                                bins=5,
                                labels=frequency_scores)
data["MonetaryScore"] = pd.cut(data["MonetaryValue"],
                               bins=5,
                               labels=monetary_scores)
print(data)

data["RecencyScore"] = data["RecencyScore"].astype(int)
data["FrequencyScore"] = data["FrequencyScore"].astype(int)
data["MonetaryScore"] = data["MonetaryScore"].astype(int)
print(data.info())

data["RFM_Score"] = data["RecencyScore"] + data["FrequencyScore"] + data["MonetaryScore"]
segment_label = ["Very Low", "Low", "Medium", "High", "Very High"]
data["Value Segment"] = pd.qcut(data["RFM_Score"],
                                q=5,
                                labels=segment_label)
#print(data[["CustomerID", "Location", "RFM_Score", "Value Segment"]].to_string())
print(data)

segment_counts = data["Value Segment"].value_counts().reset_index()
segment_counts.columns = ["Value Segment", "Count"]
print(segment_counts)
pastel_colors = px.colors.qualitative.Pastel

fig_segment_dist = px.bar(segment_counts,
                          x="Value Segment",
                          y="Count",
                          color="Value Segment",
                          color_discrete_sequence=pastel_colors,
                          title="RFM value segment distribution")
#fig_segment_dist.update_layout(xaxis)
fig_segment_dist.show()

data["RFM Customer Segments"] = ""
data.loc[data["RFM_Score"] >= 9, "RFM Customer Segments"] = "Champions"
data.loc[(data["RFM_Score"] >= 6) & (data["RFM_Score"] < 9), "RFM Customer Segments"] = "Potential loyalists"
data.loc[(data["RFM_Score"] >= 5) & (data["RFM_Score"] < 6), "RFM Customer Segments"] = "At risk customers"
data.loc[(data["RFM_Score"] >= 4) & (data["RFM_Score"] < 5), "RFM Customer Segments"] = "Can't lose"
data.loc[data["RFM_Score"] < 4, "RFM Customer Segments"] = "Lost"
print(data[["CustomerID", "RFM_Score", "RFM Customer Segments"]])


#Now let’s analyze the distribution of RFM values 
# within the Champions segment:
champions_segment = data[data["RFM Customer Segments"] == "Champions"]
print(champions_segment)

fig = go.Figure()
fig.add_trace(go.Box(y=champions_segment["RecencyScore"], name="Recency"))
fig.add_trace(go.Box(y=champions_segment["FrequencyScore"], name="Frequency"))
fig.add_trace(go.Box(y=champions_segment["MonetaryScore"], name="Monetary"))
fig.update_layout(title="Distribution of the RFM values within Champions",
                  yaxis_title="RFM value",
                  showlegend=True)
fig.show()


#let’s analyze the correlation of the recency, frequency, 
# and monetary scores within the champions segment:
correlation_matrix = champions_segment[["RecencyScore", "FrequencyScore", "MonetaryScore"]].corr()
fig_heatmap = go.Figure(data=go.Heatmap(z = correlation_matrix.values,
                                        x = correlation_matrix.columns,
                                        y = correlation_matrix.columns,
                                        colorscale="RdBu",
                                        colorbar=dict(title="Correlation")))
fig_heatmap.update_layout(title="Correlation matrix of RFM value within Champion segment")
fig_heatmap.show()


#Now let’s have a look at the number of customers in all the segments:
pastel_colors = plotly.colors.qualitative.Pastel
segment_counts = data.groupby("RFM Customer Segments")["CustomerID"].count().reset_index()
print(segment_counts)
segment_counts = data["RFM Customer Segments"].value_counts()
print(segment_counts)

fig = go.Figure(data=[go.Bar(x=segment_counts.index,
                             y=segment_counts.values,
                             marker=dict(color=pastel_colors))])
champions_color = "rgb(158, 202, 225)"
fig.update_layout(title="Comparison of RFM segments",
                  xaxis_title="RFM segments",
                  yaxis_title="Number of customers",
                  showlegend=False)
fig.show()


