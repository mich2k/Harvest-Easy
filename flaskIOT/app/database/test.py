import random, json

def randomTime():
        # generate random number scaled to number of seconds in a day
        # (24*60*60) = 86,400

        rtime = int(random.random()*86400)

        hours   = int(rtime/3600)
        minutes = int((rtime - hours*3600)/60)
        seconds = rtime - hours*3600 - minutes*60

        time_string = '%02d:%02d:%02d' % (hours, minutes, seconds)
        return time_string

timestamps = randomTime()

fakers = [{'idbin':1,'tipologia':'carta',    'ultimo_svuotamento':timestamps[0], 'apartment_ID':'Fermi'},
          {'idbin':2,'tipologia':'plastica', 'ultimo_svuotamento':timestamps[1], 'apartment_ID':'Fermi'},
          {'idbin':3,'tipologia':'vetro',    'ultimo_svuotamento':timestamps[2], 'apartment_ID':'Fermi'},
          {'idbin':4,'tipologia':'carta',    'ultimo_svuotamento':timestamps[3], 'apartment_ID':'Torri'},
          {'idbin':5,'tipologia':'plastica', 'ultimo_svuotamento':timestamps[4], 'apartment_ID':'Torri'},
          {'idbin':6,'tipologia':'umido',    'ultimo_svuotamento':timestamps[5], 'apartment_ID':'Cuoppo'},
          {'idbin':7,'tipologia':'plastica', 'ultimo_svuotamento':timestamps[6], 'apartment_ID':'Cuoppo'},
          {'idbin':8,'tipologia':'carta',    'ultimo_svuotamento':timestamps[7], 'apartment_ID':'Cuoppo'}]
for i in range(len(fakers)):
    print(json.dumps(fakers[i]))