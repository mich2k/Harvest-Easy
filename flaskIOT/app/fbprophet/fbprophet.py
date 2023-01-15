from flask import Blueprint, jsonify
from itertools import zip_longest
from datetime import datetime, timedelta
from app.database.tables import BinRecord, Bin
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import csv
from app.utils.utils import Utils
from prophet.plot import plot_plotly, plot_components_plotly

fbprophet_blueprint = Blueprint(
    'fbprophet', __name__, template_folder='templates', url_prefix='/pred')


@fbprophet_blueprint.route('/')
def main():
    return '<h1>FbProphet</h1>'


@fbprophet_blueprint.route('/getprevision')
def getprevision():
    
    timestamps = []
    filling = []
    
    for bin in Bin.query.all():  # per ogni bidone creo una previsione temporale
        
        bin_records = BinRecord.query.filter(
            BinRecord.associated_bin == bin.id_bin).order_by(BinRecord.timestamp.desc())[:30]
        
        apartment_name = Bin.query.filter(
            Bin.id_bin == bin.id_bin)[0].apartment_ID
        
        tipologia = Bin.query.filter(
            Bin.id_bin == bin.id_bin).first().tipologia
                
        for bin_record in bin_records:
            timestamps.append(bin_record.timestamp)
            filling.append(bin_record.riempimento)
        
        with open('fillinglevel.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["ds", "y"])
            for tp, fl in zip_longest(timestamps, filling):
                filewriter.writerow([tp, fl])

        df = pd.read_csv('fillinglevel.csv')
        
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])

        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=5, freq='d')
        future.tail()
        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
        """
        #m.plot(forecast)
        #m.plot_components(forecast)
        fig = plot_plotly(m, forecast)
        plot_components_plotly(m, forecast)
        datenow = datetime.now()
        dateend = datenow + timedelta(days=5)
        datestart = dateend - timedelta(days=20)
        
        plt.xlim([datestart, dateend])
        plt.title("Bin/Filling Level forecast", fontsize=20)
        plt.xlabel("Day", fontsize=20)
        plt.ylabel("Filling level", fontsize=20)
        
        plt.savefig("./predictions/%s/%s/forecast.png" %
                    (apartment_name, tipologia), format='png')
        """
        forecast.to_csv('prediction_%s_%s.csv' % (apartment_name, tipologia))
        prediction = forecast[['yhat']].values
        status_previsto = Utils.calcolastatus(
            bin.id_bin, prediction[0], None, None, None)
        
        Utils.set_previsione_status(bin.id_bin, status_previsto)

    return 'done'
