import emoji
import os
import csv

from pymongo import MongoClient
emoji_dict={}

def extract_count_emojis(str,state):
    regex =emoji.get_emoji_regexp()
    emojis=regex.findall(str)
    if len(emojis)!=0:
        for emo in emojis:
            #print(emo)
            if(emoji_dict.__contains__(emo)):
                emoji_dict[emo]=emoji_dict[emo]+1
            else:
                emoji_dict[emo]=1
        if statesdict.__contains__(state):
            state_emoji_dict=statesdict.get(state)
            for emo in emojis:
                # print(emo)
                if (state_emoji_dict.__contains__(emo)):
                    state_emoji_dict[emo] = state_emoji_dict[emo] + 1
                else:
                    state_emoji_dict[emo] = 1
            statesdict[state]=state_emoji_dict
        else:
            statesdict[state]={}
            state_emoji_dict={}
            for emo in emojis:
                # print(emo)
                if (state_emoji_dict.__contains__(emo)):
                    state_emoji_dict[emo] = state_emoji_dict[emo] + 1
                else:
                    state_emoji_dict[emo] = 1
            statesdict[state]=state_emoji_dict



state_coordinate_dict={}
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
setStates=set(states)
statesdict={}


MONGO_HOST = 'mongodb://localhost/usa_db'  # assuming you have mongoDB installed locally
# and a database called 'twitterdb'

client = MongoClient(MONGO_HOST)
db = client.usa_db
fetched_tweets=db.usa_tweets_collection.find().limit(10000)
for tweet in fetched_tweets:
    tweet_text=tweet['text']
    try:
        tweet_fullname=tweet['place']['full_name']
        tweet_state_array=str(tweet_fullname).split(",")
        tweet_state=tweet_state_array.pop().strip()
        tweet_coordinates=tweet['geo']['coordinates']

    except:
        count=0

    if tweet_state not in setStates:
        if tweet_state=="USA":
            tweet_state=tweet_state_array.pop()
            states.append(tweet_state)

    else:
        extract_count_emojis(tweet_text,tweet_state)
    state_coordinate_dict[tweet_state] = tweet_coordinates
# print(state_coordinate_dict)
from operator import itemgetter
rlist=(sorted(emoji_dict.items(), key=itemgetter(1),reverse=True))

print("Top 15 Emoji's Used are as below:")
print(rlist[:15])
print("Top 5 states for emoji '🎄' are:")
top5dict={}
for state in statesdict:
    try:
        state_count=(statesdict[state]['🎄'])
        top5dict[state]=state_count
    except:
        count=0
top5tree_sorted=(sorted(top5dict.items(), key=itemgetter(1),reverse=True))
print(top5tree_sorted[:5])
print("Top 5 emojis for MA are:")
MA_list=statesdict['MA']
ma_list_sorted=(sorted(MA_list.items(), key=itemgetter(1),reverse=True))
print(ma_list_sorted[:5])

print("Top 5 states that use emojis are")
top5Count_dict={}
for state in statesdict:
    count=0
    try:
        for emo_count in statesdict[state]:
            count=count+(statesdict[state][emo_count])
        top5Count_dict[state]=count
    except:
        count2=0

top5Count_sorted=(sorted(top5Count_dict.items(), key=itemgetter(1),reverse=True))
print(top5Count_sorted[:5])

state_top_2_dict={}
for state in statesdict:
    state_sorted=(sorted(statesdict[state].items(), key=itemgetter(1),reverse=True))
    # print(str(state)+":"+str(state_sorted[:2]))
    # break
    state_top_2_dict[state]=state_sorted[:2]
print("Top 2 emoji's for each state are listed below,these can be plotted on a map using show_map_extra_credit.py")
print(state_top_2_dict)

import random
def write_state_emoji_csv():
    if os.path.exists('usa_top_emoji_tweets.csv'):
        os.remove('usa_top_emoji_tweets.csv')
    with open('usa_top_emoji_tweets.csv', 'w', newline='', encoding='UTF-8') as outfile:
        field_names = ['text', 'lat', 'lon']
        writer = csv.DictWriter(outfile, delimiter=',', fieldnames=field_names)
        writer.writeheader()
        for state in state_top_2_dict:

            coordinates=state_coordinate_dict[state]
            for emoji in state_top_2_dict[state]:
                    rand =random.uniform(0, 1)
                    text=str(emoji[0])
                    writer.writerow({
                     'text': text,
                     'lat': coordinates[0]+rand,
                     'lon': coordinates[1]+rand})



        outfile.close()

write_state_emoji_csv()