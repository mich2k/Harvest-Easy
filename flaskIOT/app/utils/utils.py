from datetime import datetime
from os import getenv
import random

class Utils:
    def __init__(self):
        #self.key = getenv['POST_SECRET_KEY']
        self.key = "maybesupersecretkey"

    def randomTime():
        # generate random number scaled to number of seconds in a day
        # (24*60*60) = 86,400

        rtime = int(random.random()*86400)

        hours   = int(rtime/3600)
        minutes = int((rtime - hours*3600)/60)
        seconds = rtime - hours*3600 - minutes*60

        time_string = '%02d:%02d:%02d' % (hours, minutes, seconds)
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