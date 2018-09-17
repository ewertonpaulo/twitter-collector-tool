import tweepy
from coletor import Listener, access_token, access_token_secret, consumer_key, consumer_secret
from db import DatabaseConnection
from time import sleep

if __name__ == '__main__':
    listener = Listener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, listener)
    while True:
        try:
            stream.filter(track=["amor"], languages=["pt"])
        except:
            print("waiting...")
            sleep(5)
