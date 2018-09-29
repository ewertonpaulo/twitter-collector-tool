import tweepy
import psycopg2
from senticnet_instance import sentiment
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

        name = status.user.screen_name
        image = status.user.profile_image_url
        followers = status.user.followers_count
        location = status.user.location
        id_twitter = status.id_str
        partial_classification = ''
        name = treatment_string(name)
        location = treatment_string(location)
        text = treatment_string(text)
        text = text[0:]
        
        partial_classification = sentiment(text, partial_classification)
        database_connection = Database()
        if partial_classification in ['partial_negative','partial_positive']:
            database_connection.insert_new(id_twitter,name,text,image,followers,location, partial_classification)
        else:
            database_connection.insert_new(id_twitter,name,text,image,followers,location, partial_classification)
        
    def on_limit(self,status):
        print ("Rate Limit Exceeded, Sleep for 15 Mins")
        time.sleep(15 * 60)
        return True

    def on_error(self, status):
        if(status == 420):
            print ("Twitter is limiting this account.")
            return True
        else:
            print ("Error Status "+ str(status))
    
def collect(string):
    #Instance of listener and authentications
    listener = Listener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, listener)
    print('collecting tweets with key %s' %string)
    stream.filter(track=[string], languages=["pt"])    

def treatment_string(string):
    string = str(string)
    string = string.encode('utf-8').decode('utf-8')
    string = string.replace("'","´")
    string = string.replace('"',"´")
    return string
