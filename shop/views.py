from multiprocessing import context
from django.shortcuts import render, get_object_or_404
from django.views import View 
from .models import Medicine, Brand , Generic ,Order, OrderItem
from django.contrib import messages
import json
from django.http import JsonResponse
# Create your views here.

class HomeView(View):
    def get(self, request):
        brands = Brand.objects.all()
        generics = Generic.objects.all()
        medicines = Medicine.objects.all()
        order = get_object_or_404(Order, user=request.user,complete_order=False)
        items = order.orderitem_set.all()
        context = {
            'brands':brands,
            'generics':generics,
            'medicines':medicines,
            'order':order,
            'items':items

        }
        return render(request, "shop/home.html", context)

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