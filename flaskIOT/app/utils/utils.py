from datetime import datetime
from os import getenv
import random

class Utils:
    def __init__(self):
        #self.key = getenv['POST_SECRET_KEY']
        self.key = "maybesupersecretkey"

    def randomTime(n: int):
        time_string = []
        
        # (24*60*60) = 86400 H/M/S
        # (30*12) = 360 Y/M/D
        for i in range(n):
            rtime = int(random.random()*86400)
            dtime = int(random.random()*360)

            year = datetime.now().date().strftime("%Y")
            month = int(dtime/12)
            day = int((dtime - month*12)/30)
            hours   = int(rtime/3600)
            minutes = int((rtime - hours*3600)/60)
            seconds = rtime - hours*3600 - minutes*60

            time_string.append('%02d:%02d:%02d:%02d:%02d:%02d' % (day, month, year, hours, minutes, seconds))
        
        return time_string
    
    @property
    def get_universal_time(self):
        return datetime.utcnow()
    
    @property
    def get_local_time(self):
        return datetime.now()

    @property
    def get_timestamp(self):
        return datetime.timestamp(datetime.now())

    @property
    def get_post_key(self):
        return self.key