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


def load_search_and_filter(request):
    brand_list = request.GET.getlist('brand_list[]')
    generic_list = request.GET.getlist('generic_list[]')
    search_value = request.GET.get('search_value')
    print(search_value, brand_list, generic_list)
    medicines = Medicine.objects.all()
    if brand_list and generic_list:
        medicines = Medicine.objects.filter(name__contains=search_value,brand__name__in = brand_list, generic__name__in = generic_list)
    if brand_list:
        medicines = Medicine.objects.filter(name__contains=search_value,brand__name__in = brand_list)
    if generic_list:
        medicines = Medicine.objects.filter(name__contains=search_value,generic__name__in = generic_list)
    if search_value:
        medicines = Medicine.objects.filter(name__contains=search_value)
    medicines_count = medicines.count()
    paginator = Paginator(medicines, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'search.html', {'medicines':page_obj,'medicines_count':medicines_count})
