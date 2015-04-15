import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from kafka import SimpleProducer, KafkaClient
import os
import re
import logging
import logging.handlers

# import twitter keys and tokens
from config import *

#kafka = KafkaClient(os.environ['KAFKA_1_PORT_9092_TCP_ADDR'] + ':9092')
kafka = KafkaClient('kafka:9092')
producer = SimpleProducer(kafka)
topic = "hashtag-topic"

class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):
        logger = logging.getLogger('twitter_stream')

        # JSON decode the tweet
        try:
            decoded = json.loads(data)
        except ValueError:
            logger.warn("Could not JSON decode Twitter response")
            return False

        # Fetch the text content of the Tweet
        tweet = ''
        try:
            tweet = decoded['text']
        except KeyError:
            logger.warn('No key text in Twitter response')
            return False

        tweet_regex = re.compile(r"#([^\s|#]+)")
        hashtags = re.findall(tweet_regex, tweet)

        for hashtag in hashtags:
            #write to kafka
            print hashtag.encode('utf-8')
            producer.send_messages(topic, hashtag)

        return True

    # on failure
    def on_error(self, status):
        print status

if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for keyword
    stream.filter(track=['congress'])