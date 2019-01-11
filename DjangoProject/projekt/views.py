from django.shortcuts import render
from .models import Dane, Results
from .utils import *
from datetime import datetime, timedelta,date
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm
from django.shortcuts import redirect
import plotly.plotly as py
import plotly.graph_objs as go

def template(request):
    return render(request,'projekt/template.html')

def home_page(request):
    return render(request,'projekt/home_page.html')

def prediction_choice(request):
    form = NameForm()
    return render(request, 'projekt/prediction_choice.html',{'form':form})

def prediction_choice2(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if not form.is_valid():
            return redirect('projekt/')
        else:
            name = form.cleaned_data['coin_name']
            return name
def prediction(request):
    #Get today's date, create form to put in html, get coin name, date for results
    data = str(date.today());
    form = NameForm()
    name =  str(prediction_choice2(request))

    #add sample data to database
    database_adder(name,5)

    #predicted price
    predicted = predicted_price(name,data)

    #variables needed to post in html table
    posts = Dane.objects.filter(nazwa = name)
    last_price = actual_price(name)

    #return data
    return render(request, 'projekt/prediction.html', {'posts': posts,'predicted':predicted[1],'last_price':last_price,
    'name':name,'form':form})

def results(request):
    #run function to check if predictions are close to right
    compare_results(database_adder("BTC",5))
    number_of_hits_btc = float(0)
    number_of_hits_eth = float(0)
    #get results from database
    results_btc = Results.objects.filter(nazwa = "BTC")
    for result in results_btc:
        rc_1 = result.cena
        rc_2 = result.zamkniecie
        if (abs(float(rc_1) - float(rc_2))) <= 3:
            number_of_hits_btc += 1
    number_of_hits_btc = ((len(results_btc)-number_of_hits_btc)/len(results_btc))*100
    results_eth = Results.objects.filter(nazwa = "ETH")
    for result in results_eth:
        rc_1 = result.cena
        rc_2 = result.zamkniecie
        if (abs(float(rc_1) - float(rc_2))) <= 0.5:
            number_of_hits_eth += 1
    number_of_hits_eth = ((len(results_eth)-number_of_hits_eth)/len(results_eth))*100
    #results_xrp = Results.objects.filter(nazwa = "XRP")
    #results_trx = Results.objects.filter(nazwa = "TRX")
    #results_ltc = Results.objects.filter(nazwa = "LTC")

    return render(request,'projekt/results.html',{'results_btc':results_btc,'results_eth':results_eth,'number_of_hits_btc':number_of_hits_btc, 'number_of_hits_eth':number_of_hits_eth})
