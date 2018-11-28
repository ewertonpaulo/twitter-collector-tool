import json

class Report:
    def load_json_report(self, dic):
        dic = open('tweetcollector/dicionario.json','w').write(json.dumps(dic, ensure_ascii=False))
        return dic

    def save_report(self, query, count):
        try:
            with open('tweetcollector/dicionario.json', 'r') as file_json:
                dic = json.loads(file_json.read())
            try:
                dic[query]['count'].append(count)
                dic = self.load_json_report(dic)
            except:
                dic[query] = {'count':count, 'search_time':0}
                dic = self.load_json_report(dic)
        except:
            dic = {}
            dic = self.load_json_report(dic)
            self.save_report(query,count)
