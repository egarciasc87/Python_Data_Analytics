import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_white"


#1. get raw data
file_name = "15_user_funnel_analysis.csv"
data = pd.read_csv(file_name)
print(data)
#print(data.info())
#print(data.isnull().sum())
#print(data.describe())


#2. conversions stats
data_pivot = pd.pivot_table(data,
                            index="stage",
                            columns="conversion",
                            values="conversion",
                            aggfunc="count")
#data_pivot = data_pivot.fillna(0)
data_pivot = data_pivot.replace(np.nan, 0)
print("pivot table: \n", data_pivot)

data["count"] = data["conversion"]
data_group = data.groupby(["stage", "conversion"])["count"].count().reset_index()
print("group table: \n", data_group)
#print(data[data.stage == "homepage"])

print(data["stage"].value_counts())


#3. stages analysis
funnel_stages = ["homepage", "product_page", "cart", "checkout", "purchase"]
num_users = []
num_conversions = []

for stage in funnel_stages:
    stage_users = data[data["stage"] == stage]
    num_users.append(len(stage_users))
    num_conversions.append(stage_users["conversion"].sum())

#print(funnel_stages)
#print(num_users)
#print(num_conversions)

data_num_user_conve_1 = pd.DataFrame()
data_num_user_conve_1["stage"] = funnel_stages
data_num_user_conve_1["# users"] = num_users
data_num_user_conve_1["# conversions"] = num_conversions
print("# of users and conversions (method 1): \n", data_num_user_conve_1)

data_num_user = data.groupby("stage")["user_id"].count().reset_index()
data_num_conv = data.groupby("stage")["conversion"].sum().reset_index()
data_num_user_conv_2 = data_num_user.merge(data_num_conv, on="stage")
data_num_user_conv_2.columns = ["stage", "# users", "# conversions"]
print("# of users and conversions (method 2): \n", data_num_user_conv_2)


fig = go.Figure(go.Funnel(y=funnel_stages,
                          x=num_users,
                          textposition="inside",
                          textinfo="value",
                          name="Users"))
fig.add_trace(go.Funnel(y=funnel_stages,
                        x=num_conversions,
                        textposition="inside",
                        textinfo="value",
                        name="Conversions"))
fig.update_layout(title="Funnel Analysis",
                  funnelmode="stack")
fig.show()


