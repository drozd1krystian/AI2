from django.shortcuts import render
from .models import Dane
from .utils import *
from datetime import datetime, timedelta,date
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm


def post_list(request):
    return render(request, 'projekt/post_list.html')

def post_list2(request):
    if request.method == 'POST':
        form = request.POST.get('coins')
    return str(form)

def prediction(request):
    #Predict price
    predicted = predicted_price(post_list2(request))
    name =  str(post_list2(request))
    #variables needed to post in html table
    posts = Dane.objects.filter(nazwa = str(post_list2(request)))
    last_price = actual_price(str(post_list2(request)))

    return render(request, 'projekt/prediction.html', {'posts': posts,'predicted':predicted,'last_price':last_price,
    'name':name})
