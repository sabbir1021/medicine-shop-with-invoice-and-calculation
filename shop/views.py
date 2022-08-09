from multiprocessing import context
from django.shortcuts import render
from django.views import View 
from .models import Medicine, Brand , Generic
# Create your views here.

class HomeView(View):
    def get(self, request):
        brands = Brand.objects.all()
        generics = Generic.objects.all()
        medicines = Medicine.objects.all()
        context = {
            'brands':brands,
            'generics':generics,
            'medicines':medicines,

        }
        return render(request, "shop/home.html", context)