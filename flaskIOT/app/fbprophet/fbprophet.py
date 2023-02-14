from flask import Blueprint, jsonify
from itertools import zip_longest
from app.database.tables import BinRecord, Bin
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import csv
from flasgger import swag_from

fbprophet_blueprint = Blueprint(
    "fbprophet", __name__, template_folder="templates", url_prefix="/pred"
)


@fbprophet_blueprint.route("/")
def main():
    return "<h1>FbProphet</h1>"

def getprevision(apartment_name=None, tipologia=None):

    if tipologia is not None and apartment_name is not None:
        if Bin.query.filter(Bin.tipologia==tipologia).filter(Bin.apartment_ID == apartment_name).first() == None:
            return jsonify({"error": "tipology or apartment name not valid"}), 401
        
    if apartment_name is not None:
        if Bin.query.filter(Bin.apartment_ID == apartment_name).first() == None:
            return jsonify({"error": "Apartment name not valid or it doesn't have any bin"}), 401
        
    array_pred=[]

    if tipologia is None and apartment_name is None:
        bins = Bin.query.all()
    if tipologia is not None:
        bins = Bin.query.filter(Bin.tipologia==tipologia)
    if apartment_name is not None:
        bins = Bin.query.filter(Bin.apartment_ID == apartment_name)
    if apartment_name is not None and tipologia is not None:
        bins=Bin.query.filter(Bin.apartment_ID == apartment_name).filter(Bin.tipologia==tipologia)
    
    for bin in bins:  
        file = pd.read_csv(
            "./predictions_file/%s/prediction_%s.csv"
            % (bin.apartment_ID, bin.tipologia)
        )
        predictions = file["yhat"] 
        dates = pd.to_datetime(file["ds"]) 

        json_bin={"bin": bin.id_bin, "tipologia": bin.tipologia, "apartment": bin.apartment_ID, "previsioni": None}

        values_and_dates=[]
        for i in range(len(predictions)):
            array={}
            array["value"]= predictions[i]
            array["date"]= dates[i]
            values_and_dates.append(array)
        json_bin["previsioni"]=values_and_dates
        array_pred.append(json_bin)

    return jsonify({"fbprophet": array_pred}), 200

def createprevision(time, apartment_name=None, tipologia=None):
    
    if time < 0:
        return jsonify({"error": "time not correct"}), 401
    
    if apartment_name is not None:
        if tipologia is not None:
            if Bin.query.filter(Bin.tipologia==tipologia).filter(Bin.apartment_ID == apartment_name).first() == None:
                return jsonify({"error": "Apartment or tipology not valid"}), 402
        if Bin.query.filter(Bin.apartment_ID == apartment_name).first() == None:
                return jsonify({"error": "Apartment not valid"}), 403
    
    if time == 0:   #se tempo non inserito(0), default 5 giorni
        time = 5
    bins = None
    if apartment_name is None and tipologia is None: 
        bins = Bin.query.all()
    if apartment_name is not None:
        if tipologia is not None:
            bins = Bin.query.filter(Bin.tipologia==tipologia).filter(Bin.apartment_ID == apartment_name)
        else: 
            bins = Bin.query.filter(Bin.apartment_ID == apartment_name)

    for bin in bins:  # per ogni bidone creo una previsione temporale
        bin_records = BinRecord.query.filter(
            BinRecord.associated_bin == bin.id_bin
        ).order_by(BinRecord.timestamp.desc())[:50]
        apartment_name = bin.apartment_ID
        tipologia = bin.tipologia

        if len(bin_records) >= 2:
            timestamps = []
            filling = []
            for bin_record in bin_records:
                timestamps.append(bin_record.timestamp)
                filling.append(bin_record.riempimento)

            with open(
                "./predictions_file/%s/riempimento_%s.csv"
                % (apartment_name, tipologia),
                "w",
            ) as csvfile:
                filewriter = csv.writer(
                    csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
                )
                filewriter.writerow(["ds", "y"])
                for tp, fl in zip_longest(timestamps, filling):
                    filewriter.writerow([tp, fl])

            df = pd.read_csv(
                "./predictions_file/%s/riempimento_%s.csv"
                % (apartment_name, tipologia)
            )

            df.columns = ["ds", "y"]
            df["ds"] = pd.to_datetime(df["ds"])
            # plotting the actual values
            plt.plot(df.ds, df.y)
            plt.title(
                "Dati attuali di riempimento %s dell'appartamento %s"
                % (tipologia, apartment_name)
            )
            plt.xlabel("Data")
            plt.ylabel("Livello di riempimento")

            plt.savefig(
                "./predictions/%s/%s/dati_attuali.png"
                % (apartment_name, tipologia),
                format="png",
            )
            
            m = Prophet()
            m.fit(df)
            future = m.make_future_dataframe(periods=time, freq="d")
            future.tail()
            forecast = m.predict(future)
            forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail()
            forecast.to_csv(
                "./predictions/%s/prediction_%s.csv"
                % (apartment_name, tipologia)
            )
            
            # Plotting the generated forecast
            m.plot(forecast, uncertainty=True)
            plt.title(
                "Previsioni di riempimento %s dell'appartamento %s"
                % (tipologia, apartment_name)
            )
            plt.xlabel("Data")
            plt.ylabel("Livello di riempimento")

            plt.savefig(
                "./predictions/%s/%s/forecast.png" % (apartment_name, tipologia),
                format="png",
            )
            

            # Plotting the forecast components.
            m.plot_components(forecast)
            plt.savefig(
                "./predictions/%s/%s/components.png" % (apartment_name, tipologia),
                format="png",
            )

            """
            prediction = forecast[["yhat"]].values
            status_previsto = Utils.calcolastatus(
                Utils, bin.id_bin, prediction[0], None, None, None
            )
            
            Utils.set_previsione_status(bin.id_bin, status_previsto)
            """
            
    return jsonify({"msg": "Previsioni correttamente create"}), 200


@fbprophet_blueprint.route("/getprevision")
@swag_from('docs/predizioni.yml')
def prevision():
    """
    questo endpoint prende le previsioni temporali di riempimento dei bidoni 
    precedentemente create e ritorna un json con le relative previsioni
    """
    return getprevision(None, None)

@fbprophet_blueprint.route("/getprevision/<string:apartment_name>")
@swag_from('docs/predizioni2.yml')
def prevision2(apartment_name):
    """
    questo endpoint prende le previsioni temporali di riempimento dei bidoni di uno specifico appartamento
    precedentemente create e ritorna un json con le previsioni di tutti i bidoni dell'appartamento
    """
    return getprevision(apartment_name, None)

@fbprophet_blueprint.route("/getprevision/<string:apartment_name>&<string:tipologia>")
@swag_from('docs/predizioni3.yml')
def prevision3(apartment_name, tipologia):
    """
    questo endpoint prende le previsioni temporali di riempimento dei bidoni di uno specifico appartamento 
    e di una specifica tipologia precedentemente create e ritorna un json con le relative previsioni 
    """
    return getprevision(apartment_name=apartment_name, tipologia=tipologia)

@fbprophet_blueprint.route("/createprevision/<int:time>")
@swag_from('docs/createpredizioni.yml')
def createprevision1(time):
    """
    questo end point crea previsioni temporali di riempimento dei bidoni per un certo periodo di tempo, 
    se l'input è uguale a 0, di defaul si assume 5 giorni
    """
    return createprevision(time, None, None)

@fbprophet_blueprint.route("/createprevision/<string:apartment_name>&<int:time>")
def createprevision2(apartment_name, time):
    """
    questo end point crea previsioni temporali di riempimento dei bidoni per un certo periodo di tempo, 
    per un appartamento specifico
    se l'input è uguale a 0, di defaul si assume 5 giorni
    """
    return createprevision(time, apartment_name=apartment_name, tipologia=None)

@fbprophet_blueprint.route("/createprevision/<string:apartment_name>&<string:tipologia>&<int:time>")
@swag_from('docs/createpredizioni2.yml')
def createprevision3(apartment_name, tipologia, time):
    """
    questo end point crea previsioni temporali di riempimento dei bidoni per un certo periodo di tempo, 
    per un appartamento specifico e per una tipologia di bidoni specifica
    se l'input è uguale a 0, di defaul si assume 5 giorni
    """
    return createprevision(time, apartment_name=apartment_name, tipologia=tipologia)

