from .tables import BinRecord
from ..utils import utils

sample = {'status': 1, 
          'temperature': 23, 
          'humidity': 25, 
          'co2': 32, 
          'riempimento':34.45,
          'associated_bin':1}

timestamps = [x for x in utils.Utils.randomTime(90)]
records = []

def faker_instances(db):
    
    for timestamp in timestamps:
        records.append(sample.update('timestamp', timestamp))

    for record in records:    
        db.session.add(BinRecord(record))

    db.session.commit()
    return True