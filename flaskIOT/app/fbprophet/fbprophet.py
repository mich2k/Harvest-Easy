from flask import Blueprint, jsonify
from itertools import zip_longest
from datetime import datetime, timedelta
from app.database.tables import BinRecord, Bin
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import csv
from app.utils.utils import Utils

fbprophet_blueprint = Blueprint(
    "fbprophet", __name__, template_folder="templates", url_prefix="/pred"
)


@fbprophet_blueprint.route("/")
def main():
    return "<h1>FbProphet</h1>"


@fbprophet_blueprint.route("/getprevision")
def getprevision():
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
    return {"fbprophet": array_pred}

@fbprophet_blueprint.route("/getprevision/<string:apartment_name>")
def getprevision2(apartment_name):
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
    
        json_bin={"bin": bin.id_bin, "previsioni": None}
        
        values_and_dates=[]
        for i in range(len(predictions)):
            array={}
            array["value"]= predictions[i]
            array["date"]= dates[i]
            values_and_dates.append(array)
        json_bin["previsioni"]=values_and_dates
        array_pred.append(json_bin)
    return {"apartment_name": apartment_name, "tipologia": tipologia, "previsioni_bidoni": array_pred}

@fbprophet_blueprint.route("/getprevision/<string:apartment_name>&<string:tipologia>")
def getprevision3(apartment_name, tipologia):
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
    return {"apartment_name": apartment_name, "tipologia": tipologia, "previsioni_bidoni": array_pred}


@fbprophet_blueprint.route("/createprevision/<int:time>")
def createprevision(time):
    if time == 0:
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
            
    return 'done'

@fbprophet_blueprint.route("/createprevision/<string:apartment_name>&<string:tipologia>&<int:time>")
def createprevision2(apartment_name, tipologia, time):
    if time is None:
        time = 5
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
            
    return 'done'


