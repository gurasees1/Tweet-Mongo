from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost/usa_db'  # assuming you have mongoDB installed locally
# and a database called 'twitterdb'


keys_file = open("keys.txt")
lines = keys_file.readlines()
consumer_key = lines[0].rstrip()
consumer_secret = lines[1].rstrip()
access_token = lines[2].rstrip()
access_token_secret = lines[3].rstrip()
no_of_tweets=0
class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        # This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)

            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.usa_db

            # Decode the JSON from Twitter
            datajson = json.loads(data)
          #  print(datajson)
            # grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']
            coordinatesField=str(datajson['coordinates'])
           # print(coordinatesField)
            # print out a message to the screen that we have collected a tweet
            #print("Tweet collected at " + str(created_at))
           # print(tweepy.Stream)
            # insert the data into the mongoDB into a collection called twitter_search
            # if twitter_search doesn't exist, it will be created.
            if coordinatesField!="None":
                db.usa_tweets_collection.insert(datajson)
                no_of_tweets=db.usa_tweets_collection.find().count()
                print("No of Records in DB="+str(no_of_tweets))
                if no_of_tweets>9999:
                    return False
        except Exception as e:
            print(e)

client = MongoClient(MONGO_HOST)
db = client.usa_db
initial_no_of_tweets=db.usa_tweets_collection.find().count()

if(initial_no_of_tweets<10000):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
    listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
    streamer = tweepy.Stream(auth=auth, listener=listener)
    streamer.filter(locations=[-125,25,-65,48])

print("Collection Stopped:No of tweets in db="+str(initial_no_of_tweets))