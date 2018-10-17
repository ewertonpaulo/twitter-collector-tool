import random
from src.senticnet_instance import adjetivos
from src.collector import collect

word = random.choice(adjetivos())

collect(word)