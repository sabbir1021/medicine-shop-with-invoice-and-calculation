from ast import Or
from multiprocessing import context
from django.shortcuts import render, get_object_or_404 , HttpResponse
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
        medicines_count = medicines.count()
        paginator = Paginator(medicines, 10) # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        try:
            order = get_object_or_404(Order, user=request.user,complete_order=False)
            items = order.orderitem_set.all() or None
        except:
            order = None
            items = None
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
        productId = request.POST.get('product_id')
        action = request.POST.get('action')
        print(productId, action)
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

        order = get_object_or_404(Order, user=request.user,complete_order=False)
        items = order.orderitem_set.all()
        context = {
            'order':order,
            'items':items

        }
        return render(request, "partials/cart_result.html", context)
        # return JsonResponse('item' , safe=False)


def load_search_and_filter(request):
    brand_list = request.GET.getlist('brand_list[]')
    generic_list = request.GET.getlist('generic_list[]')
    search_value = request.GET.get('search_value')
    medicines = Medicine.objects.all()
    if brand_list and generic_list:
        medicines = Medicine.objects.filter(name__contains=search_value, brand__name__in = brand_list, generic__name__in = generic_list)
    elif brand_list:
        medicines = Medicine.objects.filter(name__contains=search_value, brand__name__in = brand_list)
    elif generic_list:
        medicines = Medicine.objects.filter(name__contains=search_value, generic__name__in = generic_list)
    elif search_value:
        medicines = Medicine.objects.filter(name__contains=search_value)
    medicines_count = medicines.count()
    paginator = Paginator(medicines, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'partials/search.html', {'medicines':page_obj,'medicines_count':medicines_count})


def confirm_order(request):
    orderId = request.POST.get('order_id')
    print(orderId)
    order = Order.objects.get(id=orderId)
    order.complete_order = True
    order.save()
    items = order.orderitem_set.all()
    for i in items:
        print(i.product.id, i.quantity)
        medicine = Medicine.objects.get(id=i.product.id)
        medicine.quantity = medicine.quantity - i.quantity
        medicine.save()

    return HttpResponse("ok")


import datetime
def report_generate(request):
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    if from_date and to_date:
        orders = Order.objects.filter(updated_at__range=[from_date,to_date], complete_order=True)
    else:
        orders = Order.objects.filter(updated_at=datetime.date.today(), complete_order=True)
    
    total_sell = 0
    total_profit = 0
    for i in orders:
        total_sell = total_sell + i.get_cart_total
        total_profit = total_profit + i.get_profit_total

    context = {
        'total_orders': orders.count(),
        'total_sell' : total_sell,
        'total_profit': total_profit,
        'from_date': from_date,
        'to_date' : to_date

    }
    return render(request, 'shop/report.html', context)