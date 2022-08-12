from django.db import models
from base.models import MEDICINE_TYPE
from django.contrib.auth import get_user_model
User = get_user_model()

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

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complete_order = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
            verbose_name = 'Orders'
            verbose_name_plural = '1. Orders'

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        return sum(i.get_total for i in items)

    @property
    def get_profit_total(self):
        items = self.orderitem_set.all()
        return sum(i.get_total_profit for i in items)


class OrderItem(models.Model):
    product = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
            verbose_name = 'OrderItems'
            verbose_name_plural = '2. OrderItems'

    def __str__(self):
        return str(self.order)
    
    @property
    def get_total(self):
        return self.product.sell_price  * self.quantity
    
    @property
    def get_total_profit(self):
        return (self.product.sell_price - self.product.buy_price)  * self.quantity