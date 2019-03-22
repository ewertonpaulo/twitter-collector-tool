import json
import re
from unicodedata import normalize
from tweetcollector.db import Database
from tweetcollector.senticnet_instance import Sentiment

class Report:

    def __init__(self):
        self.db = Database()
        self.st = Sentiment()

    def load_json_report(self, dic):
        dic = open('dic.json','w').write(json.dumps(dic, ensure_ascii=False))
        return dic

    def save_report(self, query, count):
        try:
            dic = self.open_json()
            try:
                dic[query]['count'].append(count)
                dic = self.load_json_report(dic)
            except:
                dic[query] = {'count':count}
                dic = self.load_json_report(dic)
        except:
            dic = {}
            dic = self.load_json_report(dic)
            self.save_report(query,count)

    def open_json(self):
        with open('dic.json', 'r') as file_json:
            return json.loads(file_json.read())

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
            self.save_report(i, count)
    
    def rm_acentos(self, txt):
        temp = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
        return temp.lower()

    def last_attempt(self):
        try:
            dic = self.open_json()
            adjs = self.st.adjectives()
            els = list(dic.items())
            last_query = els[-1][0]
            index = adjs.index(last_query)
            return adjs[index:len(adjs)]
        except:
            return self.st.adjectives()