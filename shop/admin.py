from django.contrib import admin
from .models import Medicine , Generic, Brand, Place
# Register your models here.

admin.site.register(Medicine)
admin.site.register(Generic)
admin.site.register(Brand)
admin.site.register(Place)