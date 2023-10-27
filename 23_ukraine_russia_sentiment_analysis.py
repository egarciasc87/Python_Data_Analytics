import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS
import nltk
import re
from nltk.corpus import stopwords
import string


#1. get raw data
file_name = "23_ukraine_russia_sentiment_analysis.csv"
data = pd.read_csv(file_name)

#print(data)
#print(data.columns)
null_columns = pd.DataFrame(data.isnull().sum()).reset_index()
null_columns.columns = ["column", "total"]
#print(null_columns)
#print(null_columns.info())
null_columns = null_columns[null_columns.total >= 9000]
columns_delete = null_columns["column"].tolist()
data = data.drop(columns=columns_delete)
print(data.columns)


#2. get some stats for languages
data = data[["username", "tweet", "language"]]
#print(data)

data_language = pd.DataFrame(data["language"].value_counts()).reset_index()
data_language.columns = ["language", "total"]
data_language["language_other"] = np.where(data_language["total"] >= 100, data_language["language"], "other")
data_language_other = data_language.groupby("language_other")["total"].sum().reset_index()
data_language_other.columns = ["language", "total"]
#print(data_language)
print(data_language_other)

fig = px.bar(data_language[:5],
             x="language",
             y="total",
             title="TOP 100 languages per # of tweets")
#fig.show()

fig = px.bar(data_language_other,
             x="language",
             y="total",
             title="TOP 100 languages per # of tweets")
#fig.show()


#3. transform data about tweets
#print(data)
nltk.download("stopwords")
stemmer = nltk.SnowballStemmer("english")
stopword = set(stopwords.words("english"))

def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(" ") if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(" ")]
    text = " ".join(text)
    return text

data["tweet"] = data["tweet"].apply(clean)
print(data.head())

text = " ".join(i for i in data.tweet)
#print(text)
stopwords = set(STOPWORDS)
worldcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
plt.figure(figsize=(15,10))
plt.imshow(worldcloud, interpolation="bilinear")
plt.axis("off")
#plt.show()

nltk.download('vader_lexicon')
sentiments = SentimentIntensityAnalyzer()
data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["tweet"]]
data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["tweet"]]
data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["tweet"]]
data = data[["tweet", "Positive", "Negative", "Neutral"]]
print(data.head())


