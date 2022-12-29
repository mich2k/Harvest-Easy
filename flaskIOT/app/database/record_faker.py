from ..utils import utils
from .tables import Bin, BinRecord
from datetime import datetime
import random

sample = {'status': 1, 
          'temperature': 0, #randomvalue
          'humidity': 0, #randomvalue
          'co2': 0, #randomvalue in ppm
          'riempimento':0.0, #randomvalue
          'associated_bin':1, #randomvalue 
          'timestamp':'0'}

threshold = 0.9

def faker_instances(db):
    #Campiono un bidone a caso
    selected_bin = sample['associated_bin'] = random.randint(1, 8)
    
    #Prelevo l'ultima istanza del bin selezionato casualmente
    act_timestamp = db.session.query(BinRecord).where(BinRecord.associated_bin == selected_bin).order_by(BinRecord.timestamp.desc())
    act_filling =   db.session.query(BinRecord).where(BinRecord.associated_bin == selected_bin).order_by(BinRecord.riempimento.desc())
    act_state =     db.session.query(BinRecord).where(BinRecord.associated_bin == selected_bin).order_by(BinRecord.status.desc())
        
    #Campiono
    next_timestamp = utils.Utils.randomTime()
    next_filling = random.random()
    next_status = 1
    
    while(True):
        
        if datetime.strptime(next_timestamp, "%Y-%m-%d %H:%M:%S") <= datetime.strptime(act_timestamp, "%Y-%m-%d %H:%M:%S"):
            next_timestamp = utils.Utils.randomTime()
        
        if next_filling > act_filling:
            
            #Mi mantengo nello stato attuale
            if (act_state == 1 and next_filling < threshold) or (act_state == 2 and next_filling >= threshold):
                next_status = act_state
                break
            else:
                if act_state == 2 and next_filling < threshold:
                    next_status = 1
                if act_state == 1 and next_filling >= threshold:
                    next_status = 2
        else:
            next_filling = random.random()

    sample['riempimento'] = next_timestamp
    sample['status'] = next_status
    sample['timestamp'] = next_filling
    sample['temperature'] = random.randrange(10,25)
    sample['humidity'] = random.randrange(40,90)

    return sample