from ..utils import utils
from .tables import BinRecord
from datetime import datetime, timedelta
import random


sample = {
    "status": 1,
    "temperature": 0,  # randomvalue
    "humidity": 0,  # randomvalue
    "riempimento": 0.0,  # randomvalue
    "id_bin": 1,  # randomvalue
    "timestamp": "0",
}

threshold = 0.8


def faker_instances():

    # Campiono un bidone a caso
    selected_bin = sample["id_bin"] = utils.Utils.get_random_int(2, 8)

    # Prelevo l'ultima istanza del bin selezionato casualmente
    act_record = (
        BinRecord.query.filter(BinRecord.associated_bin == selected_bin)
        .order_by(BinRecord.timestamp.desc())
        .first()
    )

    act_filling = (
        BinRecord.query.filter(BinRecord.associated_bin == selected_bin)
        .order_by(BinRecord.riempimento.desc())
        .first()
    )

    # Campiono
    # TODO:  il livello di riempimento deve essere progressivo quindi quello iniziale deve essere molto basso ed
    #       il prossimo deve essere dato dal livello precedente + una costante pseudo-lineare

    next_timestamp = utils.Utils.randomTime(
        rdm=False) if act_record is None else utils.Utils.randomTime()
    next_filling = act_filling.riempimento + utils.Utils.get_limited_random(
        0.1, 0.2) if act_filling is not None else utils.Utils.get_limited_random(0, 0.1)
    next_status = 1

    if act_record is not None:
        diff = datetime.strptime(act_record.timestamp, "%Y-%m-%d %H:%M:%S") - \
            datetime.strptime(next_timestamp, "%Y-%m-%d %H:%M:%S")

        while diff > timedelta(hours=1, days=1):
            next_timestamp = utils.Utils.randomTime()
            diff = datetime.strptime(act_record.timestamp, "%Y-%m-%d %H:%M:%S") - \
                datetime.strptime(next_timestamp, "%Y-%m-%d %H:%M:%S")

        # Mi mantengo nello stato attuale
        if act_record.status == 1 and next_filling < threshold:
            next_status = act_record.status

        if act_record.status == 2 and next_filling >= threshold:
            next_status = 1
            next_filling = 0

        # cambio stato
        if act_record.status == 2 and next_filling < threshold:
            next_status = 1

        if act_record.status == 1 and next_filling >= threshold:
            next_status = 2

        if next_filling - act_filling.riempimento > 0.6:
            next_filling /= 2

    if next_filling > 1 and next_status == 2:
        next_filling = 0
        next_status = 1

    sample["riempimento"] = next_filling
    sample["status"] = next_status
    sample["timestamp"] = next_timestamp
    sample["temperature"] = random.randrange(10, 25)
    sample["humidity"] = random.randrange(40, 90)
    return sample
