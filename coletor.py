import tweepy
from time import sleep
from db import Database
from auth import access_token, access_token_secret, consumer_key, consumer_secret

# Listener of tweets
class Listener(tweepy.StreamListener):

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

        name = str(status.user.screen_name)
        image = str(status.user.profile_image_url)
        followers = str(status.user.followers_count)
        location = str(status.user.location)
        text.replace("'","´")
        text.replace('"',"´´")
        text.encode('utf-8').decode('utf-8')
        text = text[0:]
        
        database_connection = Database(name,text,image,followers,location)
        try:
            database_connection.insert_new()
        except:
            database_connection.create_table()
        

        #print(text)

    def on_error(self, status):
        print(status)
    
def collect(string):
    #Instance of listener and authentications
    listener = Listener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, listener)
    while True:
        try:
            print('collecting tweets with key %s' %string)
            stream.filter(track=[string], languages=["pt"])
        except:
            print("waiting...")
            sleep(5)
