from pymongo import MongoClient
from operator import itemgetter

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
setStates=set(states)
statesdict={}
citydict={}

MONGO_HOST = 'mongodb://localhost/usa_db'  # assuming you have mongoDB installed locally
# and a database called 'usa_db'

client = MongoClient(MONGO_HOST)
db = client.usa_db
fetched_tweets=db.usa_tweets_collection.find()

for tweet in fetched_tweets:
    try:
        tweet_fullname=tweet['place']['full_name']
        tweet_state_array=str(tweet_fullname).split(",")
        tweet_state=tweet_state_array.pop().strip( )
        tweet_city=tweet['place']['name']
    except:
        count=0

    if tweet_state not in setStates:
        if tweet_state=="USA":
            tweet_state=tweet_state_array.pop()
            states.append(tweet_state)
    if tweet_state == 'CA':
        if citydict.__contains__(tweet_city):
            citydict[tweet_city] += 1
        else:
            citydict[tweet_city] = {}
            citydict[tweet_city] = 1

    if statesdict.__contains__(tweet_state):
        statesdict[tweet_state] += 1
    else:
        statesdict[tweet_state] = {}
        statesdict[tweet_state] = 1

print("Top 5 states that have tweets are")
top5_sorted=(sorted(statesdict.items(), key=itemgetter(1),reverse=True))
print(top5_sorted[:5])

print("In the state of California, the top 5 cities that tweet are")
top5_sorted=(sorted(citydict.items(), key=itemgetter(1),reverse=True))
print(top5_sorted[:5])
