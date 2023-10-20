import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
pio.templates.default = "plotly_white"


#1. get raw data
file_name = "18_t20_world_cup_2022.csv"
data = pd.read_csv(file_name)
print(data)
#print(data.isnull().sum())
print(data.columns)


#2. some graphs ans stats
data_wins = data.groupby("winner")["venue"].count().reset_index()
data_wins.columns = ["winner", "# matches won"]
print("# matches won: \n", data_wins)

fig = px.bar(data,
             x="winner",
             title="Number of Matches Winned")
#fig.show()

data_won_by = data.groupby("won by")["winner"].count().reset_index()
data_won_by.columns = ["won by", "total"]
print("# won by: \n", data_won_by)

fig = px.pie(data_won_by,
             names="won by",
             values="total",
             hole=0.5,
             color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_traces(textinfo="percent+label",
                  textposition="inside")
fig.update_layout(title="Won by: wickets vs runs")
#fig.show()

toss = data["toss decision"].value_counts()
label = toss.index,
counts = toss.values
colors = ["skyblue", "yellow"]
#print(toss)
#print(label)
#print(counts)
#print(type(toss))
data_toss_decision = pd.DataFrame(toss).reset_index()
data_toss_decision.columns = ["toss decision", "total"]

fig = px.pie(data_toss_decision, 
             names="toss decision",
             values="total",
             color_discrete_sequence=colors,
             hole=0.5)
fig.update_traces(textinfo="percent+label",
                  textposition="inside")
fig.update_layout(title="Toss Decisions in t20 World Cup 2022")
#fig.show()

data_top_scorers = pd.DataFrame(data["top scorer"].value_counts()).reset_index()
data_top_scorers.columns = ["scorer", "total"]
print("# times top scorer: \n", data_top_scorers)

fig = px.bar(data,
             x="top scorer",
             y="highest score",
             color="highest score",
             title="Top Scorers in t20 Wordl Cup 2022")
#fig.show()

fig = px.bar(data,
             x="player of the match",
             title="Times Player of the Match")
#fig.show()

fig = px.bar(data,
             x="best bowler",
             title="Best Bowler in t20 World Cup 2022")
#fig.show()


#3. innings statistics
fig = go.Figure()
fig.add_trace(go.Bar(x=data["venue"],
                     y=data["first innings score"],
                     name="First Innings Score",
                     marker_color="blue"))
fig.add_trace(go.Bar(x=data["venue"],
                     y=data["second innings score"],
                     name="Second Innings Score",
                     marker_color="red"))
fig.update_layout(title="Best Stadium to Bat First or Chase",
                  barmode="group")
fig.show()


fig = go.Figure()
fig.add_trace(go.Bar(x=data["venue"],
                     y=data["first innings wickets"],
                     name="First Innings Wickets",
                     marker_color="blue"))
fig.add_trace(go.Bar(x=data["venue"],
                     y=data["second innings wickets"],
                     name="Second Innings Wickets",
                     marker_color="red"))
fig.update_layout(title="Best Stadiums to Bowl or Defend",
                  barmode="group")
fig.show()
