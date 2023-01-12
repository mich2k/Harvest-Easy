from datetime import datetime
from os import getenv
import random

class Utils:
    def __init__(self):
        #self.key = getenv['POST_SECRET_KEY']
        self.key = "maybesupersecretkey"

    def randomTime(rdm = True):        
        # (24*60*60) = 86400 H/M/S
        # (30*12) = 360 Y/M/D
        if rdm:
            rtime = int(random.random()*86400)
            dtime = int(random.random()*360)

            year = random.randrange(2022, 2050)
            month = int(dtime/30) if int(dtime/30) != 0 else int(dtime/30) + 1
            day = int(dtime/12) if int(dtime/12) != 0 else int(dtime/12) + 1
            hours   = int(rtime/3600)
            minutes = int((rtime - hours*3600)/60)
            seconds = rtime - hours*3600 - minutes*60
            time_string = '%s-%d-%d %02d:%02d:%02d' % (year, month, day, hours, minutes, seconds)
        else:
            time_string = str(datetime.utcnow().replace(microsecond=0))
        return time_string
    
    def get_random_int(low: int, upper: int):
        return random.randint(low, upper)
    
    def get_random():
        return random.random()

    @property
    def get_local_time(self):
        return datetime.now()
    
    @property
    def get_timestamp(self):
        return datetime.timestamp(datetime.now())

    @property
    def get_post_key(self):
        return self.key