# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 16:23:23 2019

@author: taha
"""
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#list all files
list_files = glob.glob('./Performance Counters/*.csv')
latest_file = max(list_files, key=os.path.getctime)
print latest_file
# read csv file

df = pd.read_csv(latest_file)

df.rename(columns= {
        '(PDH-CSV 4.0) (Maroc (heure d': 'created_at'
        
        }, inplace=True)
df.rename(
        columns= lambda x: x.split('\\')[-1].replace(" ", "_").replace("/","_"), inplace= True
    

        )
# Data type conversions
#df['created_at'] = df['created_at'].astype('datetime64[ns]')

    

print df.head(20)
df.groupby(df["created_at"].astype('datetime64[ns]').dt.day).count().plot(kind="bar")

kk =[]
for mm in df['created_at']:
    k=mm.split(" ",1)
    kk.append(k[1])
print(kk)
x = kk
y = df['thread_count']
f, ax = plt.subplots(figsize=(18,5))
plt.bar(x,y, align='center') # A bar chart
plt.xlabel('TimeLine (secondes)')
plt.ylabel('threads count')
plt.show()

# plot a line
x = kk
y = df['%_user_time']
f, ax = plt.subplots(figsize=(18,5))
plt.plot(x,y)
plt.yscale('linear')
plt.xlabel('TimeLine (secondes)')
plt.ylabel('CPU Usage %')

