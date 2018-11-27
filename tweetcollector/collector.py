import tweepy, random, time
from tweetcollector.db import Database
from unicodedata import normalize
from tweetcollector.senticnet_instance import sentiment, adjectives
from auth import access_token, access_token_secret, consumer_key, consumer_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def save_data(result):
    db = Database()
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

def collect(min_per_query,min_search):
    db = Database()
    db.create_table()
    search_time = time.time() + min_search*60
    while time.time() < search_time:
        timeout = time.time() + min_per_query*60
        query = random.choice(adjectives())
        print('collecting tweets with key %s' %normalize('NFKD', query).encode('ASCII', 'ignore').decode('ASCII'))
        try:
            for result in tweepy.Cursor(api.search, q=query, tweet_mode="extended", lang="pt").items():
                if result:
                    save_data(result)
                if time.time() > timeout:
                    print('timeout')
                    break
        except tweepy.error.TweepError:
            time.sleep(60)
            collect(min_per_query,min_search)