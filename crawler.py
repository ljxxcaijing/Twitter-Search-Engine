import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import re
import json

ckey = 'uaS0SBO5qIm9vQ1gPp67GRCYt'
consumer_secret = 'rBSB0XUDTGNwbGC2XNCp1w1XmIhTcWIZANarI01k4wT87mUafg'
access_token_key = '899074213-H30SiJX1Uff5gOJc8yeuLMD5gLPz5fkKMVtHlPod'
access_token_secret = 'P9fqfraxKqlNO7E8clFuRZl7dqhqqgCnmaw1svUJB4WVQ'
i = 1
start_time = time.time() # grabs the system time
keyword_list = ['life'] #track list

#Listener Class Override
class listener(StreamListener):

	def on_data(self, data):
		try:
			global i
			json_data = json.loads(data)
			new_json = {}
			new_json ["created_at"] = json_data["created_at"]
			new_json ["name"] = json_data["user"]["name"]
			if (json_data["coordinates"]):
				new_json ["location"] = json_data["coordinates"]["coordinates"]
			else:
				new_json ["location"] = json_data["coordinates"]
			new_json ["text"] = json_data["text"]
			new_json ["link"] = re.findall(r'(https?://\S+)', json_data["text"])
			result_json = json.dumps(new_json)
			saveFile = open('tweets/raw_tweets'+str(i) + '.json', 'a')
			saveFile.write(result_json)
			saveFile.write('\n')
			if (os.path.getsize('tweets/raw_tweets'+str(i) + '.json') > 10485760):
				i += 1
				saveFile.close()
			return True

		except BaseException, e:
			print 'failed ondata,', str(e)
			time.sleep(5)
			pass

	def on_error(self, status):
		print status

auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)


twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[-180,-90,180,90]) #call the filter method to run the Stream Object
