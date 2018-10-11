import random
from senticnet_instance import adjetivos
from coletor import collect

list=[]
while True:
    try:
        collect(random.choice(adjetivos(list)))
    except:
        continue