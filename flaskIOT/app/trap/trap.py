from flask import Blueprint, request
from ..database import tables


trap_blueprint = Blueprint('trap', __name__)
#Ricevo il dato, ottengo l'id e modifico lo status


@trap_blueprint.route('/full')
def change_status_f():
    msgJson = request.get_json()
    tables.BinRecord.query()
    


@trap_blueprint.route('/rigged')
def change_status_r():
    msgJson = request.get_json()



"""
    status_attuale=1 #-->quando non ci sono istanze nella tabella
    
    bin_attuale=BinRecord.query.all()
    
    if(len(bin_attuale)>0): 
        status_attuale=bin_attuale[0].status
    
    riempimento_attuale=msgJson['riempimento']

    if(status_attuale==1 and float(riempimento_attuale)>=0.9): status_attuale=2
    if(status_attuale==3 and float(riempimento_attuale)>=0.9): status_attuale=4
    if(status_attuale==2 and float(riempimento_attuale)<0.9): status_attuale=1
    if(status_attuale==4 and float(riempimento_attuale)<0.9): status_attuale=3"""