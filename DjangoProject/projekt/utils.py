import requests
import quandl
import pandas as pd
import numpy as np

from .models import Dane
from datetime import datetime, timedelta,date

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import cross_validate,train_test_split

def predicted_price(name):
    #get data from bitfinex echange for 'name' - specified coin
    df = quandl.get("BITFINEX/"+name+"USD", rows = "100")
    # For calculations we need only column  with hightest price
    df = df[['Last']]

    #get data from echchange as numpy table and insert them to database
    l_daty = 0 # iteral to get dates: 1 for yesterday etc.
    df2 = quandl.get("BITFINEX/"+name+"USD",returns = "numpy",rows = "5")
    Dane.objects.all().delete()
    for i in range(4,-1,-1):
        model = Dane(nazwa = name ,data =date.today() - timedelta(1)-timedelta(l_daty),cena = df2[i][4])
        l_daty +=1
        model.save()
    #end of adding data

    forecast_out = int(1) # predicting 1 day into future
    df['Prediction'] = df[['Last']].shift(-forecast_out) #  label column with data shifted 1 unit up

    X = np.array(df.drop(['Prediction'], 1))
    X = preprocessing.scale(X)
    X_forecast = X[-forecast_out:] # set X_forecast equal to last 1

    X = X[:-forecast_out] # remove last 1 from X
    y = np.array(df['Prediction'])
    y = y[:-forecast_out]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    # Training
    clf = LinearRegression()
    clf.fit(X_train,y_train)
    # Testing
    confidence = clf.score(X_test, y_test)
    forecast_prediction = clf.predict(X_forecast)

    return forecast_prediction[0]

def actual_price(name):
    resp_json = requests.get('https://api.bitfinex.com/v2/candles/trade:1m:t'+name+"USD/hist").json()
    return resp_json[0][2]
