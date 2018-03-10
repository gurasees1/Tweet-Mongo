from pymongo import MongoClient
import re

client = MongoClient('localhost', 27017)
database_object = client['twitterdb']
collection_obj = database_object['twitter_search']
all_tweets = collection_obj.find()
count_geo_enabled = 0
for tweets in all_tweets:
    if re.search('(?<=(?<=(?<=d)a)t)a', tweets['text'], re.IGNORECASE) is not None:
        user = tweets['user']
        if user['geo_enabled']:
            count_geo_enabled += 1

print("Count of data related objects that are geo_enabled = ", count_geo_enabled)
