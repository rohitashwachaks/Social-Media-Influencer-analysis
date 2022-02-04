# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:27:26 2020

@author: rohit
"""

#%% Import Dependencies

import pandas as pd


#%% Class Indexes

class Col_Indexes:
    
    def __init__(self):
        self.index = ["created_at",
               "id_str", "user_id",
               "is_quote_status",
               "text", "verified", 
               "likes", "retweet_count",
               #"tweet_loc", "user_loc", "geoParsed",
               "location","json"
              ]
        return
    
    def getColIndex(self):
        return self.index
    
    def getStructuredDF(self):
        return pd.DataFrame(columns = self.index)
    
    def getStructuredDF(self, data):
        return pd.Series([created_at,
                          id_str, user_id,
                          is_quote_status,
                          ziptext, verified,
                          likes, retweet_count,
                          #tweet_loc, user_loc, geoParsed,
                          location, json_body
                          ],
                         index = index).to_frame().T

#%% Class Get Structured Tweets