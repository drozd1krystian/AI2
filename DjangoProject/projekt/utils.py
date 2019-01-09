import requests
import quandl
import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import os
from .models import Dane
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

def predicted_price(name, data):
    #get data from bitfinex echange for 'name' - specified coin
    #start_date="2001-12-31", end_date="2005-12-31")
    df_main = quandl.get("BITFINEX/"+name+"USD", rows = "2000", start_date = "2014-01-01", end_date = data)
    # For calculations we need only column  with hightest price
    #df = df_main[['Last']]
    database_adder(name, df_main)

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
    close.extend(predicted_data)
    """
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
    #chart
    chart(name) # draws a chart with orginal data

    price = []
    price.extend(df_main['Last'].tolist())
    price.append(forecast_prediction[0])
    """
    chart_date = df_main.index.tolist()
    for i in range(0,31):
        chart_date.append(date.today()+timedelta(i))

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
    return predicted_data[0]

def database_adder(name, df):
    #get data from echchange as numpy table and insert them to database
    l_daty = 0 # iteral to get dates: 1 for yesterday etc.
    df2 = quandl.get("BITFINEX/"+name+"USD",returns = "numpy",rows = "5")
    x = df.index.to_pydatetime()    #change index to dateformat
    dl = len(x)-1
    Dane.objects.all().delete()
    for i in range(4,-1,-1):
        date_input = x[dl-l_daty]
        model = Dane(nazwa = name ,data =date_input.strftime('%B %d, %Y'),cena = round(df2[i][4],1))
        l_daty +=1
        model.save()
    #end of adding data

def actual_price(name):
    resp_json = requests.get('https://api.bitfinex.com/v2/candles/trade:1m:t'+name+"USD/hist").json()
    return resp_json[0][2]
