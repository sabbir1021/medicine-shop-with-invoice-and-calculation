from django.urls import path
from . import views
from django.urls import reverse_lazy

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('ajax/search-and-filter/', views.load_search_and_filter, name="ajax_load_search_and_filter"),
    path('update_item/', views.UpdateItemView.as_view(), name="update_item"),
    path('confirm-order/', views.confirm_order, name="confirm_order"),
    path('report-generate/', views.report_generate, name="report_generate"),
    
]