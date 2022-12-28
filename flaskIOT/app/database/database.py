from flask import render_template, request, Blueprint
from app.database.tables import *
from .faker import create_faker
from .record_faker import faker_instances
from .__init__ import db
import requests
import datetime
from os import getenv
HERE_API_KEY = getenv('HERE_KEY')
WEATHER_KEY = getenv('WEATHER_KEY')

database_blueprint = Blueprint('database', __name__, template_folder='templates', url_prefix='/db')

#CREA IL DB A RUNTIME, SE GIà PRESENTE DROPPA TUTTE LE TABLES
#È LA PRIMA ROUTE DA RAGGIUNGERE QUANDO SI AVVIA IL SISTEMA
@database_blueprint.route('/')
def createDB():
    db.drop_all()
    db.create_all()
    create_faker(db)
    faker_instances(db)
    return 'Done'

#AGGIUNTA DI INFORMAZIONI SUL BIDONE
#Le informazioni saranno inviate mediante JSON ogni N secondi.
@database_blueprint.route('/addrecord', methods=['POST'])
def addrecord():
    msgJson = request.get_json()
    status=calcolastatus(msgJson["id_bin"], msgJson["riempimento"], msgJson["roll"], msgJson["pitch"])
    msgJson["status"]=status

    try:
        sf = BinRecord(msgJson)
        db.session.add(sf)
        db.session.commit()
    except:
        return 'Error'
    return 'Done'

#AGGIUNTA DI UN BIDONE
@database_blueprint.route('/addbin', methods=['POST'])
def addbin():
    msgJson = request.get_json()

    try:
        sf = Bin(msgJson)
        db.session.add(sf)
        db.session.commit()
    except:
        return 'Error'
    return 'Done'

#ACCESSO DI UN UTENTE AL BIDONE
@database_blueprint.route('/checkOp/<string:uid>&<int:id_bin>', methods=['GET'])
@database_blueprint.route('/checkAdmin/<string:uid>', methods=['GET'])
@database_blueprint.route('/checkUser/<string:uid>&<string:apartment>', methods=['GET'])
def checkUser(uid, id_bin):
    users=User.query.all()
    
    if(len(users)>0): 
        for user in users:
            if(uid == user.uid): return user.uid, '200 OK'
            
    return '201 ERRORE' 

#AGGIUNTA DI UN USER
@database_blueprint.route('/adduser', methods=['POST'])
def adduser():
    msgJson = request.get_json()
    user = User(Person(uid=msgJson['uid'], 
                   name=msgJson['name'], 
                   surname=msgJson['surname'],
                   password=msgJson['password'], 
                   city=msgJson['city'], 
                   birth_year=msgJson['year']),
                apartment_ID=msgJson['apartment_ID'],
                internal_number=msgJson['internal_number'])
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return 'Error'
    return 'OK'

#AGGIUNTA DI UN ADMIN
@database_blueprint.route('/addadmin', methods=['POST'])
def addadmin():
    msgJson = request.get_json()
    admin = Admin(Person(uid=msgJson['uid'], 
                   name=msgJson['name'], 
                   surname=msgJson['surname'],
                   password=msgJson['password'], 
                   city=msgJson['city'], 
                   birth_year=msgJson['year']))
    try:
        db.session.add(admin)
        db.session.commit()
    except:
        return 'Error'
    return 'Done'

#AGGIUNTA DI UN OPERATORE
@database_blueprint.route('/addoperator', methods=['POST'])
def addoperator():
    msgJson = request.get_json()
    print(msgJson)
    operator = Operator(id=msgJson['id'])
    try:
        db.session.add(operator)
        db.session.commit()
    except:
        return 'Error'
    return 'Done'
  
#AGGIUNTA DI UN APARTMENT
#inserire qui lat e long dell'appartamento tramite chiamata ad API
#da verificare chiamata ad API
@database_blueprint.route('/addapartment', methods=['POST'])
def addapartment():
    msgJson = request.get_json()
    HERE_API_URL = f'https://geocode.search.hereapi.com/v1/geocode'
    address = msgJson['city'] + msgJson['street'] + str(msgJson['street_number'])
    params = {
        'q': address + 'italia', 
        'apiKey': HERE_API_KEY
    }

    req = requests.get(HERE_API_URL, params=params)
    result = req.json()
    # Use the first result
    lat = result['items'][0]['position']['lat']
    lng = result['items'][0]['position']['lng']
    
    apartment = Apartment(apartment_name=msgJson['apartment_name'], 
                          city=msgJson['city'], 
                          street=msgJson['street'], 
                          lat=lat,
                          lng=lng,
                          apartment_street_number=msgJson['street_number'], 
                          n_internals=msgJson['n_internals'],  
                          associated_admin=msgJson['associated_admin'])
    
    try:
        db.session.add(apartment)
        db.session.commit()
    except:
        return 'Error'
    return 'Done'


#Print tables
@database_blueprint.route('/items', methods=['GET'])
def stampaitems():
    
    elenco=[Bin.query.order_by(Bin.id_bin.desc()).all(),
            Apartment.query.order_by(Apartment.apartment_name.desc()).all(),
            User.query.order_by(User.uid.desc()).all(),
            Admin.query.order_by(Admin.uid.desc()).all(),
            BinRecord.query.order_by(BinRecord.id.desc()).all()] 
    
    return render_template('listitems.html', listona=elenco)


def calcolastatus(id_bin, riempimento, roll, pitch): 
    soglie={"plastica": 0.9, "carta": 0.9, "vetro": 0.8, "umido": 0.7} #soglie fisse
    dd_umido={"medie": 5, "alte": 3, "altissime": 2} #soglia dinamica per l'organico in base alla temperatura
    
    status_attuale=1 #default del primo record del bidone
    bin_attuale=BinRecord.query.filter(BinRecord.id_bin == id_bin)
    if(bin_attuale.count()): 
        status_attuale= (BinRecord.query.filter(BinRecord.id_bin == id_bin).order_by(BinRecord.timestamp.desc()).first()).status

    tipologia = (Bin.query.filter(Bin.id_bin == id_bin)).first().tipologia
    soglia_attuale=0
    if (tipologia=="umido"):
        now = datetime.datetime.now()
        mese=now.month  
        if(mese>=4 and mese<=10): #mesi caldi
            apartment_ID=(Bin.query.filter(Bin.id_bin == id_bin)).first().apartment_ID
            lat=(Apartment.query.filter(Apartment.apartment_name==apartment_ID)).first().lat
            lon=(Apartment.query.filter(Apartment.apartment_name==apartment_ID)).first().lng
            
            WEATHERE_API_URL = f'https://api.openweathermap.org/data/2.5/weather'
            params = {
                'lat':lat,
                'lon':lon,
                'appid': WEATHER_KEY
            }
            req = requests.get(WEATHERE_API_URL, params=params)
            res = req.json()
            temp = int(res['main']['temp']-272.15) #conversione kelvin-celsius

            dd_time=0
            if(temp>=20 and temp<=25): #medie
                dd_time=dd_umido["media"]
            if(temp>25 and temp<=30): #alte
                dd_time=dd_umido["alte"]
            if(temp>30): #altissime
                dd_time=dd_umido["altissime"]

            timestamp=Bin.query.filter(Bin.id_bin==id_bin).first().ultimo_svuotamento
            last_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.now()
            if((now-last_date).days>dd_time and dd_time>0): #temperature alte + sono passo più di deltagiorni
                soglia_attuale=0
            else:
                soglia_attuale=soglie["umido"]
        else:
            soglia_attuale=soglie["umido"]
    elif(tipologia=='plastica'):
        soglia_attuale=soglie["plastica"]
    elif(tipologia=='carta'):
        soglia_attuale=soglie["carta"]
    elif(tipologia=='vetro'):
        soglia_attuale=soglie["vetro"]

    # 1: integro e non-pieno, 2: integro e pieno, 3: manomesso e non-pieno, 4: manomesso e pieno
    #passaggio da pieno a non pieno e viceversa
    if(status_attuale==1 and float(riempimento)>=soglia_attuale): 
        #SEGNALAZIONE AD HERA
        status_attuale=2
    if(status_attuale==3 and float(riempimento)>=soglia_attuale): 
        #SEGNALAZIONE AD HERA
        status_attuale=4
    if(status_attuale==2 and float(riempimento)<soglia_attuale): 
        status_attuale=1
        db.session.query(Bin).filter(Bin.id_bin == id_bin).update({'ultimo_svuotamento': datetime.datetime.now()})
        db.session.commit()
       
    if(status_attuale==4 and float(riempimento)<soglia_attuale):
        status_attuale=3
        db.session.query(Bin).filter(Bin.id_bin == id_bin).update({'ultimo_svuotamento': datetime.datetime.now()})
        db.session.commit()

    #passaggio da accappottato a dritto e viceversa
    if(status_attuale==3 and (roll<45 and (abs(pitch)-90)<45)): status_attuale=1
    if(status_attuale==1 and (roll>=45 or (abs(pitch)-90)>=45)): 
        #SEGNALAZIONE CAPOTTAMENTO
        status_attuale=3
    if(status_attuale==4 and (roll<45 and (abs(pitch)-90)<45)): status_attuale=2
    if(status_attuale==2 and (roll>=45 or (abs(pitch)-90)>=45)): 
        #SEGNALAZIONE CAPOTTAMENTO
        status_attuale=4

    return status_attuale

def getstringstatus(status):
    if(status==1):
        return "integro e non-pieno"
    elif(status==2):
        return "integro e pieno"
    elif(status==3):
        return "manomesso e non-pieno"
    elif(status==4):
        return "manomesso e pieno"
    else:
        return "Error"
    