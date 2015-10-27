#!/usr/bin/env python

from bs4 import BeautifulSoup
import json
import os
import re
import requests
import robotparser
import time
import threading
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from urlparse import urlparse
import yaml

ckey = 'uaS0SBO5qIm9vQ1gPp67GRCYt'
consumer_secret = 'rBSB0XUDTGNwbGC2XNCp1w1XmIhTcWIZANarI01k4wT87mUafg'
access_token_key = '899074213-H30SiJX1Uff5gOJc8yeuLMD5gLPz5fkKMVtHlPod'
access_token_secret = 'P9fqfraxKqlNO7E8clFuRZl7dqhqqgCnmaw1svUJB4WVQ'
i = 1
start_time = time.time() # grabs the system time
keyword_list = ['life'] #track list

"""
visitUrl takes in fileName of raw_tweets data and creates a file
of raw tweets with the visited url data added to the json data.

Called as a new thread once raw data is done being written
"""
def visitUrl(fileName):
	visited = {} #dictionary of visited urls
	rp = robotparser.RobotFileParser()	#robot file parser

	#create new file for visited url info
	newName = fileName[:-5] + "_visited.json"
	saveFile = open(newName, 'a')

	with open(fileName) as oldFile:
		#for each tweet
		for line in oldFile:
			j = yaml.safe_load(line)
			#if links exist
			if j['urls']:
				urls = j['urls']
				#for each link
				for url in urls:
					#get url value
					url = url["expanded_url"]

					#check robots
					parsed = urlparse(url)
					robotsUrl = parsed.scheme + "://" + parsed.netloc + "/robots.txt"
					rp.set_url(robotsUrl)
					rp.read()

					if rp.can_fetch('*', url):
						#get info from url
						r = requests.get(url)
						soup = BeautifulSoup(r.content, 'html.parser')
						#append info onto json_data
						if soup.title.string:
							j["title"] = soup.title.string
							print j["title"]
						else:
							j["title"] = None

			else:	#link doesn't exist
				j["title"] = None
			#write line to file
			newLine = json.dumps(j)
			saveFile.write(newLine)
			saveFile.write('\n')

		#remove old file
		os.remove(fileName)
		saveFile.close()
		oldFile.close()

	return

#Listener Class Override
class listener(StreamListener):

	def on_data(self, data):
		try:
			global i
			json_data = json.loads(data)
			new_json = {}
			new_json ["created_at"] = json_data["created_at"]
			new_json ["name"] = json_data["user"]["name"]
			new_json ["text"] = json_data["text"]
			if (json_data["coordinates"]):
				new_json ["location"] = json_data["coordinates"]["coordinates"]
			else:
				new_json ["location"] = json_data["coordinates"]
			new_json ["urls"] = json_data["entities"]["urls"]
			#new_json ["urls"] = json_data["urls"]
			#new_json ["link"] = re.findall(r'(https?://\S+)', json_data["text"])
			result_json = json.dumps(new_json)
			fileName = 'tweets/raw_tweets'+ str(i) + '.json'
			saveFile = open(fileName, 'a')
			saveFile.write(result_json)
			saveFile.write('\n')
			if (os.path.getsize(fileName) > 30000):
				saveFile.close()
				#New thread to visit urls of tweets
				t = threading.Thread(target=visitUrl, args=[fileName])
				t.start()
				i += 1
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
