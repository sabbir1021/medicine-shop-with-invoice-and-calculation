from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('ajax/search', views.load_search, name="ajax_load_search"),
    path('ajax/brand/filter', views.load_brand_filter, name="ajax_load_brand_filter"),
    path('update_item/', views.UpdateItemView.as_view(), name="update_item"),
    
]