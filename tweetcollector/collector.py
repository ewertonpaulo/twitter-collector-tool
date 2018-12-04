import tweepy, random, time, json
from unicodedata import normalize
from tweetcollector.db import Database
from tweetcollector.report import Report
from tweetcollector.senticnet_instance import Sentiment
from auth import access_token, access_token_secret, consumer_key, consumer_secret


class Collector():
    def __init__(self):
        self.db = Database()
        self.report = Report()
        self.st = Sentiment()
        self.api = None
        self.all = None

    def save_data(self, query, result):
        try:
            text = result.retweeted_status.full_text
        except:
            text = result.full_text
        id_twitter = result.id
        name = result.user.screen_name
        img = result.user.profile_image_url
        followers = result.user.followers_count
        location = result.user.location
        self.db.save(id_twitter,name,text,img,followers,location,self.all)

    def collect(self, min_per_query, min_search):
        self.db = Database()
        self.db.create_table()
        self.auth()
        timeout = time.time() + min_per_query*60
        search_time = time.time() + min_search*60
        self.all = self.db.get_all()
        while time.time() < search_time:
            self.doing(search_time,self.api,timeout, min_search)

    def doing(self,search_time,api,timeout, min_search):
        query = random.choice(self.st.adjectives())
        print('collecting tweets with key %s' %normalize('NFKD', query).encode('ASCII', 'ignore').decode('ASCII'))
        try:
            for result in tweepy.Cursor(api.search, q=query, tweet_mode="extended", lang="pt").items():
                if result:
                    self.save_data(query,result)
                if time.time() > timeout:
                    break
        except tweepy.error.TweepError:
            error_time = time.time()
            time.sleep(30)
            self.collect(timeout/60, min_search = (search_time - error_time)/60)

    def auth(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)