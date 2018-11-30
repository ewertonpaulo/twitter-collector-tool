import json

class Report:
    def load_json_report(self, dic,name):
        dic = open('tweetcollector/'+name,'w').write(json.dumps(dic, ensure_ascii=False))
        return dic

    def save_report(self, query, count):
        try:
            with open('tweetcollector/dicionario.json', 'r') as file_json:
                dic = json.loads(file_json.read())
            try:
                dic[query]['count'] = count
                dic = self.load_json_report(dic, 'dicionario.json')
            except:
                dic[query] = {'count':count}
                dic = self.load_json_report(dic, 'dicionario.json')
        except:
            dic = {}
            dic = self.load_json_report(dic,'dicionario.json')
            self.save_report(query,count)
