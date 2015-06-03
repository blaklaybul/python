from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ckey = 'wea96s33EhV2FOMtjQjAw'
csec = 'iu6l3Jw7ifWwdEL480N0tKAgefsoxw1cnsuqnA0Ac'
atok = '1884142105-DYNRDv6OvDmjgJkFKz34nnqcGuNvyn4hy65VRb0'
asec = 'sMROyokyoWm3lcwVnRYVSRGHinyhsIkHDGFDICDwA'

class listener(StreamListener):

	def on_data(self,data):
		print data
		return True

	def on_error(self,status):
		print status

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = listener()
    auth = OAuthHandler(ckey, csec)
    auth.set_access_token(atok, asec)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['hillary2016', 'hillaryclinton', 'clinton'])