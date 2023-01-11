from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from app.database.tables import BinRecord, Bin
import pandas as pd
from prophet import Prophet
import matplotlib as plt
import csv
from app.database.database import calcolastatus, set_previsione_status
 

fbprophet_blueprint = Blueprint(
    'fbprophet', __name__, template_folder='templates', url_prefix='/fbprophet')


@fbprophet_blueprint.route('/')
def main():
    return '<h1>FbProphet</h1>'


@fbprophet_blueprint.route('/getprevision')
def getprevision():
    bins = Bin.query.all()
    timestamp = []
    filling = []
    for bin in bins:  # per ogni bidone creo una previsione temporale
        bin_records = BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin).order_by(BinRecord.timestamp.desc())[:30]
        apartment_name = Bin.query.filter(Bin.id_bin==bin.id_bin)[0].apartment_ID
        tipologia = Bin.query.filter(Bin.id_bin == bin.id_bin).first().tipologia

        for bin_record in bin_records:
            timestamp.append(bin_record.timestamp)
            filling.append(bin.riempimento)

        with open('fillinglevel.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["ds", "y"])
            for i in range(0, 30):
                filewriter.writerow([timestamp[i], filling[i]])

        df = pd.read_csv('fillinglevel.csv')
        df.plot()
        plt.show()
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])

        m = Prophet()
        m.fit(df)

        future = m.make_future_dataframe(m, periods=5, freq="day")
        future.tail()
        forecast = m.predict(future)

        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

        m.plot(forecast)

        datenow = datetime.datetime.now()
        dateend = datenow + timedelta(days=5)
        datestart = dateend - timedelta(days=20)
        plt.xlim([datestart, dateend])
        plt.title("Bin/Filling Level forecast", fontsize=20)
        plt.xlabel("Day", fontsize=20)
        plt.ylabel("Filling level", fontsize=20)
        plt.savefig("/Predizioni/%s/%s/Forecast.png" % (apartment_name, tipologia), format='png')

        prediction = forecast[['yhat']]
        status_previsto=calcolastatus(bin.id_bin, prediction[0], None, None, None)
        set_previsione_status(bin.id_bin, status_previsto)

        return 'done'
