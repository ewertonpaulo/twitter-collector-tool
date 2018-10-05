import tweepy
from time import sleep
from db import Database
from queue import Queue
from threading import Thread 
from senticnet_instance import sentiment
from auth import access_token, access_token_secret, consumer_key, consumer_secret

# Listener of tweets
class Listener(tweepy.StreamListener):
    def __init__(self, q = Queue()):
        super().__init__()
        self.q = q
        for i in range(4):
            t = Thread(target=self.do_stuff)
            t.daemon = True
            t.start()

    def on_status(self, status):
        self.q.put(status)
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
            
            db.insert_new(
                dt['id_twitter'],dt['name'],text,dt['image'],dt['followers'],dt['location'])
            print(text)
        else:
            pass
    
    def do_stuff(self):
        while True:
            self.q.get()
            self.q.task_done()

    def on_limit(self,status):
        print ("Rate Limit Exceeded, Sleep for 15 Mins")
        time.sleep(60)
        return True

    def on_error(self, status):
        if(status == 420):
            print ("Twitter is limiting this account.")
            return True
        else:
            print ("Error Status "+ str(status))

def collect(string):
    listener = Listener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, listener)
    print('collecting tweets with key %s' %string)
    while True:
        try:
            stream.filter(track=[string], languages=["pt"])
        except:
            continue

def str_(string):
    string = str(string)
    string = string.encode('utf-8').decode('utf-8')
    string = string.replace("'","´")
    string = string.replace('"',"´")
    return string
