import folium
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

divvyStations_q3 = pd.read_csv('C:/Users/guras/PycharmProjects/mongo_tweets/usa_tweets.csv')
# divvyStations_q3=divvyStations_q3.head(10)
m = folium.Map([41.8781, -87.6298], zoom_start=5)

for index, row in divvyStations_q3.iterrows():
    folium.CircleMarker([row['lat'],row['lon']],
                        radius=3,
                        fill_color="#3db7e4", # divvy color
                       ).add_to(m)
m.save('part2_d_map.html')
print("Map has been saved in part2_d_map.html ")