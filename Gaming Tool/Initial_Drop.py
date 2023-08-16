# -*- coding: utf-8 -*-
"""
Spyder Editor
Author: Satyajit Bhuyan <satyajit.bhuyan@intel.com>
This script ingests cfx csv file and spits
This is a temporary script file.
"""
import pandas as pd
import math
from tabulate import tabulate
import json
#ingest csv file | json do later
f = open(r'Farcry4.json')
data = json.load(f)

dict1={}

for i in data['Runs']:
    c = i['CaptureData']
    for i, j in c.items():
        dict1[i] = j

#Main DataFrame
df = pd.DataFrame(dict1)
df.sort_values(by=['MsBetweenPresents'], ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)


# Calculate statistics
application_name = df.iloc[0,0]
total_game_time = df['TimeInSeconds'].max()
time_1plow= (0.01*total_game_time*1000)
time_0p1plow = 0.001*total_game_time*1000
count_1plow = math.ceil(0.01*len(df))
count_0p1plow = math.ceil(0.001*len(df))
mean_frame_time = df['MsBetweenPresents'].mean()
min_frame_time = df['MsBetweenPresents'].min()
max_frame_time = df['MsBetweenPresents'].max()
P99_frame_time = df['MsBetweenPresents'].quantile(q=0.99)
P95_frame_time = df['MsBetweenPresents'].quantile(q=0.95)
P5_frame_time = df['MsBetweenPresents'].quantile(q=0.05)
P1_frame_time = df['MsBetweenPresents'].quantile(q=0.01)

series = df['MsBetweenPresents']

# Calculate 1% and 0.1% low integral
def lowavgintegral(time_1plow):
    running_sum=0
    index=-1
    for MsBetweenPresents in series:
        running_sum += MsBetweenPresents
        index=index+1
        if running_sum > time_1plow:
            break
    lowavg=round(1000/series[index], 3)
    return lowavg
# Calculate 1% and 0.1% low integral
def lowavg(count_1plow):

        lowavg = round(1000/series.head(count_1plow).mean(),3)
        return lowavg


table_data = [
    ("Game Name:", application_name),
    ("Total Gameplay Time:", 1000 * total_game_time),
    ("Avg fps:", round(1000 / mean_frame_time, 3)),
    ("Max fps:", round(1000 / min_frame_time, 3)),
    ("Min fps:", round(1000 / max_frame_time, 3)),
    ("P1 fps:", round(1000 / P99_frame_time, 3)),
    ("P5 fps:", round(1000 / P95_frame_time, 3)),
    ("P95 fps:", round(1000 / P5_frame_time, 3)),
    ("P99 fps:", round(1000 / P1_frame_time, 3)),
    ("1% low integral fps:", lowavgintegral(time_1plow)),
    ("0.1% low integral fps:", lowavgintegral(time_0p1plow)),
    ("1% low avg fps:", lowavg(count_1plow)),
    ("0.1% low avg fps:", lowavg(count_0p1plow))
]

table = tabulate(table_data, tablefmt='fancy_grid')
print(table)

import matplotlib.pyplot as plt

# Your graph_data here
graph_data = [
    ("Avg fps:", round(1000 / mean_frame_time, 3)),
    ("Max fps:", round(1000 / min_frame_time, 3)),
    ("Min fps:", round(1000 / max_frame_time, 3)),
    ("P1 fps:", round(1000 / P99_frame_time, 3)),
    ("P5 fps:", round(1000 / P95_frame_time, 3)),
    ("P95 fps:", round(1000 / P5_frame_time, 3)),
    ("P99 fps:", round(1000 / P1_frame_time, 3)),
    ("1% low integral fps:", lowavgintegral(time_1plow)),
    ("0.1% low integral fps:", lowavgintegral(time_0p1plow)),
    ("1% low avg fps:", lowavg(count_1plow)),
    ("0.1% low avg fps:", lowavg(count_0p1plow))
]

# Extract labels and values from graph_data
labels = [item[0] for item in graph_data]
values = [item[1] for item in graph_data]

# Create the bar graph
plt.figure(figsize=(10, 6))
bars = plt.barh(labels, values, color='skyblue')
plt.xlabel('Frames per seconds')
plt.ylabel('Metrics')
plt.title('Game Performance Metrics')

# Annotate bars with values
for bar, value in zip(bars, values):
    plt.text(value, bar.get_y() + bar.get_height() / 2, str(value), va='center', color='black')

# Show the plot
plt.show()

