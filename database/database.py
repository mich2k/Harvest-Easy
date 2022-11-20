# sample11
# objects
#pip install flask-sqlalchemy


from flask import Flask
from config import Config
from flask import render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

appname = "SmartBin"
app = Flask(appname)
myconfig = Config
app.config.from_object(myconfig)

# db creation
db = SQLAlchemy(app)


class Bin(db.Model):
    __tablename__='bin'
    id = db.Column('id', db.String, primary_key=True) 
    idcondominio = db.Column('condominio_id', db.Integer, default="SmartApartment")
    id_bin = db.Column('bin_id', db.String) 
    status = db.Column('status', db.Integer)  #1: integro e non-pieno, 2: integro e pieno, 3: manomesso e non-pieno, 4: manomesso e pieno
    temperature = db.Column('temperature', db.Integer, nullable=False)
    umidità = db.Column('umidità', db.Integer, nullable=False)
    co2 = db.Column('co2', db.Integer, nullable=False)
    riempimento = db.Column('livello_di_riempimento', db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False,  default=datetime.utcnow)


    def __init__(self, id_bin, status, temperature, umidità, co2, riempimento):
        self.id_bin = id_bin
        self.status = status
        self.temperature = temperature
        self.umidità = umidità
        self.co2 = co2
        self.riempimento = riempimento

class Utente(db.Model):
    __tablename__='utente'
    username = db.Column('username', db.String, primary_key=True, nullable=False)
    idcondominio = db.Column('condominio_id', db.String, primary_key=True, default="SmartApartment")
    UID = db.Column('UID', db.String, nullable=False)

    def __init__(self, username, UID):
        self.UID=UID
        self.username=username



@app.errorhandler(404)
def page_not_found(error):
    return 'Errore', 404

@app.route('/')
def testoHTML():
    if request.accept_mimetypes['application/json']:
        return jsonify({'text':'Valori rilevati'}), '200 OK'
    else:
        return '<h1>Valori rilevati</h1>'

#STAMPA INFORMAZIONI BIDONE
@app.route('/items', methods=['GET'])
def stampaitems():
    elenco=Bin.query.order_by(Bin.id.desc()).all() #Bin.query.all() --> ritorna l'intero contenuto della tabella
    return render_template('listaitems.html', lista=elenco)

#STAMPA UTENTI
@app.route('/users', methods=['GET'])
def stampausers():
    elenco=Utente.query.all()
    return render_template('listausers.html', lista=elenco)

#AGGIUNTA DI INFORMAZIONI SUL BIDONE
@app.route('/additem', methods=['POST'])
def additem():
    status_attuale=1 #-->quando non ci sono istanze nella tabella
    bin_attuale=Bin.query.all()
    
    if(len(bin_attuale)>0): 
        status_attuale=bin_attuale[0].status
    
    msg = request.get_json()
    id_bin = msg['idbin']
    temperature = msg['temperature']
    umidità = msg['humidity']
    co2 = msg['co2']
    riempimento = msg['riempimento']

    if(status_attuale==1 and float(riempimento)>=0.9): status_attuale=2
    if(status_attuale==3 and float(riempimento)>=0.9):status_attuale=4
    if(status_attuale==2 and float(riempimento)<0.9): status_attuale=1
    if(status_attuale==4 and float(riempimento)<0.9):status_attuale=3

    sf = Bin(id_bin, status_attuale, temperature, umidità, co2, str(riempimento))

    db.session.add(sf)
    db.session.commit()
    return str(sf.id)

#AGGIUNTA DI UN UTENTE
@app.route('/adduser', methods=['POST'])
def adduser():
    username=request.args.get('username')
    UID=request.args.get('UID')

    sf = Utente(username, UID)

    db.session.add(sf)
    db.session.commit()
    return str(sf.username)

#CONTROLLA UTENTE
@app.route('/checkUID/<string:UID>', methods=['GET'])
def checkUID(UID):
    users=Utente.query.all()
    
    if(len(users)>0): 
        for user in users:
            if(UID==user.UID): return user.username, '200 OK'
    return '201 ERRORE' 



if __name__ == '__main__':

    with app.app_context():
        #Utente.__table__.drop(db.engine)
        db.create_all()

    port = 80
    interface = '0.0.0.0'
    app.run(host=interface,port=port)