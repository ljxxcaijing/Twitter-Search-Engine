#!/usr/bin/env python

from bs4 import BeautifulSoup
import json
import os
import requests
import robotparser
import sys
import time
import threading
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from urlparse import urlparse

i = 70

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
			try:
				json_data = json.loads(line)
				j = {}
				j["created_at"] = json_data["created_at"]
				j["name"] = json_data["user"]["name"]
				j["text"] = json_data["text"]
				j["htags"] = json_data["entities"]["hashtags"]
				j["location"] = json_data["place"]["bounding_box"]["coordinates"]
				j["urls"] = json_data["entities"]["urls"]

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
								#cprint j["title"]
							else:
								j["title"] = None

				else:	#link doesn't exist
					j["title"] = None
				#write line to file
				newLine = json.dumps(j)
				saveFile.write(newLine)
				saveFile.write('\n')
			except BaseException, e:
				#print 'failed on visit', str(e)
				pass
	#remove old file
	oldFile.close()
	saveFile.close()
	os.remove(fileName)


	return

#Listener Class Override
class listener(StreamListener):
	def __init__(self, fileSize, outputDir):
		self.fileSize = int(fileSize) * 10000000
		self.outputDir = outputDir
		if not os.path.exists(outputDir):
			os.makedirs(outputDir)

	def on_data(self, data):
		try:
			global i
			to_json = json.loads(data)
			res = json.dumps(to_json)
			self.fileName = os.path.join(self.outputDir, 'raw_tweets'+ str(i) + '.json')
			self.saveFile = open(self.fileName, 'a')
			self.saveFile.write(res)
			self.saveFile.write('\n')
			if (os.path.getsize(self.fileName) > self.fileSize):
				self.saveFile.close()
				i += 1
				#New thread to visit urls of tweets
				t = threading.Thread(target=visitUrl, args=[self.fileName])
				t.start()

			return True

		except BaseException, e:
			print 'failed ondata,', str(e)
			time.sleep(5)
			pass

	def on_error(self, status):
		print 'FAILED ON ERROR: ', status

def main(argv):
	if len(argv) != 2:
		print "Please enter with two command line arguments: fileSize, outputFile"
		return

	ckey = 'bUovU12dSjif7vcWMOrfjkMMh'
	consumer_secret = 'idZCztlegOdFXTGM7qolbF4n5qnUM9H8RjYVVmXMSJSplp7He5'
	access_token_key = '899074213-EMRW02PKE7aGYcXhmNbnMLMyxrfGLXvQZd85i6mJ'
	access_token_secret = 'BeHbdfLy56KoxmuEiY3mX0zbD5GXJnD3lT2faQzxZOczP'

	auth = OAuthHandler(ckey, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)
	while True:
		try:
			twitterStream = Stream(auth, listener(argv[0], argv[1]))
			twitterStream.filter(locations=[-125.0011, 24.9493, -66.9326, 49.5904], stall_warnings=True) #call the filter method to run the Stream Object
		except:
			continue

if __name__ == "__main__":
   main(sys.argv[1:])
