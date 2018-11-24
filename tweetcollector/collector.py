import tweepy, random, time
from tweetcollector.db import Database
from unicodedata import normalize
from tweetcollector.senticnet_instance import sentiment, adjectives
from auth import access_token, access_token_secret, consumer_key, consumer_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def save_data(results):
    db = Database()
    for result in results:
        try:
            text = result.retweeted_status.full_text
        except:
            text = result.full_text
        name = result.user.screen_name
        img = result.user.profile_image_url
        id_user = result.id
        followers = result.user.followers_count
        location = result.user.location
        if sentiment(text) and db.matches(text):
            db.save(id_user,name,text,img,followers,location)

def collect(minutes):
    db = Database()
    db.create_table()
    string = random.choice(adjectives())
    print('collecting tweets with key %s for %d minutes' %(normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII'),minutes))
    last_id = 1
    timeout = time.time() + 60*minutes
    while True:
        if time.time() > timeout:
            break
        results = api.search(q=string,since_id=last_id, count=100, tweet_mode="extended", lang="pt")
        try:
            last_id=results[-1].id
        except:
            last_id=1
        save_data(results)
