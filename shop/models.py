from django.db import models
from base.models import MEDICINE_TYPE
# Create your models here.
class Generic(models.Model):
    name  = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Brand(models.Model):
    name  = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Place(models.Model):
    name  = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Medicine(models.Model):
    name  = models.CharField(max_length=150)
    buy_price = models.FloatField()
    sell_price = models.FloatField()
    generic = models.ForeignKey(Generic, on_delete=models.CASCADE)
    brand  = models.ForeignKey(Brand, on_delete=models.CASCADE)
    type =  models.CharField(max_length=15,choices=MEDICINE_TYPE)
    quantity = models.IntegerField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name