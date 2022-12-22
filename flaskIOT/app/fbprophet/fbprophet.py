import pandas as pd
from pandas import to_datetime
import matplotlib.pyplot as plt
from fbprophet import Prophet
from datetime import datetime, timedelta
from app.database.tables import BinRecord, Bin
import csv
from flask import Flask,jsonify,json

bins=Bin.query.all()
timestamp=[]
filling=[]
for bin in bins: #per ogni bidone creo previsione temporale
    #prendo le ultime 30 istanze
    bin_records=(BinRecord.query.filter_by(BinRecord.id_bin==bin.id_bin).order_by(BinRecord.timestamp))[30]
    for bin_record in bin_records:
        timestamp.append(bin_record.timestamp)
        filling.append(bin.riempimento)
    with open('fillinglevel.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["ds", "y"])
        for i in range(0,30):
            filewriter.writerow([timestamp[i], filling[i]])

    df = pd.read_csv('fillinglevel.csv')
    df.plot()
    plt.show()
    df.columns = ['ds', 'y']
    df['ds']= to_datetime(df['ds'])
    #Predictions are then made on a dataframe with a column ds containing the dates for which a prediction is to be made.
    #You can get a suitable dataframe that extends into the future a specified number of days using the helper method Prophet.make_future_dataframe. 
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(m, periods=5, freq="day")
    future.tail()
    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail() #The forecast object here is a new dataframe that includes a column yhat with the forecast, as well as columns for components and uncertainty intervals.

    fig1 = m.plot(forecast)
    #datenow = datetime.now()
    datenow = datetime(2022, 12, 24)
    dateend = datenow + timedelta(days=5)
    datestart = dateend - timedelta(days=20)
    plt.xlim([datestart, dateend])
    plt.title("Bin/Filling Level forecast", fontsize=20)
    plt.xlabel("Day", fontsize=20)
    plt.ylabel("Filling level", fontsize=20)
    plt.axvline(datenow, color="k", linestyle=":")
    plt.show()

    fig2 = m.plot_components(forecast)

    prediction=forecast[['yhat']]
    #messaggio Json
    msgJson = {'id_bin': bin.id_bin,
        'riempimento': prediction[0]}
    jsonify(msgJson)
    #mando il json alla pagina trap/getstatus
    status=0#previsione ricevuta
    Bin.query().filter(Bin.id_bin==bin.id_bin).update({Bin.previsione_status: status}, synchronize_session = False)