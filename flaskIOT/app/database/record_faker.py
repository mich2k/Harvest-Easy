from ..utils import utils
from .tables import Bin, BinRecord
from datetime import datetime
import random

sample = {
    "status": 1,
    "temperature": 0,  # randomvalue
    "humidity": 0,  # randomvalue
    "riempimento": 0.0,  # randomvalue
    "id_bin": 1,  # randomvalue
    "timestamp": "0",
}

threshold = 0.9


def faker_instances():
    # Campiono un bidone a caso
    selected_bin = sample["id_bin"] = utils.Utils.get_random_int(1, 8)

    # Prelevo l'ultima istanza del bin selezionato casualmente
    act_record = (
            BinRecord.query.filter(BinRecord.associated_bin == selected_bin)
            .order_by(BinRecord.timestamp.desc())
            .first()
        )

    # Campiono
    next_timestamp = utils.Utils.randomTime()
    next_filling = utils.Utils.get_random()
    next_status = 1

    if act_record is not None: 
        while True:
            if datetime.strptime(
                next_timestamp, "%Y-%m-%d %H:%M:%S"
            ) > datetime.strptime(act_record.timestamp, "%Y-%m-%d %H:%M:%S"):
                next_timestamp = utils.Utils.randomTime()
                continue
            
            # Mi mantengo nello stato attuale
            if (act_record.status == 1 and next_filling < threshold) or (
                act_record.status == 2 and next_filling >= threshold
            ):
                next_status = act_record.status
                break

            #cambio stato
            if act_record.status == 2 and next_filling < threshold:
                next_status = 1
            if act_record.status == 1 and next_filling >= threshold:
                next_status = 2
            break
    else:
        if(next_filling >= threshold):
            next_status=2


    sample["riempimento"] = next_filling
    sample["status"] = next_status
    sample["timestamp"] = next_timestamp
    sample["temperature"] = random.randrange(10, 25)
    sample["humidity"] = random.randrange(40, 90)
    return sample
