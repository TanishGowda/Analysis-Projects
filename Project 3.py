# -*- coding: utf-8 -*-
"""
Created on Tue May  6 22:44:08 2025

@author: tanis
"""

import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from textblob import TextBlob

df = pd.read_csv("chatgpt1.csv")

df.isna()
clean_df = df.dropna()

a = df['Text'][1]
lang = detect(a)

# Function to detect language

def det(x):
    try:
        lan = detect(x)
    except:
        lan = 'Other'
    return lan

df['Language'] = df['Text'].apply(det)
clean_df['Language'] = clean_df['Text'].apply(det)

try_df = df[df['Language']=='en']
df = df.loc[df['Language']=='en']
df = df.reset_index(drop=True)

# Cleaning text

df['Text'] = df['Text'].str.replace('https','')
df['Text'] = df['Text'].str.replace('http','')
df['Text'] = df['Text'].str.replace('t.co','')

# Sentiment Function

def get_sentiment(text):
    sentiment  = TextBlob(text).sentiment.polarity
    
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'

df['sentiment'] = df['Text'].apply(get_sentiment)

# Creating a WordCloud
comment_words = ''
stopwords = set(STOPWORDS)

for val in df.Text:
    val = str(val)
    tokens = val.split()
    comment_words = comment_words + " ".join(tokens)+ " "

wordcloud = WordCloud(width=500, height=900, background_color='black', stopwords=stopwords, min_font_size=10).generate(comment_words)

plt.figure(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis('off')
plt.tight_layout()
plt.show()

# Creating a Countplot

import seaborn as sns

sns.set_style('whitegrid')
plt.figure(figsize=(10,5))

sns.countplot(x='sentiment', data=df)
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.title('Sentiment Analysis Distribution')
plt.show()


