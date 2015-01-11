# Author: Omar A. Ansari
# Version 1.3 December 2014. Use of this program is permitted with no warranties or liabilities.
#
# This python script employs the Tweepy library to scan for tweets to a certain Twitter user. When a tweet is received,
# a pin on the Arduino board turns on, then off for 60 seconds.
#


#!/usr/bin/env python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from Arduino import Arduino
import tweepy
import time
import datetime
import re


CONSUMER_KEY = 'XXXXXXXXXXXXXXXX' #keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #keep the quotes, replace this with your access token
ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #keep the quotes, replace this with your access token secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
board = Arduino('9600', port="/dev/ttyUSB0") #Change to your port.
board.pinMode(13, "OUTPUT") #Change to pin used on Arduino.


PREV_MENTION = "DUMMY"

def checkForTweets(pin):
    global PREV_MENTION
    board.pinMode(pin, "OUTPUT")
    board.digitalWrite(13, "HIGH")
    for mention in api.mentions_timeline(user_id = "2914398401", count = "1"): # Change to user ID you would like to scan.
        MENTION = mention.text
        if (MENTION != PREV_MENTION):
            print MENTION
            count = 0
            while (count < 60):
            #sleepTime = int(re.match(r'\d+', MENTION).group())
                board.digitalWrite(pin, "HIGH")
                print "GOING TO SLEEP"
                time.sleep(1)
                print "WAKING UP"
                board.digitalWrite(pin, "LOW")
                time.sleep(1)
                count = count + 1
        PREV_MENTION = MENTION
       
while True:
       
        checkForTweets(13)
        print "GOING TO SLEEP AGAIN"
    board.digitalWrite(13, "HIGH")
    time.sleep(60)