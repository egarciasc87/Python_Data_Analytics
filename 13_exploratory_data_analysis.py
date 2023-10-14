import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from wordcloud import WordCloud
pio.templates.default = "plotly_white"


#1. get raw data
file_name = "13_exploratory_data_analysis.csv"
data = pd.read_csv(file_name, encoding="latin-1")
print(data.head())
#print(data.describe())
#print(data.isnull().sum())
#print(data.info())
print(data.columns)


#2. some stats aboud 'impressions'
fig = px.histogram(data,
                   x="Impressions",
                   nbins=10,
                   title="Distribution of Impressions")
#fig.show()

#data["Total"] = data["From Home"] + data["From Hashtags"] + data["From Explore"] + data["From Other"]
#print(data[["Impressions", "From Home", "From Hashtags", "From Explore", "From Other", "Total"]])

fig = px.line(data,
              x=data.index,
              y="Impressions",
              title="Impressions over time")
#fig.show()


#3. metrics about likes, saves, and follows
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index,
                         y=data["Likes"],
                         name="Likes"))
fig.add_trace(go.Scatter(x=data.index,
                         y=data["Saves"],
                         name="Saves"))
fig.add_trace(go.Scatter(x=data.index,
                         y=data["Follows"],
                         name="Follows"))
fig.update_layout(title="Metrics Over Time",
                  xaxis_title="Date",
                  yaxis_title="Count")
#fig.show()

reach_sources = ["From Home", "From Hashtags", "From Explore", "From Other"]
reach_counts = [data[source].sum() for source in reach_sources]

data_reach_sources = pd.DataFrame()
data_reach_sources["Source"] = reach_sources
data_reach_sources["Counts"] = reach_counts
print(data_reach_sources)

colors = ['#FFB6C1', '#87CEFA', '#90EE90', '#FFDAB9']
fig = px.pie(data_frame=data_reach_sources,
             names="Source",
             values="Counts",
             color_discrete_sequence=colors)
fig.update_layout(title="Reach from different sources")
fig.update_traces(textposition="inside",
                  textinfo="percent+label")
#fig.show()

engagement_sources = ["Saves", "Comments", "Shares", "Likes"]
engagement_counts = [data[metric].sum() for metric in engagement_sources]

data_engagement_sources = pd.DataFrame()
data_engagement_sources["Metric"] = engagement_sources
data_engagement_sources["Counts"] = engagement_counts
print(data_engagement_sources)

fig = px.pie(data_frame=data_engagement_sources,
             names="Metric",
             values="Counts",
             color_discrete_sequence=colors,
             title="Engagement Sources")
fig.update_traces(textposition="inside",
                  textinfo="percent+label")
#fig.show()


#4. relationship between profile visits and follows
fig = px.scatter(data,
                 x="Profile Visits",
                 y="Follows",
                 trendline="ols",
                 title="Profile Visits vs Follows")
#fig.show()

hashtags = ' '.join(data["Hashtags"].astype(str))
wordcloud = WordCloud().generate(hashtags)
#print(hashtags)
#print(type(hashtags))

fig = px.imshow(wordcloud,
                title="Hashtags Word Cloud")
#fig.show()


corr_matrix = data.corr()
print(corr_matrix)

fig = go.Figure(data=go.Heatmap(x=corr_matrix.columns,
                                y=corr_matrix.index,
                                z=corr_matrix.values,
                                colorscale="RdBu",
                                zmin=-1,
                                zmax=1))
fig.update_layout(title="Correlation Matrix",
                  xaxis_title="Features",
                  yaxis_title="Features")
#fig.show()


#5. hastags analysis
all_hashtags = []
count = 0
for row in data["Hashtags"]:
    #count += 1
    #print(count)
    hashtags = str(row).split()
    hashtags = [tag.strip() for tag in hashtags]
    #print(hashtags)
    all_hashtags.extend(hashtags)

#print(all_hashtags)
hashtags_distribution = pd.Series(all_hashtags).value_counts().reset_index()
hashtags_distribution.columns = ["Hashtags", "Count"]
print(hashtags_distribution[hashtags_distribution.Count > 10])

fig = px.bar(hashtags_distribution[hashtags_distribution.Count > 10],
             x="Hashtags",
             y="Count",
             title="Distribution of Hashtags")
fig.show()





