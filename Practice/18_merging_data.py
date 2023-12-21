import numpy as np
import pandas as pd
import os
import plotly.express as px


#1. generate raw data
table1 = pd.DataFrame({"P_ID" : (1,2,3,4,5,6,7,8),
                     "gender" : ("male", "male", "female","female",
                                "female", "male", "female", "male"),
                     "height" : (71,73,64,64,66,69,62,72),
                     "weight" : (175,225,130,125,165,160,115,250)})
table2 = pd.DataFrame({"P_ID" : (1, 2, 4, 5, 7, 8, 9, 10),
                     "sex" : ("male", "male", "female","female",
                            "female", "male", "male", "female"),
                     "visits" : (1,2,4,12,2,2,1,1),
                     "checkup" : (1,1,1,1,1,1,0,0),
                     "follow_up" : (0,0,1,2,0,0,0,0),
                     "illness" : (0,0,2,7,1,1,0,0),
                     "surgery" : (0,0,0,2,0,0,0,0),
                     "ER" : ( 0,1,0,0,0,0,1,1) } ) 
table1.rename(columns={"gender": "sex"},
              inplace=True)
print(table1)
print(table2)


#2. merge data
data_inner_join = pd.merge(table1,
                     table2,
                     how="inner",
                     on="P_ID")
print("\ninner join: \n", data_inner_join)

data_left_join = pd.merge(table1,
                          table2,
                          how='left',
                          on='P_ID')
print("\nleft join: \n", data_left_join)

data_right_join = pd.merge(table1,
                           table2,
                           how='right',
                           on='P_ID')
print("\nright join: \n", data_right_join)

data_outer_join = pd.merge(table1,
                           table2,
                           how='outer',
                           on=["P_ID", "sex"])
print("\nouter join: \n", data_outer_join)


#3. some graphics
data_height = data_outer_join.groupby("sex")["height"].mean().reset_index()
print(data_height)

fig = px.bar(data_height,
             x="sex",
             y="height",
             title="Average height by sex")
#fig.show()

data_weight = data_outer_join.groupby("sex")["weight"].mean().reset_index()
#data_weight["weight_kg"] = data_weight["weight"]/2.2
print(data_weight)

fig = px.bar(data_weight,
             x="sex",
             y="weight",
             title="Average weight by sex")
#fig.show()

data_sex = data_outer_join.groupby("sex")["height"].count().reset_index()
data_sex = data_sex.rename(columns={"height": "total"})
print(data_sex)

fig = px.pie(data_sex,
             values="total",
             names="sex",
             title="Total people by sex")
fig.show()


