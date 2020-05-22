# -*- coding: utf-8 -*-
"""
Created on Mon May  4 15:46:33 2020

@author: nrdas
"""
from textblob import TextBlob
from statistics import mean
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '1215****'
ACCESS_SECRET = 'xhj8****'
CONSUMER_KEY = '1QCej****'
CONSUMER_SECRET = 'iwGMq****'

# Setup tweepy to authenticate with Twitter credentials:

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

class StreamListener(tweepy.StreamListener):
    tweet_list = []
    
    def on_status(self, status):
        self.tweet_list.append(json.dumps(status._json)['text'])
    
    def on_error(self, status_code):
        if status_code == 420:
            return False

def check_sentiment(tweet_list):
    sent = []
    sbjt = []
    for tweets in tweet_list:
        b = TextBlob(tweets)
        sent.append(b.sentiment.polarity)
        sbjt.append(b.sentiment.subjectivity)
    return (mean(sent), mean(sbjt))  
    
def load_tweets(name):
    tweet_list = []
    for tweet in tweepy.Cursor(api.search, q=name, lang='en').items(300):
        tweet_list.append(json.loads(json.dumps(tweet._json))['text'])
    return tweet_list

