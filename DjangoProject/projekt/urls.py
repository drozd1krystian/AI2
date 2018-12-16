from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('projekt/prediction', views.prediction, name='prediction')
]
