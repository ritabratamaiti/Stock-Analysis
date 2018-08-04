# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 01:18:55 2018

@author: Ritabrata Maiti
"""

from easygui import *
import sys

# A nice welcome message
ret_val = msgbox("Dashboard Configuration Wizard")
if ret_val is None: # User closed msgbox
    sys.exit(0)

import time
import threading
try:
    import Tkinter as tkinter
    import ttk
except ImportError:
    import tkinter
    from tkinter import ttk


class GUI(object):

    def __init__(self):
        self.root = tkinter.Tk()

        self.progbar = ttk.Progressbar(self.root)
        self.progbar.config(maximum=500, mode='determinate')
        self.progbar.pack()
        self.root.geometry("500x50") 
        self.root.resizable(0, 0) 

        self.i = 0
        self.b_start = ttk.Button(self.root, text='Start sentiment analysis')
        self.b_start['command'] = self.start_thread
        self.b_start.pack()

    def start_thread(self):
        self.b_start['state'] = 'disable'
        self.work_thread = threading.Thread(target=work) 
        self.work_thread.start()
        self.root.after(50, self.check_thread)
        self.root.after(50, self.update)

    def check_thread(self):
        if self.work_thread.is_alive():
            self.root.after(50, self.check_thread)
        else:
            self.root.destroy()        


    def update(self):
        #Updates the progressbar
        self.progbar["value"] = self.i
        if self.work_thread.is_alive():
            self.root.after(50, self.update)#method is called all 50ms

gui = GUI()

def work():
    #Do your work :D
    # coding: utf-8
    
    # In[1]:
    
    
    from os import path
    import numpy as np
    import os
    from textblob import TextBlob
    from newsapi import NewsApiClient
    import pandas as pd
    
    
    # In[2]:
    
    
    api = NewsApiClient(api_key='')
    result = api.get_everything(q='Maruti Stock Price')
    
    
    # In[3]:
    
    
    values = {"positive": 0, "negative": 0, "neutral": 0}
    c = 0
    i = 0
    text = ''
    for art in result['articles']:
           
           analysis = TextBlob(art['title'] + art['description'])
    
           labels = []
           value = []
    
           
           sentiment_value = analysis.sentiment.polarity
           if sentiment_value >= -0.1 and sentiment_value <= 0.1:
               values['neutral'] += 1
           elif sentiment_value < 0:
               values['negative'] += 1
           elif sentiment_value > 0:
               values['positive'] += 1               
           
           for i in values:                   
               labels.append(i)
               value.append(values[i])     
    
    
    # In[4]:
    
    
    import plotly
    plotly.tools.set_credentials_file(username='', api_key='')
    
    
    # In[12]:
    
    
    import plotly.plotly as py
    import plotly.graph_objs as go
    
    colors = ['#2a843a','#e13838', '#158dd8']
    
    trace = go.Pie(labels=labels, values=value,
               hoverinfo='label+percent', textinfo='value', 
               textfont=dict(size=20),
               marker=dict(colors=colors))
    
    py.plot([trace], filename='Sentiment',  auto_open=False)  
    
    
    # In[42]:
    
    
    import tweepy           # To consume Twitter's API
    import pandas as pd     # To handle data
    import numpy as np      # For number computing
    
    
    
    
    # In[43]:
    
    
    
    # Consume:
    CONSUMER_KEY    = ''
    CONSUMER_SECRET = ''
    
    # Access:
    ACCESS_TOKEN  = ''
    ACCESS_SECRET = ''
    
    
    # In[44]:
    
    
    # We import our access keys:
       # This will allow us to use the keys as variables
    
    # API's setup:
    def twitter_setup():
        """
        Utility function to setup the Twitter's API
        with our access keys provided.
        """
        # Authentication and access using keys:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
        # Return API with authentication:
        api = tweepy.API(auth)
        return api
    
    
    # In[100]:
    
    
    # We create an extractor object:
    extractor = twitter_setup()
    
    # We create a tweet list as follows:
    tweets = extractor.search(q="Maruti Stock", count=200)
    
    
    
    
    # In[101]:
    
    
    # We create a pandas dataframe as follows:
    data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    
    
    
    
    # In[102]:
    
    # We add relevant data:
    data['len']  = np.array([len(tweet.text) for tweet in tweets])
    data['ID']   = np.array([tweet.id for tweet in tweets])
    data['Date'] = np.array([tweet.created_at for tweet in tweets])
    data['Source'] = np.array([tweet.source for tweet in tweets])
    data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
    data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
    
    
    # In[103]:
    
    
    
    # In[110]:
    
    
    from textblob import TextBlob
    import re
    
    
    # In[106]:
    
    
    
    
    
    # In[115]:
    
    
    sent = []
    for tweet in data['Tweets']:
            
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        analysis = TextBlob(tweet) 
        sent.append(analysis.sentiment.polarity*100)
    dat = [go.Scatter(x = data["Date"], y = sent, name='Sentiment'), go.Scatter( x= data['Date'], y=data['Likes'], name='No. of Likes' ), go.Scatter( x= data['Date'], y=data['RTs'], name='No. of retweets' )]    
    
    
    # In[116]:
    
    
    py.plot(dat, filename='semtiment_tweets',  auto_open=False)    
    for i in range(11):
        gui.i = i
        time.sleep(0.1)
    import quandl
    API = ''
    quandl.ApiConfig.api_key = API

    stock_list2 = ["SENSEX","BOM532500","SI1900","SI1400"]
    stock_dict2 = {}
    for coin in stock_list2:
        stock_dict2[coin] = quandl.get("BSE/"+str(coin), start_date="2016-12-01")
        
    frame2 = [ stock_dict2[name]['Close'] for name in stock_list2 ]
    #for name, item in stock_dict2.items():
    #    frame.append(item)
    df2 = pd.concat(frame2, axis=1, keys=stock_list2)
    df2 = df2.fillna(0)
    l = []

    for k in df2.columns:

        l.append("BSE/"+str(k))
 
    trace = go.Heatmap(z = df2.corr(min_periods = 12).values.tolist(), colorscale = 'Viridis', x = l, y= l)
    data=[trace]
    py.plot(data, filename='correlation-matrix-new',  auto_open=False)
    data = []
    i = 0
    print(l)
    for col in df2.columns:
        data.append(go.Scatter(x=df2[col].index, y=df2[col], name = l[i]))
        i+=1
    py.plot(data, filename = 'Standard Timeseries new',  auto_open=False)

gui.root.mainloop()


msg ="Select your algorithm."
title = "Dashboard Configuration Wizard"
choices = ["Genetic Algorithms", "Deep Learning", "SVM", "MLP"]
while 1:

    choice = choicebox(msg, title, choices)
    if choice is None:
        sys.exit(0)
    msgbox("You chose: {}\nThe Web dashboard will now initiate.....".format(choice), "Initiated (Press OK to reselect training algorithm)...")
    