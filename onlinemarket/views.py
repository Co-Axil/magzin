from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Category, CartItem, Order, Table, OrderProduct
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from django.db import models
from .serializers import (ProductSerializer, CategorySerializer, 
                           CartItemSerializer, OrderSerializer ,TableSerializer
                          )



# ✅ Mahsulotlar ro‘yxati API
@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all().order_by('-id')
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# ✅ Mahsulot detali API
@api_view(['GET'])
def product_detail_api(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

# ✅ Kategoriyalar ro‘yxati API
@api_view(['GET'])
def category_list_api(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)



# ✅ Savat API (Qo‘shish yoki ko‘rish)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_api(request):
    if request.method == 'GET':
        cart_items = CartItem.objects.filter(customer=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            customer=request.user, 
            product=product,
            defaults={"quantity": 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return Response({"message": "Mahsulot savatga qo‘shildi!"}, status=status.HTTP_201_CREATED)

# ✅ Savatdan mahsulot o‘chirish
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_item_api(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return Response({"message": "Mahsulot savatdan o‘chirildi!"}, status=status.HTTP_204_NO_CONTENT)

# ✅ Buyurtma yaratish API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_api(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    
    Order = Order.objects.create(
        address=request.data.get('address'),
        phone=request.data.get('phone'),
        total_price=total_price,
        customer=request.user
    )

  
    cart_items.delete()
    return Response({"message": "Buyurtma yaratildi!"}, status=status.HTTP_201_CREATED)

# ✅ Buyurtmalar ro‘yxati API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list_api(request):
    orders = Order.objects.filter(customer=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# ✅ Buyurtma mahsulotlari API
@api_view(['GET'])
def order_product_api(request):
    products = Product.objects.filter(in_stock=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def table_list_api(request):
    if request.user.is_authenticated:
        tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Unauthorized'}, status=401)

# ✅ Diagramma uchun statistika API

   
# ================== FRONTEND VIEWS ==================


@login_required(login_url='users/sign_in')
def products_list(request):
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

  
    
    product_id = request.GET.get('product')
    if product_id:
        try:
            product = Product.objects.get(pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                customer=request.user, 
                product=product,
                defaults={"quantity": 1}
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return redirect('product_list')
        except Product.DoesNotExist:
            pass  # Mahsulot topilmasa, hech narsa qilmaymiz

    context = {
        "products": products,
        "categories": categories,
        
    }
    return render(request, 'product_list.html', context)


@login_required(login_url='users/sign_in')
def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])
    return render(request, 'cart.html',
                  {'cart_items': cart_items,
                   'total_quantity': total_quantity,
                   'total_price': total_price})


def delete_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk).delete()
    return redirect('cart')


def edit_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    action = request.GET.get('action')

    if action == 'take' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('cart')
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    images = product.images.all()
    return render(request, 'product_detail.html', {"product": product})
def create_order(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    amount = sum([item.quantity for item in cart_items])
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Order yaratish
            order = form.save(commit=False)
            order.customer = request.user
            order.total_price = total_price
            order.amount = amount  # 👈 amount ni qo'shing
            order.save()
            
            # OrderProduct yaratish
            for cart_item in cart_items:
                OrderProduct.objects.create(
                    order=order,
                    product=cart_item.product,
                    amount=cart_item.quantity,
                    total=cart_item.total_price(),
                )
            
            # Tanlangan stolni band qilish
            order.table.is_available = False
            order.table.save()
            
            cart_items.delete()
            return redirect('cart')
    else:
        form = OrderForm()
    
    return render(request, 'order_creation_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'amount': amount,
        'form': form
    })



def orders(request):
    if request.user.is_authenticated:
        order_list = Order.objects.filter(customer=request.user)
        return render(request, 'orders.html', {'orders':order_list})
    else:
        return redirect('sign_up')
def Tables(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            selected_table = form.cleaned_data['tables']
            # Tanlangan stolni sessiyaga saqlash
            request.session['selected_table'] = selected_table.id
            return redirect('create_order')
    else:
        form = TableForm()
    
    return render(request, 'dropdown_list_options.html', {'form': form})


