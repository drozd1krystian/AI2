from django.shortcuts import render
from .models import Dane
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
    #Predict price
    #Get coin name
    data = str(date.today());
    form = NameForm()
    name =  str(prediction_choice2(request))
    predicted = round(predicted_price(name,data),1)
    #variables needed to post in html table
    posts = Dane.objects.filter(nazwa = name)
    last_price = round(actual_price(name),1)
    return render(request, 'projekt/prediction.html', {'posts': posts,'predicted':predicted,'last_price':last_price,
    'name':name,'form':form})
