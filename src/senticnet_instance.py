from senticnet.senticnet import SenticNet
import codecs
from auth import sentiment_boolean

def sentiment(text):
    if sentiment_boolean == False:
        return True
    sn = SenticNet('pt')
    list_polarity = []
    l_avg = {'psv' : [0.003], 'ngt' : [-0.003]}
    qtd_words = len(text)
    temp = text.split()
    avg_n = 0
    for i in range(len(temp)):
        try:
            polarity_value = sn.polarity_value(treatment_string(temp[i]))
            list_polarity.append(polarity_value)
        except:
            qtd_words-=1
            i+=1

    avg_n = avg(list_polarity, qtd_words)
    if avg_n > l_avg['psv'][0] or avg_n < l_avg['ngt'][0]:
        return True
    else:
        return False
        
def avg(lst, size):
    return sum(lst) / size

def treatment_string(string):
    string = string.lower()
    sign = ['.',',','!','?','(',')','´','*','#','@',';',':']
    for i in sign:
        try:
            string = string.replace(i,'')
            return string
        except:
            pass

def adjectives():
    dir_ = 'src/layout-one.txt'
    data = codecs.open(dir_,'r','utf8')
    list = data.readline()
    data.close()
    return list.split()
