from django.db import models

# Create your models here.

class Group(models.Model):
    name  = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Company(models.Model):
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    company  = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name