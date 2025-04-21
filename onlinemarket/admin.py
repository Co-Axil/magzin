from django.contrib import admin

from .models import *

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name', 'region__name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_hot', 'is_new', 'in_stock')
    list_filter = ('is_hot', 'is_new', 'in_stock', 'brand', 'category')
    search_fields = ('title', 'description')

    # Xit mahsulotlar bo'limi uchun
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Bu joyni kerak bo‘lsa o‘zgartirasiz
        return qs

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'address')
    list_filter = ('district__region', 'district')
    search_fields = ('name', 'district__name', 'address')
# Register your models here.
admin.site.unregister(Product)  
admin.site.register(Product, SlugAdmin)
admin.site.register(Category)
admin.site.register(SearchImage)
admin.site.register(Brand)
admin.site.register(Slide)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ProductImage)
admin.site.register(Review)