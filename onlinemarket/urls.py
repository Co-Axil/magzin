from django.urls import path
from .views import ( order_list_api, product_list_api, product_detail_api, category_list_api, 
                    cart_api, delete_cart_item_api, create_order_api,
                    orders, create_order,table_list_api,  
                    
                    products_list,
                    cart,
                    delete_cart_item,
                    edit_cart_item,
                    product_detail,
                    create_order,
                    
                    orders, create_order )
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/products/', product_list_api, name='product_list_api'),
    path('api/products/<int:pk>/', product_detail_api, name='product_detail_api'),
    path('api/categories/', category_list_api, name='category_list_api'),
    path('api/cart/', cart_api, name='cart_api'),\
    path('api/tables/', table_list_api, name='table-list_api'),
    path('api/cart/<int:pk>/', delete_cart_item_api, name='delete_cart_item_api'),
    path('api/orders/', create_order_api, name='create_order_api'),
    path('api/orderlist/', order_list_api, name='order_list_api'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', products_list, name='product_list'),
    path('cart/', cart, name='cart'),
    path('item/<int:pk>/delete/', delete_cart_item, name='delete_item'),
    path('edit_cart_item<int:pk>/', edit_cart_item, name='edit_cart_item'),
    path('product/<int:pk>/detail/', product_detail, name='product_detail'),
    path('cart/create_order/item/', create_order, name='create_order'),
    path('orders/', orders, name='orders'),
    path('', products_list, name='products_list'),
    path('create_order/', create_order, name='create_order'),
]