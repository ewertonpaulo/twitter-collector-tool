import tweepy
import json

#Autenticações
consumer_key = 'JItXCDXKcCqulu8vx58Go6eZg'
consumer_secret = 'Vlrza3KfonxqMpvzr4TDSG0cmrN9o6WBFkJrFAPxKuQVf5hjY3'
access_token = '750123144-tqP5pv6sHS4YTlBQKjy6CYZA9tD6JYuITluOzxeE'
access_token_secret = 'Eb8iNY45Z8JTTt7iytewOw5gdSTamWbddTZmeEUEWB8ue'

# Listener of tweets
class PrintListener(tweepy.StreamListener):

    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text
                
        user = status.user
        image = status.user.profile_image_url
        followers = status.user.followers_count
        location = status.user.location
        
        print(str(user.screen_name) + " => " + str(tweet.encode("ascii","ignore")))
    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = PrintListener()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    stream = tweepy.Stream(auth, listener)
    stream.filter(follow=None, track=['lula'], languages=["pt"])
