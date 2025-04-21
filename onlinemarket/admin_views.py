# onlinemarket/admin_views.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from .models import Order, OrderProduct

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'address', 'phone', 'total_price', 'customer')
    change_list_template = "order_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:order_id>/details/', self.admin_site.admin_view(self.order_details), name='order-details'),
        ]
        return custom_urls + urls

    def order_details(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_products = OrderProduct.objects.filter(order=order)
        context = dict(
            self.admin_site.each_context(request),
            order=order,
            order_products=order_products,
        )
        return render(request, 'admin/order_details.html', context)

    def customer_name(self, obj):
        return obj.customer.username
    customer_name.short_description = 'Customer Name'