from senticnet.senticnet import SenticNet
import codecs
from auth import sentiment_boolean

class Sentiment():
    def sentiment_avg(self,text):
        if sentiment_boolean == False:
            return True
        sn = SenticNet('pt')
        list_polarity = []
        qtd_words = len(text)
        temp = text.split()
        avg_n = 0
        for i in range(len(temp)):
            try:
                polarity_value = sn.polarity_value(self.treatment_string(temp[i]))
                list_polarity.append(polarity_value)
            except:
                qtd_words-=1
                i+=1

        avg_n = self.avg(list_polarity, qtd_words)
        if avg_n > 0.003 or avg_n < -0.003:
            return True
        else:
            return False
            
    def avg(self,lst, size):
        return sum(lst) / size

    def treatment_string(self,string):
        string = string.lower()
        sign = ['.',',','!','?','(',')','´','*','#','@',';',':']
        for i in sign:
            try:
                string = string.replace(i,'')
                return string
            except:
                pass

    def adjectives(self):
        dir_ = 'tweetcollector/layout-one.txt'
        data = codecs.open(dir_,'r','utf8')
        list = data.readline()
        data.close()
        return list.split(',')
