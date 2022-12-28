from .tables import BinRecord
from ..utils import utils
from random import randrange, randint

sample = {'status': 1, 
          'temperature': 0, #randomvalue
          'humidity': 0, #randomvalue
          'co2': 0, #randomvalue in ppm
          'riempimento':0.0, #randomvalue
          'associated_bin':1, #randomvalue 
          'timestamp':'0'}

records = []

def faker_instances(db):
    
    for i in range(90):
        sample['temperature'] = randrange(10, 25)
        sample['humidity'] = randrange(40, 90)
        sample['co2'] = randrange(600, 2500)
        sample['riempimento'] = randrange(0, 1)
        sample['timestamp'] = utils.Utils.randomTime() 
        records.append(sample)

    for record in records:    
        db.session.add(BinRecord(record))

    db.session.commit()
    return True