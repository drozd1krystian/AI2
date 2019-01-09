from django.urls import path
from . import views
from django.http import HttpResponseRedirect


urlpatterns = [
    path('', views.home_page),
    path('post_list', views.prediction_choice, name='prediction_choice'),
    path('prediction', views.prediction, name='prediction'),
    path('homepage',views.home_page,name='homepage')
]
