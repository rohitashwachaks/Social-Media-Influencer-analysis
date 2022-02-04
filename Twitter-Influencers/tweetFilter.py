# -*- coding: utf-8 -*-
"""
Created on Thu Feb 03 2022

@author: nemo
"""

#%% Import Dependencies

from tweetStructure import *
import pandas as pd


#%% Class Definition

class TweetFilter():
    def __init__(self, regionCode, startIndex, bufferSize):
        self.failed_tweets = []
        self.status = ''
        self.structuredTweet = ''
        self.rowCount = startIndex         #Change to ensure data not overriden
        self.buffer_size = bufferSize
        self.code = regionCode
        
        self.columnIndex = Col_Indexes()
        self.tweetsList = self.columnIndex.getStructuredDF()
        return
    
    
    def FailPreFilters(self):
        flag = False                # Assume every tweet passes pre-filters by default; untill proven otherwise
        # Add Language Check
        if self.status["lang"] != "en":
            flag = True
        
        # Add Duplication Check
        flag = idSet.CheckID(self.status["id_str"])    # Flag = True -> already Exists
        
        return flag
    
    
    def FailPostFilters(self, data):
        flag = False                # Assume every tweet passes post-filters by default; untill proven otherwise
        # Add Country Check
        
        try:
            if self.code not in data["location"][0]:
                flag = True
        except:
            flag = True
        
        return flag
    
    
    def UploadTweet(self):
        try:
#             d2g.upload(self.tweetsList,
#                        spreadsheet_key,
#                        wks_name,
#                        credentials=credentials,
#                        col_names=False,
#                        row_names=True,
#                        start_cell = ''.join(['A',str(self.rowCount)]),  
#                        clean=False)
#             self.rowCount = self.rowCount + self.buffer_size
#             self.tweetsList = self.tweetsList.iloc[0:0]
            return True
        except BaseException as ex:
            print('failed while Uploading to Google Sheets: ',str(ex))
            self.failed_tweets.append(self.status["id_str"])
            return False

    def StoreTweet(self, data):
        status = True
        # Store Tweets and Upload Them
        try:
            self.tweetsList = pd.concat([self.tweetsList, data], ignore_index=True)
            if self.tweetsList.shape[0] >= self.buffer_size:
                status = self.UploadTweet()
            return status
        
        except BaseException as ex:
            print('failed in UploadTweet: ',str(ex))
            self.failed_tweets.append(self.status["id_str"])
            return False
    
    
    
    def ProcessTweet(self):
        # Process tweet to get desired output
        status = False
        # Discard Tweet if Pre-Filter Criterias not met
#         if self.FailPreFilters(): 
#             return status 
        
        # StructureTweet()
        try:
            structuredTweet = GetStructuredTweet(self.status)
            
        except BaseException as ex:
            print('failed in GetStructuredTweet: ',str(ex))
            self.failed_tweets.append(self.status["id_str"])
            return status
        
        # Discard Tweet if Post-Filter Criterias not met
        if self.FailPostFilters(structuredTweet): 
            return status
        
        # StoreTweet()
        status = self.StoreTweet(structuredTweet)
        
        return status
    
    
    def PreProcessTweet(self, tweet):
        # Pre Process Tweet Data and obtain 'root' tweet
        body = tweet._json
        # Get Root Tweet
        retweet_id = "#"
        quoted_id = "#"
        
        try:
            #Quoted
            if "quoted_status" in body:
                if "retweeted_status" in body["quoted_status"]:
                    self.status = body["quoted_status"]["retweeted_status"]
                else:
                    self.status = body["quoted_status"]

            #Retweeted
            elif "retweeted_status" in body:
                if "quoted_status" in body["retweeted_status"]:
                    self.status = body["retweeted_status"]["quoted_status"]
                else:
                    self.status = body["retweeted_status"]

            #Original
            else:
                self.status = body

            status = self.ProcessTweet()

            if status:
                idSet.UpdateID(body["id_str"])

            return status
        except BaseException as e:
            print('failed: ',e)
            self.failed_tweets.append(self.status["id_str"])