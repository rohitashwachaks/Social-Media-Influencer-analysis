# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 00:27:26 2020

@author: rohit
"""

#%% Import Dependencies

import pandas as pd
from typing import Any, Union


#%% Class Indexes

class Col_Indexes:
    
    def __init__(self, col_names: Union[None, list] = None)-> None:
        self.index = ["created_at",
               "id_str", "user_id",
               "is_quote_status",
               "text", "verified", 
               "likes", "retweet_count",
               #"tweet_loc", "user_loc", "geoParsed",
               "location","json"
              ] if col_names is None else col_names
        return

    def aslist(self):
        return self.index
    def __iter__(self):
        return iter(self.aslist())

    
    def getColIndex(self):
        return self.index
    
    def getStructuredDF(self):
        return pd.DataFrame(columns = self.index)
    
    def getStructuredDF(self, data: Union[pd.DataFrame, None] = None)-> Union[pd.DataFrame, str] :
        if data == None:
            return 'Initialised'
        return pd.Series(data= data[self.index],
                         index = self.index).to_frame().T

#%% Class Get Structured Tweets

    def GetStructuredTweet(inp):
        try:
            created_at = inp["created_at"]
            id_str = inp["id_str"]
            user_id = inp["user"]["id_str"]
            is_quote_status = inp["is_quote_status"]
            
            text = inp["extended_tweet"]["full_text"] if "extended_tweet" in inp else inp["text"]
        
            likes = inp["favorite_count"]
            retweet_count = inp["retweet_count"]
            verified = inp["user"]["verified"]
            json_body = json.dumps(inp)

            user_loc = inp["user"]["location"] or np.nan
            
            # location = getEnsembleLoc(inp["place"], user_loc, text)
            
            # if(location != None):
            #     location = ','.join(list(location))
            
            k = pd.Series([created_at,
                           id_str, user_id,
                           is_quote_status,
                           text, verified,
                           likes, retweet_count,
                           user_loc, json_body
                          ],
                     index = col_indexes).to_frame().T
            return k
        except BaseException as ex:
            print('failed in Structuring the tweet: ',inp["id_str"],ex)
            return pd.DataFrame(columns = col_indexes)