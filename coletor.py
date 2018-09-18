import tweepy
from db import DatabaseConnection

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
        
        database_connection = DatabaseConnection(name,text,image,followers,location)
        database_connection.create_table()
        database_connection.insert_new()

        print(text)

    def on_error(self, status):
        print(status)
