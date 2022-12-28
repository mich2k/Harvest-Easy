from .tables import BinRecord
from ..utils import utils

sample = {'status': 1, 
          'temperature': 0, #randomvalue
          'humidity': 0, #randomvalue
          'co2': 0, #randomvalue
          'riempimento':0.0, #randomvalue
          'associated_bin':1, #randomvalue 
          'timestamp':'0'}

records = []

def faker_instances(db):
    
    for i in range(90):
        sample['timestamp'] = utils.Utils.randomTime() 
        records.append(sample)

    for record in records:    
        db.session.add(BinRecord(record))

    db.session.commit()
    return True