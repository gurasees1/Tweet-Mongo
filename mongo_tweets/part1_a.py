from pymongo import MongoClient
import re

client = MongoClient('localhost', 27017)
database_obj = client['twitterdb']
collection_obj = database_obj['twitter_search']
all_tweets = collection_obj.find()
count_data = 0

for tweets in all_tweets:
    if re.search('(?<=(?<=(?<=d)a)t)a', tweets['text'], re.IGNORECASE) is not None:
        count_data =count_data+1

print("Count of Tweets that contain data somewhere in their text = ", count_data)
