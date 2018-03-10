from pymongo import MongoClient
import re
from textblob import TextBlob

client = MongoClient('localhost', 27017)
database_obj = client['twitterdb']
collection_obj = database_obj['twitter_search']
all_tweets = collection_obj.find()

for tweets in all_tweets:
    if re.search('(?<=(?<=(?<=d)a)t)a', tweets['text'], re.IGNORECASE) is not None:
        blob = TextBlob(tweets['text'])
        for sentence in blob.sentences:
            if sentence.sentiment.polarity < 0:
                print("Negative  | "+str(sentence))
            elif sentence.sentiment.polarity > 0:
                print("Positive | "+str(sentence))
            else:
                print("Neutral  | "+str(sentence))