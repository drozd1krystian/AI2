from django.db import models
from django.utils import timezone

class Dane(models.Model):
    id = models.AutoField(primary_key = True)
    nazwa = models.CharField(max_length = 15)
    data = models.CharField(max_length = 40)
    cena = models.FloatField()

    def __str__(self):
        return self.cena
