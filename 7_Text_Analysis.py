import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import spacy
from collections import defaultdict
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


#1. load row data
print("Hello world...")
nlp = spacy.load("en_core_web_sm")
file_name = "7_Text_Analysis.csv"
data = pd.read_csv(file_name, encoding="latin-1")
print(data.head())
#print(type(data))
#print(data.columns)


#2. create a graph about the frequency of words
titles_text = ' '.join(data["Title"])
#print(titles_text)
wordcloud = WordCloud(width=800, 
                      height=400, 
                      background_color='white').generate(titles_text)
#print(wordcloud)

fig = px.imshow(wordcloud,
                title="Word Cloud of Titles")
fig.update_layout(showlegend=False)
#fig.show()


#3. elaborate sentiment analysis
data["Sentiment"] = data["Article"].apply(
    lambda x: TextBlob(x).sentiment.polarity)
print(data.head())
fig = px.histogram(data,
                   x="Sentiment",
                   title="Sentiment Distribution")
#fig.show()


#4. calculate Named Entity Recognition (NER)
def extract_named_entities(text):
    doc = nlp(text)
    entities = defaultdict(list)

    for ent in doc.ents:
        entities[ent.label_].append(ent.text)
    return dict(entities)

data["Named_Entities"] = data["Article"].apply(extract_named_entities)
#print(data)


entity_counts = Counter(
    entity for entities in data['Named_Entities'] for entity in entities)
entity_df = pd.DataFrame.from_dict(entity_counts, 
                                   orient='index').reset_index()
entity_df.columns = ['Entity', 'Count']
print(entity_df)

fig = px.bar(entity_df.head(7),
             x="Entity",
             y="Count",
             title="Top 7 Named Entities")
#fig.show()


#5. perform topic modeling
vectorizer = CountVectorizer(max_df=0.95, 
                             min_df=2, 
                             max_features=1000, 
                             stop_words='english')
tf = vectorizer.fit_transform(data['Article'])
lda_model = LatentDirichletAllocation(n_components=5, random_state=42)
lda_topic_matrix = lda_model.fit_transform(tf)

topic_names = ["Topic " + str(i) for i in range(lda_model.n_components)]
data['Dominant_Topic'] = [topic_names[i] for i in lda_topic_matrix.argmax(axis=1)]

fig = px.bar(data['Dominant_Topic'].value_counts().reset_index(), 
             x='index', 
             y='Dominant_Topic', 
             title='Topic Distribution')
fig.show()


