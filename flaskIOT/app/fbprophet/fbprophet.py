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


@fbprophet_blueprint.route("/getprevision")
#@swag_from('predizioni.yml')
def getprevision():
    """
    questo endpoint prende le previsioni temporali di riempimento dei bidoni 
    precedentemente create e ritorna un json con le relative previsioni
    """
    array_pred=[]
    for bin in Bin.query.all():  
    
        apartment_name = Bin.query.filter(Bin.id_bin == bin.id_bin)[0].apartment_ID
        tipologia = Bin.query.filter(Bin.id_bin == bin.id_bin).first().tipologia

        file = pd.read_csv(
            "./app/fbprophet/predictions/%s/prediction_%s.csv"
            % (apartment_name, tipologia)
        )
        predictions = file["yhat"] 
        dates = pd.to_datetime(file["ds"]) 
    
        json_bin={"bin": bin.id_bin, "tipologia": tipologia, "apartment": apartment_name, "previsioni": None}
        
        values_and_dates=[]
        for i in range(len(predictions)):
            array={}
            array["value"]= predictions[i]
            array["date"]= dates[i]
            values_and_dates.append(array)
        json_bin["previsioni"]=values_and_dates
        array_pred.append(json_bin)

    return jsonify({"fbprophet": array_pred}), 200

@fbprophet_blueprint.route("/getprevision/<string:apartment_name>")
#@swag_from('predizioni2.yml')
def getprevision2(apartment_name):
    """
    questo endpoint prende le previsioni temporali di riempimento dei bidoni di uno specifico appartamento
    precedentemente create e ritorna un json con le previsioni di tutti i bidoni dell'appartamento
    """
    if apartment_name is None:
        return jsonify({"error": "Apartment name not correct"}), 401

    if Bin.query.filter(Bin.apartment_ID == apartment_name).first() == None:
        return jsonify({"error": "Apartment name not valid or it doesn't have any bin"}), 402

    
    array_pred=[]
    bins = Bin.query.filter(Bin.apartment_ID == apartment_name)
    for bin in bins:
        tipologia = Bin.query.filter(Bin.id_bin == bin.id_bin).first().tipologia  
        file = pd.read_csv(
            "./app/fbprophet/predictions/%s/prediction_%s.csv"
            % (apartment_name, tipologia)
        )
        predictions = file["yhat"] 
        dates = pd.to_datetime(file["ds"]) 
    
        json_bin={"bin": bin.id_bin, "tipologia": tipologia, "previsioni": None}
        
        values_and_dates=[]
        for i in range(len(predictions)):
            array={}
            array["value"]= predictions[i]
            array["date"]= dates[i]
            values_and_dates.append(array)
            
        json_bin["previsioni"]=values_and_dates
        array_pred.append(json_bin)

    return jsonify({"apartment_name": apartment_name, "previsioni_bidoni": array_pred}), 200

@fbprophet_blueprint.route("/getprevision/<string:apartment_name>&<string:tipologia>")
#@swag_from('predizioni3.yml')
def getprevision3(apartment_name, tipologia):
    """
    questo endpoint prende le previsioni temporali di riempimento dei bidoni di uno specifico appartamento 
    e di una specifica tipologia precedentemente create e ritorna un json con le relative previsioni 
    """
    if apartment_name is None or tipologia is None:
        return jsonify({"error": "Input not correct"}), 401
    
    if Bin.query.filter(Bin.tipologia==tipologia).filter(Bin.apartment_ID == apartment_name).first() == None:
        return jsonify({"error": "tipology or apartment_name not valid"}), 402

    array_pred=[]
    bins = Bin.query.filter(Bin.tipologia==tipologia).filter(Bin.apartment_ID == apartment_name)
    for bin in bins:  
        file = pd.read_csv(
            "./app/fbprophet/predictions/%s/prediction_%s.csv"
            % (apartment_name, tipologia)
        )
        predictions = file["yhat"] 
        dates = pd.to_datetime(file["ds"]) 
    
        json_bin={"bin": bin.id_bin, "previsioni": None}
        
        values_and_dates=[]
        for i in range(len(predictions)):
            array={}
            array["value"]= predictions[i]
            array["date"]= dates[i]
            values_and_dates.append(array)
        json_bin["previsioni"]=values_and_dates
        array_pred.append(json_bin)

    return jsonify({"apartment_name": apartment_name, "tipologia": tipologia, "previsioni_bidoni": array_pred}), 200


@fbprophet_blueprint.route("/createprevision/<int:time>")
@swag_from('createpredizioni.yml')
def createprevision(time):
    """
    questo end point crea previsioni temporali di riempimento dei bidoni per un certo periodo di tempo, 
    se l'input è uguale a 0, di defaul si assume 5 giorni
    """
    if time < 0:
        return jsonify({"error": "time not correct"}), 401

    if time == 0:   #se tempo non inserito(0), default 5 giorni
        time = 5
    for bin in Bin.query.all():  # per ogni bidone creo una previsione temporale
        bin_records = BinRecord.query.filter(
            BinRecord.associated_bin == bin.id_bin
        ).order_by(BinRecord.timestamp.desc())[:50]
        apartment_name = Bin.query.filter(Bin.id_bin == bin.id_bin)[0].apartment_ID
        tipologia = Bin.query.filter(Bin.id_bin == bin.id_bin).first().tipologia

        if len(bin_records) >= 2:
            timestamps = []
            filling = []
            for bin_record in bin_records:
                timestamps.append(bin_record.timestamp)
                filling.append(bin_record.riempimento)

            with open(
                "./app/fbprophet/predictions/%s/riempimento_%s.csv"
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
                "./app/fbprophet/predictions/%s/riempimento_%s.csv"
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
                "./Predizioni/%s/%s/dati_attuali.png"
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
                "./app/fbprophet/predictions/%s/prediction_%s.csv"
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
                "./Predizioni/%s/%s/forecast.png" % (apartment_name, tipologia),
                format="png",
            )
            

            # Plotting the forecast components.
            m.plot_components(forecast)
            plt.savefig(
                "./Predizioni/%s/%s/components.png" % (apartment_name, tipologia),
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

@fbprophet_blueprint.route("/createprevision/<string:apartment_name>&<string:tipologia>&<int:time>")
@swag_from('createpredizioni2.yml')
def createprevision2(apartment_name, tipologia, time):
    """
    questo end point crea previsioni temporali di riempimento dei bidoni per un certo periodo di tempo, 
    per un appartamento specifico e per una tipologia di bidoni specifica
    se l'input è uguale a 0, di defaul si assume 5 giorni
    """
    if time == 0:
        time = 5

    if apartment_name is None or tipologia is None or time < 0:
        return jsonify({"error": "Input not correct"}), 401

    if Bin.query.filter(Bin.tipologia==tipologia).filter(Bin.apartment_ID == apartment_name).first() == None:
        return jsonify({"error": "Apartment or tipology not valid"}), 402
        
    bins = Bin.query.filter(Bin.tipologia==tipologia).filter(Bin.apartment_ID == apartment_name)
    for bin in bins:  
        bin_records = BinRecord.query.filter(
            BinRecord.associated_bin == bin.id_bin
        ).order_by(BinRecord.timestamp.desc())[:50]

        if len(bin_records) >= 2:
            timestamps = []
            filling = []
            for bin_record in bin_records:
                timestamps.append(bin_record.timestamp)
                filling.append(bin_record.riempimento)

            with open(
                "./app/fbprophet/predictions/%s/riempimento_%s.csv"
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
                "./app/fbprophet/predictions/%s/riempimento_%s.csv"
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
                "./Predizioni/%s/%s/dati_attuali.png"
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
                "./app/fbprophet/predictions/%s/prediction_%s.csv"
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
                "./Predizioni/%s/%s/forecast.png" % (apartment_name, tipologia),
                format="png",
            )
            
            # Plotting the forecast components.
            m.plot_components(forecast)
            plt.savefig(
                "./Predizioni/%s/%s/components.png" % (apartment_name, tipologia),
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


