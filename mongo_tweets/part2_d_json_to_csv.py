#converting the Twitter json dump in MongoDB to CSV using PyMongo
from pymongo import MongoClient
from operator import itemgetter
import csv
import os

db = MongoClient().usa_db

if os.path.exists('usa_tweets.csv'):
    os.remove('usa_tweets.csv')
with open('usa_tweets.csv', 'w',newline='',encoding='UTF-8') as outfile:
  field_names = ['text', 'user', 'created_at', 'lat','lon']
  writer = csv.DictWriter(outfile, delimiter=',', fieldnames=field_names)
  writer.writeheader()

  for data in db.usa_tweets_collection.find():
    # try:
      coordinates=(data['geo']['coordinates'])
      # print(coordinates[1])
      # break
      writer.writerow({
        'text': data['text'],
        'user': data['user'],
        'created_at': data['created_at'],
        'lat': coordinates[0],
        'lon': coordinates[1] })
    # except:
      print(data)



  outfile.close()