from ..utils import utils
import random

sample = {'status': 1, 
          'temperature': 0, #randomvalue
          'humidity': 0, #randomvalue
          'co2': 0, #randomvalue in ppm
          'riempimento':0.0, #randomvalue
          'associated_bin':1, #randomvalue 
          'timestamp':'0'}

def faker_instances():
    sample['temperature'] = int(random.random()*25)
    sample['humidity'] = int(random.random()*90)
    sample['riempimento'] = random.random()
    sample['associated_bin'] = random.randint(1, 8)
    sample['timestamp'] = utils.Utils.randomTime() 

    return sample