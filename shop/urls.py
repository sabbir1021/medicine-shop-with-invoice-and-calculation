from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    
]