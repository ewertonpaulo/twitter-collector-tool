import json
import re
from unicodedata import normalize
from tweetcollector.db import Database
from tweetcollector.senticnet_instance import Sentiment

class Report:

    def __init__(self):
        self.db = Database()
        self.st = Sentiment()

    def load_json_report(self, dic, name):
        dic = open('%s.json' %name,'w').write(json.dumps(dic, ensure_ascii=False))
        return dic

    def save_report(self, query, count, name, param):
        try:
            dic = self.open_json(name)
            try:
                dic[query][param].append(count)
                dic = self.load_json_report(dic, name)
            except:
                dic[query] = {param:count}
                dic = self.load_json_report(dic, name)
        except:
            dic = {}
            dic = self.load_json_report(dic, name)
            self.save_report(query,count, name, param)

    def open_json(self, name):
        with open('%s.json' %name, 'r') as file_json:
            return json.loads(file_json.read())

    def rm_acentos(self, txt):
        temp = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
        return temp.lower()

    def update(self):
        querys = self.last_attempt()
        tweets = self.db.get_all()
        print(len(tweets))
        for i in querys:
            i = self.rm_acentos(i)
            count = 0
            for y in tweets:
                text = self.rm_acentos(y[1])
                if re.search(i, text):
                    count+=1
            self.save_report(i, count, 'dic', 'count')

    def last_attempt(self):
        try:
            dic = self.open_json('dic')
            adjs = self.st.adjectives()
            els = list(dic.items())
            last_query = els[-1][0]
            index = adjs.index(last_query)
            return adjs[index:len(adjs)]
        except:
            return self.st.adjectives()

    def last_id_tweet(self, query, id_tweet):
        self.save_report(query, id_tweet, 'temp', 'id')

    def last_id(self, query):
        try:
            dic = self.open_json('temp')
            try:
                dic[query]['id']
            except:
                return 0
        except:
            dic = {}
            dic = self.load_json_report(dic, 'temp')
            return 0