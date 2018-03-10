import folium
import pandas as pd


csv_data = pd.read_csv('C:/Users/guras/PycharmProjects/mongo_tweets/usa_top_emoji_tweets.csv')
m = folium.Map([41.8781, -87.6298], zoom_start=4)
count=0
for index, row in csv_data.iterrows():
    if count==0:
        folium.Marker([row['lat'],row['lon']],popup=row['text'],
                        icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
        count=count+1;
    else:
        folium.Marker([row['lat'], row['lon']], popup=row['text'],
                      icon=folium.Icon(color='green', )).add_to(m)
        count=count-1;
m.save('top_2_emoji_state.html')
print("Map has been saved in top_2_emoji_state.html")

