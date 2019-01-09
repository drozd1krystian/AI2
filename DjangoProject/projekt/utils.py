import requests
import quandl
import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os
from .models import Dane, Results
from datetime import datetime, timedelta,date
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, svm
from sklearn.model_selection import cross_validate,train_test_split
from django.http import HttpResponseRedirect,HttpResponse
from django.http.response import HttpResponse

def prediction_all(name,df_column,df_main):
    df = df_main[[df_column]]
    forecast_out = int(1) # predicting 1 day into future
    df['Prediction'] = df[[df_column]].shift(-forecast_out) #  label column with data shifted 1 unit up

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
    return forecast_prediction

def predicted_price(name, data, checker = True):
    #get data from bitfinex echange for 'name' - specified coin
    df_main = quandl.get("BITFINEX/"+name+"USD", start_date = "2014-01-01", end_date = data)
    predicted_price = []

    predicted_data = prediction_all(name,'Mid',df_main)
    open = []
    open = df_main['Mid'].tolist()
    open.extend(predicted_data)

    predicted_data = prediction_all(name,'High',df_main)
    hight = []
    high = df_main['High'].tolist()
    high.extend(predicted_data)

    predicted_data = prediction_all(name,'Low',df_main)
    low = []
    low = df_main['Low'].tolist()
    low.extend(predicted_data)

    predicted_data = prediction_all(name,'Last',df_main)
    close = []
    close = df_main['Last'].tolist()
    predicted_price.append(close[-1])
    close.extend(predicted_data)

    chart_date = df_main.index.tolist()
    for i in range(0,1):
        chart_date.append(date.today()+timedelta(i))

    if checker:
        trace = go.Candlestick(x=chart_date,
                open = open,
                high=high,
                low=low,
                close =close)

        layout = go.Layout(
        title=name+'/USD predicted chart',
        yaxis=dict(
            title='Price $',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
                )
            )
        )
        data = [trace]
        data = go.Figure(data=data, layout=layout)
        py.plot(data,layout,filename = 'predictedchart', auto_open=False)
    if name == "BTC" or name == "ETH":
        predicted_price.append(round(predicted_data[0],2))
    else:
        predicted_price.append(round(predicted_data[0],4))
    return predicted_price

def database_adder(name, rows):
    #get data from echchange as numpy table and insert them to database
    df2 = quandl.get("BITFINEX/"+name+"USD",returns = "numpy",rows = rows)
    Dane.objects.all().delete()
    for i in range(4,-1,-1):
        date_as_string = str(df2[i][0])
        if name == "BTC" or name == "ETH":
            cena = round(df2[i][4],2)
        else:
            cena = round(df2[i][4],4)
        model = Dane(nazwa = name, data = date_as_string[0:10], cena = cena)
        model.save()
    #end of adding data
    return df2

def actual_price(name):
    resp_json = requests.get('https://api.bitfinex.com/v2/candles/trade:1m:t'+name+"USD/hist").json()
    if name == "BTC" or name == "ETH":
        price = round(resp_json[0][2],2)
    else:
        price = round(resp_json[0][2],4)
    return price

def add_results(name, data, price, close):
    if name =="BTC" or name == "ETH":
        price = round(price,2)
        close = round(close,2)
    else:
        price = round(price,4)
    model = Results(nazwa = name, data = data[0:10], cena = price, zamkniecie = close)
    model.save()

def compare_results(date_results):
    Results.objects.all().delete()
    list = ["BTC","ETH"]
    checker = False # so it won't draw chart again for those coins
    #Podaj date np. 7 stycznia to podajemy 7-1 czyli 6 stycznia i liczy nam dla 7
    for name in list:
        for i in range(3,1,-1):
            date_as_string = str(date_results[i][0])
            price = predicted_price(name, str(date_results[i-1][0]), checker)
            add_results(name, date_as_string[0:10], price[1],price[0])
