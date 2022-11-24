from .tables import *
from .tables import faker_data as faker
from flask import render_template, request, jsonify, Blueprint
from .__init__ import db
from sqlalchemy import insert

database_blueprint = Blueprint('database', __name__, template_folder='templates')

@database_blueprint.errorhandler(404)
def page_not_found(error):
    return 'Errore', 404

@database_blueprint.route('/')
def testoHTML():
    
    db.create_all()
        
    if request.accept_mimetypes['application/json']:
        return jsonify({'text':'Valori rilevati'}), '200 OK'
    else:
        return '<h1>Valori rilevati</h1>'

#STAMPA INFORMAZIONI BIDONE
@database_blueprint.route('/items', methods=['GET'])
def stampaitems():
    try:
        elenco=BinRecord.query.order_by(BinRecord.id.desc()).all() #BinRecord.query.all() --> ritorna l'intero contenuto della tabella
    except:
        db.create_all()
        fakeBin = BinRecord(1)
        db.session.add(fakeBin)
        db.session.commit()        
    return render_template('listitems.html', lista=elenco)

#STAMPA UTENTI
@database_blueprint.route('/users', methods=['GET'])
def stampausers():
    elenco=User.query.all()
    return render_template('listausers.html', lista=elenco)


#AGGIUNTA DI INFORMAZIONI FAKE SUL BIDONE
@database_blueprint.route('/addfakeitem', methods=['POST','GET'])
def addfakeitem():
    
    
    #BinGroup
    bg1 = BinGroup()
    
    db.session.add(bg1)
    
    # Admin
    ad1 = Admin(
        Person(
        username="rossi1",
        name="Mario",
        surname="Rossi",
        password="ilovecondomini",
        city="Modena",
        birth_year=2000)
    )
    
    db.session.add(ad1)
    
    # Apartments
    ap1 = Apartment(
        apartment_name="Fermi",
        city="Modena",
        street="via Garibaldi",
        apartment_street_number=1,
        n_internals=155,
        associated_bingroup=0,
        associated_admin='rossi1')
    
    db.session.add(ap1)
    
    db.session.commit()
    
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
    if(status_attuale==3 and float(riempimento_attuale)>=0.9):status_attuale=4
    if(status_attuale==2 and float(riempimento_attuale)<0.9): status_attuale=1
    if(status_attuale==4 and float(riempimento_attuale)<0.9):status_attuale=3

    #   sf = BinRecord(id_bin, status_attuale, temperature, humidity, co2, str(riempimento))
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
