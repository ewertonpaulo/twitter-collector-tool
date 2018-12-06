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
        self.all = None
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

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
        return self.db.save(id_twitter,name,text,img,followers,location,self.all)

    def collect(self, min_per_query, min_search):
        self.db = Database()
        self.db.create_table()
        search_time = time.time() + min_search*60
        self.all = self.db.get_all()
        while time.time() < search_time:
            count = 0
            timeout = time.time() + min_per_query*60
            query = random.choice(self.st.adjectives())
            print('collecting tweets with key %s' %normalize('NFKD', query).encode('ASCII', 'ignore').decode('ASCII'))
            count = self.doing(timeout, query, count)
            self.report.save_report(query, count)

    def doing(self,timeout, query, count):
        api = self.auth_()
        try:
            for result in tweepy.Cursor(api.search, q=query, tweet_mode="extended", lang="pt").items():
                if result:
                    if self.save_data(query,result):
                        count+=1
                if time.time() > timeout:
                    break
        except:
            print('waiting 60 seconds')
            time.sleep(60)
            timeout += 60
            self.doing(timeout, query, count)
        return count
        # ConnectionError

    def auth_(self):
        api = tweepy.API(self.auth)
        return api