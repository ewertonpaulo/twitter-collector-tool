from senticnet.senticnet import SenticNet

def sentiment(text, partial_classification):
    sn = SenticNet('pt')
    value = 0
    list_polarity = []
    list_avg = {'psv' : [0.01], 'ngt' : [-0.01]}
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
    if avg_n > 0 and avg_n > list_avg['psv'][0]:
        partial_classification = 'partial_positive %s' %avg_n
        return partial_classification
    if avg_n < 0 and avg_n < list_avg['ngt'][0]:
        partial_classification = 'partial_negative %s' %avg_n
        return partial_classification
    else:
        partial_classification = 'partial_neutral %s' %avg_n
        return partial_classification
        
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
