from ..utils import utils
from .tables import Bin, BinRecord
from datetime import datetime
import random

sample = {'status': 1, 
          'temperature': 0, #randomvalue
          'humidity': 0, #randomvalue
          'riempimento':0.0, #randomvalue
          'associated_bin':1, #randomvalue 
          'timestamp':'0'}

threshold = 0.9

def faker_instances(db):
    #Campiono un bidone a caso
    selected_bin = sample['associated_bin'] = utils.Utils.get_random_int(1,8)
    
    #Prelevo l'ultima istanza del bin selezionato casualmente
    act_timestamp = db.session.query(BinRecord.timestamp).filter(BinRecord.associated_bin == selected_bin).order_by(BinRecord.timestamp.desc()).first()
    act_filling =   db.session.query(BinRecord.riempimento).filter(BinRecord.associated_bin == selected_bin).order_by(BinRecord.riempimento.desc()).first()
    act_state =     db.session.query(BinRecord.status).filter(BinRecord.associated_bin == selected_bin).order_by(BinRecord.status.desc()).first()    
    
    #Campiono
    next_timestamp = utils.Utils.randomTime()
    next_filling = utils.Utils.get_random()
    next_status = 1
    
    if act_timestamp is not None and act_filling is not None and act_state is not None:
        while(True):

            if datetime.strptime(next_timestamp, "%Y-%m-%d %H:%M:%S") > datetime.strptime(act_timestamp[0], "%Y-%m-%d %H:%M:%S"):
                next_timestamp = utils.Utils.randomTime()
                continue
            
            if next_filling > act_filling[0]:

                #Mi mantengo nello stato attuale
                if (act_state == 1 and next_filling < threshold) or (act_state == 2 and next_filling >= threshold):
                    next_status = act_state
                    break
                
                else:
                    if act_state == 2 and next_filling < threshold:
                        next_status = 1
                    if act_state == 1 and next_filling >= threshold:
                        next_status = 2
                    break
            else:
                next_filling = utils.Utils.get_random()
            

    sample['riempimento'] = next_filling
    sample['status'] = next_status
    sample['timestamp'] = next_timestamp
    sample['temperature'] = random.randrange(10,25)
    sample['humidity'] = random.randrange(40,90)
    return sample