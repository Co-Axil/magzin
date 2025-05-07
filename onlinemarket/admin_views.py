# onlinemarket/admin_views.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404
from .models import Order

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

    
    def customer_name(self, obj):
        return obj.customer.username
    customer_name.short_description = 'Customer Name'