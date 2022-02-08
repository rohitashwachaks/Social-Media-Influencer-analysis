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
        self.file=open("tweet.json","w+")
        self.file.write('[ ')
        self.num_tweets = bufferSize
        
    def on_status(self, status):
        print("Received tweet")
        bool = True
        self.num_tweets -= 1
        tweet=status._json

        if self.num_tweets>0:
            self.file.write(json.dumps(tweet).strip()+ ',')
            self.tweet_list.append(status)
            

        if self.num_tweets <= 0:
            self.file.write(json.dumps(tweet).strip()+ ']')
            self.file.close()
            super().disconnect()
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
        if not self.file.closed:
            self.file.write(']')
            self.file.close()


#%%

class TweetScraper:
    def __init__(self, twitterAppCredentials, topicList = None, location = ["US"], buffer_size= 512):
        self.stream = MyStreamListener(twitterAppCredentials, location, buffer_size)
        self.topicList = topicList
        return

    def Start(self):
        print(f"Beginning Stream for {self.topicList}")
        self.stream.filter(track=self.topicList, languages = ["en"], threaded=True)
        return
    
    def End(self):
        self.stream.disconnect()
        return
    
    def GetDetails(self):
        print(self.stream.dataFilter)#.tweetsList.shape)
        print("Failed Tweets:\n",self.stream.dataFilter.failed_tweets)
        return self.stream.dataFilter.tweetsList

    def Status(self):
        print('running',self.stream.running)
        print('session',self.stream.session)
        print('thread',self.stream.thread)
        print('user_agent',self.stream.user_agent)
        return
    
    def __del__(self):
        print(f'Deleting {self.topicList}')
        del self.stream
           