from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Category, Brand, Slide, CartItem, Order, OrderProduct, Review, SearchImage, District, Branch, Region
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, RateForm
from django.db import models
from .serializers import (ProductSerializer, CategorySerializer, BrandSerializer, 
                          SlideSerializer, CartItemSerializer, OrderSerializer, 
                          OrderProductSerializer, ReviewSerializer, SearchImageSerializer)

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

# ✅ Brendlar API
@api_view(['GET'])
def brand_list_api(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True)
    return Response(serializer.data)

# ✅ Slayder API
@api_view(['GET'])
def slide_list_api(request):
    slides = Slide.objects.all()
    serializer = SlideSerializer(slides, many=True)
    return Response(serializer.data)

# ✅ Qidiruv rasmi API
@api_view(['GET'])
def search_image_list_api(request):
    images = SearchImage.objects.all()
    serializer = SearchImageSerializer(images, many=True)
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
    
    order = Order.objects.create(
        address=request.data.get('address'),
        phone=request.data.get('phone'),
        total_price=total_price,
        customer=request.user
    )

    for cart_item in cart_items:
        OrderProduct.objects.create(
            order=order,
            product=cart_item.product,
            amount=cart_item.quantity,
            total=cart_item.total_price(),
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

# ✅ Izoh qoldirish API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_product_api(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ReviewSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(user=request.user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Diagramma uchun statistika API

   
# ================== FRONTEND VIEWS ==================


@login_required(login_url='users/sign_in')
def products_list(request):
    products = Product.objects.all().order_by('-is_hot', '-id')
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()
    brands = Brand.objects.all()
    slides = Slide.objects.all()

    category = request.GET.get('category')
    brand = request.GET.get('brand')
    search_query = request.GET.get('search', '')

    # Kategoriya bo‘yicha filtratsiya
    if category:
        products = products.filter(category=category)

    # Brend bo‘yicha filtratsiya
    if brand:
        products = products.filter(brand=brand)

    # Qidiruv natijalarini chiqarish
    if search_query:
        products = products.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    # Admin paneldan mos keladigan rasmni topamiz va mahsulotlar qatoriga qo‘shamiz
    pinned_image = SearchImage.objects.filter(keyword__iexact=search_query, is_pinned=True).first()

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
        "brands": brands,
        "slides": slides,
        "pinned_image": pinned_image,  # Pinned qilingan rasm
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


@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    form = OrderForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.customer = request.user
        order.total_price = total_price
        order.save()
        
        for cart_item in cart_items:
            OrderProduct.objects.create(order=order, product=cart_item.product, amount=cart_item.quantity, total=cart_item.total_price())
        
        cart_items.delete()
        return redirect('cart')

    return render(request, 'order_creation_page.html', {'form': form, 'cart_items': cart_items, 'total_price': total_price})

def rate_product(request, pk):
    product = Product.objects.get(pk=pk)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('rate_product', pk=pk)
    form = RateForm()
    return render(request, 'rate.html', {'form': form, 'product': product, 'reviews': reviews})



def orders(request):
    if request.user.is_authenticated:
        order_list = Order.objects.filter(customer=request.user)
        return render(request, 'orders.html', {'orders':order_list})
    else:
        return redirect('sign_up')
    
def load_districts(request):
    region_id = request.GET.get('region_id')
    districts = District.objects.filter(region_id=region_id).order_by('name')
    return render(request, 'dropdown_list_options.html', {'items': districts})

def load_branches(request):
    district_id = request.GET.get('district_id')
    branches = Branch.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'dropdown_list_options.html', {'items': branches})    



