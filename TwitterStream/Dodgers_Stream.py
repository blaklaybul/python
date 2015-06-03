import tweepy
import sys
import pymongo

ckey = 'wea96s33EhV2FOMtjQjAw'
csec = 'iu6l3Jw7ifWwdEL480N0tKAgefsoxw1cnsuqnA0Ac'
atok = '1884142105-DYNRDv6OvDmjgJkFKz34nnqcGuNvyn4hy65VRb0'
asec = 'sMROyokyoWm3lcwVnRYVSRGHinyhsIkHDGFDICDwA'

auth = tweepy.OAuthHandler(ckey, csec)
auth.set_access_token(atok, asec)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        self.db = pymongo.MongoClient().Dodgers

    def on_status(self, status):
        print status.text , "\n"

        data ={}
        data['text'] = status.text
        data['created_at'] = status.created_at
        data['geo'] = status.geo
        data['source'] = status.source

        self.db.Tweets.insert(data)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=['dodgers'])