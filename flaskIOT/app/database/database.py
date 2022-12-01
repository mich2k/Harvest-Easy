from flask import render_template, request, Blueprint
from sqlalchemy_utils.functions import database_exists
from .tables import *
from .faker import create_faker
from .__init__ import db
#from ...flasky import app


database_blueprint = Blueprint('database', __name__, template_folder='templates')

#CREA IL DB, SE GIÀ PRESENTE DROPPA TUTTO
@database_blueprint.route('/')
def createDB():
    
    db.create_all()
    create_faker(db)
    return 'Done'

#AGGIUNTA DI INFORMAZIONI SUL BIDONE
@database_blueprint.route('/additem', methods=['POST'])
def additem():
    
    status_attuale=1 #-->quando non ci sono istanze nella tabella
    
    bin_attuale=BinRecord.query.all()
    
    if(len(bin_attuale)>0): 
        status_attuale=bin_attuale[0].status
    
    msgJson = request.get_json()
    riempimento_attuale=msgJson['riempimento']

    if(status_attuale==1 and float(riempimento_attuale)>=0.9): status_attuale=2
    if(status_attuale==3 and float(riempimento_attuale)>=0.9): status_attuale=4
    if(status_attuale==2 and float(riempimento_attuale)<0.9): status_attuale=1
    if(status_attuale==4 and float(riempimento_attuale)<0.9): status_attuale=3

    #  sf = BinRecord(id_bin, status_attuale, temperature, humidity, co2, str(riempimento))
    sf = BinRecord(status_attuale, msgJson)
    db.session.add(sf)
    db.session.commit()
    return str(sf.id)

#AGGIUNTA DI UN User
@database_blueprint.route('/adduser', methods=['POST'])
def adduser():
    username=request.args.get('username')
    UID=request.args.get('UID')

    sf = User(username, UID)

    db.session.add(sf)
    db.session.commit()
    return str(sf.username)

#CONTROLLA User
@database_blueprint.route('/checkUID/<string:UID>', methods=['GET'])
def checkUID(UID):
    users=User.query.all()
    
    if(len(users)>0): 
        for user in users:
            if(UID==user.UID): return user.username, '200 OK'
            
    return '201 ERRORE' 

#STAMPA INFORMAZIONI BIDONE
@database_blueprint.route('/items', methods=['GET'])
def stampaitems():
    
    elenco=[BinGroup.query.order_by(BinGroup.id.desc()).all(),
            Apartment.query.order_by(Apartment.id.desc()).all()]
            #,BinRecord.query.order_by(BinRecord.id.desc()).all()] 
    
    return render_template('listitems.html', listona=elenco)

#STAMPA UTENTI
@database_blueprint.route('/users', methods=['GET'])
def stampausers():
    elenco=User.query.all()
    return render_template('listausers.html', lista=elenco)
