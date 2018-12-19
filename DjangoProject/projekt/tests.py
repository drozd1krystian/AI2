from django.test import TestCase
from .models import Dane
from datetime import datetime, timedelta,date
import requests
import numpy as np
import quandl

class DaneTestCase(TestCase):

    def test_object(self,nazwa="BTC", data = date.today(),cena = "3214"):
        return Dane.objects.create(nazwa=nazwa, data = data,cena = cena)

    def test_created_object(self):
        sample_object = Dane.objects.create(nazwa="BTC", data = date.today(),cena = "3214")
        self.assertTrue(isinstance(sample_object, Dane))

    def test_inserting(self):
        sample_data = Dane.objects.create(nazwa="BTC", data = date.today(),cena = "3214")
        sample_data.save()

    def test_filter(self):
        filter_data = Dane.objects.filter(nazwa = "BTC")
        return len(filter_data) > 0

    def test_delete(self):
        sample_object = Dane.objects.create(nazwa="BTC", data = date.today(),cena = "3214")
        sample_object.save()
        Dane.objects.all().delete()

    def test_dataFromQuandl(self):
        df = quandl.get("BITFINEX/BTCUSD",returns = "numpy", rows = "1")
        return isinstance(df, np.ndarray)

    def test_actual_price(self):
        test_object = requests.get('https://api.bitfinex.com/v2/candles/trade:1m:tBTCUSD/hist').json()
        return len(test_object) > 0
