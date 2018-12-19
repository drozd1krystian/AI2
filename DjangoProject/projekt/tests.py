from django.test import TestCase
from .models import Dane
from datetime import datetime, timedelta,date
import requests
import numpy as np
import quandl

def test_object(nazwa="BTC", data = date.today(),cena = "3214"):
    return Dane.objects.create(nazwa=nazwa, data = data,cena = cena)

class DaneTestCase(TestCase):

    def test_created_object(self):
        sample_object = test_object()
        self.assertTrue(isinstance(sample_object, Dane))

    def test_insert_and_filter(self):
        sample_data = test_object()
        sample_data.save()
        filter_data = Dane.objects.filter(nazwa = "BTC")
        self.assertIsNot(len(filter_data), 0)

    def test_delete(self):
        sample_object = test_object()
        sample_object.save()
        Dane.objects.all().delete()
        filter_data = Dane.objects.filter(nazwa = "BTC")
        self.assertIs(len(filter_data), 0)

    def test_dataFromQuandl(self):
        df = quandl.get("BITFINEX/BTCUSD",returns = "numpy", rows = "1")
        self.assertIs(type(df),np.recarray)

    def test_actual_price(self):
        test_object = requests.get('https://api.bitfinex.com/v2/candles/trade:1m:tBTCUSD/hist').json()
        self.assertIsNot(len(test_object), 0)
