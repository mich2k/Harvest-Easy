import requests
import json
from app.database.tables import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from os import getenv

TOKEN = getenv("TG_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

# Filled or Overturned or Fired Bin


def report(idbin, db, filling=None, coord=None, co2=None):

    if idbin is None:
        raise Exception('idbin in trap Modulo is None')

    apartment = Bin.query.where(Bin.id_bin == idbin).first().apartment_ID
    
    text = f"Attenzione! Anomalia nel bidone {Bin.query.where(Bin.id_bin == idbin).first().tipologia}:"
    event = 'Bidone:'
    
    # Costruisco il testo da notificare a User ed Admin
    if filling is not None:
        text += f"\n- Livello di riempimento del bidone: {str(filling)}"
        event += ' pieno'
    if coord is not None:
        text += "\n- Bidone rovesciato"
        event += ' rovesciato'
    if co2 is not None:
        text += f"\n- Rilevata elevata quantità di CO2 nel bidone({co2}).\nPossibile incendio in corso"
        event += ' in fiamme'
    
    keyboard = [[InlineKeyboardButton("Risolto", callback_data='solved')],
            [InlineKeyboardButton("Segnala", callback_data='report')]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    data = {"chat_id": '',
            'text': text,
            'reply_markup': json.dumps(reply_markup.to_dict())}
    
    # Contattare getneighbor : via, nome dell'appartamento, città e tipologia rifiuto
    sq = db.session.query(User.username).where(User.apartment_ID == apartment)
    
    chat_ids = db.session.query(UserTG.id_chat).filter(UserTG.associated_user.in_(sq)).all()
    
    #TODO: aggiungere amministratori condominiali UserTG.associated_user.in_(Apartment.query.filter(Apartment.apartment_name == apartment))).all()
            
    for chat_id in chat_ids:

        data['chat_id'] = chat_id
        
        # Mandare la segnalazione a tutti gli utenti e all'amministratore
        print(URL)
        requests.post(URL + f"sendMessage", data=data)

    db.session.add(AlterationRecord(type_of_event=event, is_notified=True, associated_bin=idbin))
    db.session.commit()
    