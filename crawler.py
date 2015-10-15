import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os

ckey = 'uaS0SBO5qIm9vQ1gPp67GRCYt'
consumer_secret = 'rBSB0XUDTGNwbGC2XNCp1w1XmIhTcWIZANarI01k4wT87mUafg'
access_token_key = '899074213-H30SiJX1Uff5gOJc8yeuLMD5gLPz5fkKMVtHlPod'
access_token_secret = 'P9fqfraxKqlNO7E8clFuRZl7dqhqqgCnmaw1svUJB4WVQ'

start_time = time.time() # grabs the system time
keyword_list = ['twitter'] #track list

#Listener Class Override
class listener(StreamListener):

	def __init__(self, start_time, time_limit=60):

		self.time = start_time
		self.limit = time_limit

	def on_data(self, data):

		while (time.time() - self.time) < self.limit:

			try:

				saveFile = open('raw_tweets.json', 'a')
				saveFile.write(data)
				saveFile.write('\n')
				saveFile.close()

				return True


			except BaseException, e:
				print 'failed ondata,', str(e)
				time.sleep(5)
				pass

		exit()

	def on_error(self, status):

		print statuses

auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)


twitterStream = Stream(auth, listener(start_time, time_limit=20)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Object
