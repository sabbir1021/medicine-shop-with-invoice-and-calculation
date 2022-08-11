from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from django.views import View 
from .models import Medicine, Brand , Generic ,Order, OrderItem
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

# Create your views here.

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        brands = Brand.objects.all()
        generics = Generic.objects.all()
        medicines = Medicine.objects.all()
        if request.GET.get('search'):
            search = request.GET.get('search')
            print(search)
            medicines = Medicine.objects.filter(name__contains=search)
        medicines_count = medicines.count()
        paginator = Paginator(medicines, 10) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        order = get_object_or_404(Order, user=request.user,complete_order=False)
        items = order.orderitem_set.all()
        context = {
            'brands':brands,
            'generics':generics,
            'medicines':page_obj,
            'medicines_count':medicines_count,
            'order':order,
            'items':items

        }
        return render(request, "shop/home.html", context)
   

@method_decorator(login_required, name='dispatch')
class UpdateItemView(View):
    def post(self, request):
        print("-----------------------------")
        
        data = json.loads(request.body)
        print(data['productId'], data['action'])
        productId = data['productId']
        action = data['action']
        user = request.user
        product = Medicine.objects.get(id=productId)
        
        order, created = Order.objects.get_or_create(user=user,complete_order=False)
        orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        if action == 'add':
            if product.quantity - orderitem.quantity > 0:
                orderitem.quantity = (orderitem.quantity +1)
            else:
                orderitem.quantity = (orderitem.quantity)
                messages.success(self.request, f'{orderitem.product}. Item Have Left {orderitem.quantity}.')
        elif action == 'sub':
            orderitem.quantity = (orderitem.quantity -1)
        orderitem.save()
        if action == 'del':
            orderitem.delete()
            messages.success(self.request, f'{orderitem.product}. Item deleted From Cart.')
        
        if orderitem.quantity <=0:
            orderitem.delete()
        return JsonResponse('item' , safe=False)

def load_search(request):
    country_id = request.GET.get('country_id')
    print(country_id)
    medicines = Medicine.objects.filter(name__contains=country_id)
    medicines_count = medicines.count()
    paginator = Paginator(medicines, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'search.html', {'medicines':page_obj,'medicines_count':medicines_count})

def load_filter(request):
    country_id = request.GET

    print('----------------------',country_id)

    medicines = Medicine.objects.all()
    medicines_count = medicines.count()
    paginator = Paginator(medicines, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'search.html', {'medicines':page_obj,'medicines_count':medicines_count})
