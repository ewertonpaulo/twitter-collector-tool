import tweepy, sys, time, random
from unicodedata import normalize
from time import sleep
from src.db import Database
from queue import Queue
from threading import Thread 
from src.senticnet_instance import sentiment, adjectives
from auth import access_token, access_token_secret, consumer_key, consumer_secret

# Listener of tweets
class Listener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.counter=0

    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text
        dt = {'name':str_(status.user.screen_name),'image':status.user.profile_image_url,'id_twitter':status.id_str,
            'followers':status.user.followers_count,'location':str_(status.user.location)}
        text = str_(text)
        text = text[0:]
        db = Database()
        if sentiment(text) == True and db.find(text) == True:
            self.counter = self.counter + 1
            db.insert_new(dt['id_twitter'],dt['name'],text,dt['image'],dt['followers'],dt['location'])
            sys.stdout.write("\r%d tweets coletados" % self.counter)
            sys.stdout.flush()
        else:
            pass

    def on_limit(self,status):
        sleep(5)
        return True

    def on_error(self, status):
        if(status == 420):
            return True
        else:
            print("Error Status "+ str(status))

def collect():
    listener = Listener()
    db = Database()
    db.create_table()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, listener)
    string = random.choice(adjectives())
    show = normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')
    print('collecting tweets with key a')
    while True:
        try:
            stream.filter(track=['a'], languages=["pt"])
        except KeyboardInterrupt:
            stream.disconnect()
            break
        except:
            continue

def str_(string):
    string = str(string)
    string = string.encode('utf-8').decode('utf-8')
    string = string.replace("'","\'")
    string = string.replace('"',"\"")
    return string
