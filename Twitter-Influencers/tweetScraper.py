import tweepy
from tweetFilter import TweetFilter
import json

#%%

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.Stream):

    def __init__(self, twitterAppCredentials, location, bufferSize):
        super().__init__(
                            consumer_key= twitterAppCredentials['consumer_key'],
                            consumer_secret= twitterAppCredentials['consumer_secret'],
                            access_token= twitterAppCredentials['access_token'],
                            access_token_secret= twitterAppCredentials['access_token_secret'],
                            daemon= False,
                            # daemon= True,
                            max_retries=1
                        )
        self.dataFilter = TweetFilter(regionCode= location,
                                    bufferSize= bufferSize,
                                    startIndex= 0)

        self.tweet_list = []
        self.file=open("tweet.json","w")
        self.num_tweets = bufferSize
        
    def on_status(self, status):
        print("Received tweet")
        if self.num_tweets>0:
            tweet=status._json
            self.file.write(json.dumps(tweet)+ '\n')
            self.tweet_list.append(status)
            
            self.num_tweets -=1

        if self.num_tweets <= 0:
            self.file.close()
            return False
        return True
        
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False
        if status_code == 406:
            print("on_error code: 406")
            #returning False in on_error disconnects the stream
            return False
        
    def on_exception(self, exception):
        print(exception)
        return

    def __del__(self):
        print("deleting Stream Listener")
        self.file.close()


#%%

class TweetScraper:
    def __init__(self, twitterAppCredentials, topicList, location, buffer_size):
        self.countryStream = MyStreamListener(twitterAppCredentials, location, buffer_size)
        self.topicList = topicList
        return

    def BeginStreaming(self):
        self.countryStream.filter(track=self.topicList, languages = ["en"], threaded=True)
        return
    
    def EndStreaming(self):
        self.countryStream.disconnect()
        return
    
    def GetDetails(self):
        print(self.countryStream.dataFilter)#.tweetsList.shape)
        print("Failed Tweets:\n",self.countryStream.dataFilter.failed_tweets)
        return self.countryStream.dataFilter.tweetsList
    
    def __del__(self):
        print(f'Deleting {self.topicList}')
        del self.countryStream
           