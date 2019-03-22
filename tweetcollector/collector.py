import tweepy, random, time, json
from unicodedata import normalize
from tweetcollector.db import Database
from tweetcollector.report import Report
from tweetcollector.senticnet_instance import Sentiment
from auth import access_token, access_token_secret, consumer_key, consumer_secret


class Collector():
    def __init__(self):
        self.db = Database()
        self.st = Sentiment()
        self.rp = Report()
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

    def collect(self, min_per_query = 30, min_search = 1440):
        search_time = time.time() + min_search*60
        while time.time() < search_time:
            timeout = time.time() + min_per_query*60
            query = random.choice(self.st.adjectives())
            try:
                self.doing(timeout, query)
            except tweepy.error.TweepError:
                error_time = time.time()
                time.sleep(30)
                min_search = (search_time - error_time) / 60
                self.collect(min_per_query,min_search)

    def doing(self,timeout, query):
        api = self.auth_()
        last = self.rp.last_id(query)
        print('collecting tweets with key %s' %normalize('NFKD', query).encode('ASCII', 'ignore').decode('ASCII'))
        for result in tweepy.Cursor(api.search, q=query, since_id=last, tweet_mode="extended", lang="pt").items():
            if result:
                self.db.save(result, query)
                self.rp.last_id_tweet(query,result.id)
            if time.time() > timeout:
                break

    def auth_(self):
        api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
        return api