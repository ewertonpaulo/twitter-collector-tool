import random
from collector.senticnet_instance import adjetivos
from collector.collector import collect


collect(random.choice(adjetivos()))