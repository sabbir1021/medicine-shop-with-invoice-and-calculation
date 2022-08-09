from django.contrib import admin
from .models import Medicine , Generic, Brand, Place, Order ,OrderItem
# Register your models here.

admin.site.register(Medicine)
admin.site.register(Generic)
admin.site.register(Brand)
admin.site.register(Place)
admin.site.register(Order)
admin.site.register(OrderItem)