import pandas as pd
import numpy as np
import plotly.express as px


#1. get raw data
movies = pd.read_csv("24_movies.dat", delimiter="::")
movies.columns = ["ID", "Title", "Genre"]
#print(movies)

#print(movies.info())
#print(movies.describe())
#print(movies.isnull().sum())

ratings = pd.read_csv("24_ratings.dat", delimiter="::")
ratings.columns = ["User", "ID", "Ratings", "Timestamp"]
#print(ratings)


#2. merge raw data
data = pd.merge(movies, ratings, on=["ID", "ID"])
#print(data)

#data_temp = movies.merge(ratings, on="ID")
#print(data_temp)


#3. two ways of making the same graphic
ratings = data["Ratings"].value_counts()

numbers = ratings.index
quantity = ratings.values
fig = px.pie(data,
             names=numbers,
             values=quantity)
#fig.show()

df_ratings = pd.DataFrame(ratings)
df_ratings = df_ratings.reset_index()
df_ratings.columns = ["Rating", "Total"]

fig = px.pie(df_ratings,
             values="Total",
             names="Rating")
#fig.show()


#4. two different ways to filter data
data2 = data.query("Ratings == 10")
#print(data2.head())

data2 = data.loc[data["Ratings"] == 10]
#print(data2.head())

data2 = data2["Title"].value_counts()
data2 = pd.DataFrame(data2).reset_index()
data2.columns = ["Title", "Count"]
#print(data2)

data2_asc = data2.sort_values(ascending=True, by="Count")
data2_des = data2.sort_values(ascending=False, by="Count")
#print(data2_asc.head(20))
#print(data2_des.head(20))


#5. chart about genres
#data_ = data.query("Genre='Animation|Adventure|Drama|Horror|Sci-Fi'")
data_ = data.loc[data["Genre"] == "Animation|Adventure|Drama|Horror|Sci-Fi"]
#print(data_)

genre_stas = pd.DataFrame(data["Genre"].value_counts())
genre_stas = genre_stas.reset_index()
genre_stas.columns = ["Genre", "Total"]
#print(genre_stas)

fig = px.bar(genre_stas.head(10),
             x="Genre",
             y="Total",
             title="Total movies by Genre")
#fig.update_layout(xtitle="")
#fig.show()

avg_rating_genre = data[["Genre", "Ratings"]]
avg_rating_genre = avg_rating_genre.groupby("Genre")["Ratings"].mean().reset_index()
avg_rating_genre["Ratings"] = avg_rating_genre["Ratings"].round(2)
avg_desc = avg_rating_genre[avg_rating_genre["Ratings"] < 10]
avg_desc = avg_desc.sort_values(ascending=False,
                                by="Ratings")
avg_desc = avg_desc.head(10)
print(avg_desc.head(20))

fig = px.bar(avg_desc,
             x="Genre",
             y="Ratings",
             title="Average Rating by Genre")
fig.show()


