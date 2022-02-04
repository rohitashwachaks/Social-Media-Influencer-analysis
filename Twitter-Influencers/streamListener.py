# -*- coding: utf-8 -*-
"""
Created on Thu Feb 03 2022

@author: nemo
"""


#%% Import Dependencies

from tweetFilter import *

import tweepy


#%% Class Definition

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, code, startIndex = 'A1', bufferSize = 10):
        super().__init__()
        self.dataFilter = TweetFilter(code, startIndex, bufferSize)
#         self.dataFilter = DataFilter()
        
#     def __del__(self):
#         print("del dataFilter")
#         del self.dataFilter
    
    def on_status(self, status):
        #print(status.text)
        self.dataFilter.PreProcessTweet(status)
#         self.dataFilter.filter_tweet(status)
        
        
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False