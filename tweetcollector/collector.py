import tweepy, random, time
from tweetcollector.db import Database
from tweetcollector.report import Report
from unicodedata import normalize
from tweetcollector.senticnet_instance import Sentiment
from auth import access_token, access_token_secret, consumer_key, consumer_secret


class Collector():
    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
        self.db = Database()
        self.report = Report()
        self.st = Sentiment()

    def save_data(self, query, result):
        try:
            text = result.retweeted_status.full_text
        except:
            text = result.full_text
        name = result.user.screen_name
        img = result.user.profile_image_url
        id_user = result.id
        followers = result.user.followers_count
        location = result.user.location
        if self.st.sentiment_avg(text) and self.db.matches(text):
            self.db.save(id_user,name,text,img,followers,location)
            return True
        return False

    def collect(self, min_per_query, min_search):
        self.db = Database()
        self.db.create_table()
        search_time = time.time() + min_search*60
        while time.time() < search_time:
            timeout = time.time() + min_per_query*60
            query = random.choice(self.st.adjectives())
            print('collecting tweets with key %s' %normalize('NFKD', query).encode('ASCII', 'ignore').decode('ASCII'))
            count = 0
            try:
                for result in tweepy.Cursor(self.api.search, q=query, tweet_mode="extended", lang="pt").items():
                    if result:
                        if self.save_data(query,result):
                            count+=1
                    if time.time() > timeout:
                        break
            except tweepy.error.TweepError:
                error_time = time.time()
                time.sleep(30)
                min_search = (search_time - error_time)/60
                self.collect(min_per_query,min_search)
            self.report.save_report(query, count)