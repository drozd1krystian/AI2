from django.test import TestCase
from .models import Dane
from datetime import datetime, timedelta,date
import response

class DaneTestCase(TestCase):
    def test_inserting(self):
        Dane.objects.create(nazwa="BTC", data = date.today(),cena = "3214")
        Dane.objects.create(nazwa="BTC", data = date.today()-timedelta(1),cena = "9999")
