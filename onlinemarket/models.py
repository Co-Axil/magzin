from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey('Category', default=False, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default_product.png', null=True, upload_to='product_img'
    )

    def __str__(self):
        return self.name

    def __str__(self):
        return self.title
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

    def clean(self):
        if self.product.images.count() >= 10:
            raise ValidationError("You can only upload up to 10 images for a product.")

    def __str__(self):
        return f"Image for {self.product.title}"




class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name





class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    def total_price(self):
        return self.product.price * self.quantity




class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    is_available = models.BooleanField(default=True)  # Yangi maydon qo'shildi
    
    def __str__(self):
        return f"Stol {self.number}"


# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()



class Order(models.Model):
    total_price = models.IntegerField()
    table = models.ForeignKey('Table', on_delete=models.PROTECT, verbose_name="Stol raqami")
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mijoz")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)  #
    
    
    
def __str__(self):
        return f"Buyurtma #{self.id} | Stol: {self.table.number}"
# Buyurtma modeli



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f'{self.product} x{self.amount} - {self.order.customer.username}'
