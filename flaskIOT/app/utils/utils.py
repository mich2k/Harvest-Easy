from datetime import datetime


class Utils:
    def __init__(self):
        self.key = "maybesupersecretkey"

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