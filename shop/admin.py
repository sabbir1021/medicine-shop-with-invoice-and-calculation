from django.contrib import admin
from .models import Medicine , Group, Company, Place
# Register your models here.

admin.site.register(Medicine)
admin.site.register(Group)
admin.site.register(Company)
admin.site.register(Place)