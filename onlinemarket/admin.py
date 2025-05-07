from django.contrib import admin

from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', )
    list_filter = ( 'category')
    search_fields = ('title', 'description')

    # Xit mahsulotlar bo'limi uchun
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Bu joyni kerak bo‘lsa o‘zgartirasiz
        return qs

# Register your models here.
admin.site.unregister(Product)  
admin.site.register(Product)
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(ProductImage)
