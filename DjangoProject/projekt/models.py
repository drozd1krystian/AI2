from django.db import models
from django.utils import timezone

class Dane(models.Model):
    id = models.AutoField(primary_key = True)
    nazwa = models.CharField(max_length = 15)
    data = models.CharField(max_length = 40)
    cena = models.FloatField()


class Results(models.Model):
    nazwa = models.CharField(max_length = 15)
    data = models.CharField(max_length = 40)
    cena = models.FloatField()
    zamkniecie = models.FloatField(default = 0)
