from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=70)
    description = models.TextField()
    price = models.IntegerField()
    is_new = models.BooleanField(default=False)
    is_discounted = models.BooleanField(default=False)
    category = models.ForeignKey('Category', default=False, on_delete=models.CASCADE)
    is_hot = models.BooleanField(default=False, verbose_name="Hot Mahsulotmi?")
    brand = models.ForeignKey('Brand', default=None, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default_product.png', null=True, upload_to='product_img'
    )
    sale_product_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # yangi maydon:
    in_stock = models.BooleanField(default=True, verbose_name='Есть в наличии')

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

class Brand(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='brands_icon')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Slide(models.Model):
    image = models.ImageField(upload_to='slide_images')


class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    def total_price(self):
        return self.product.price * self.quantity



class Region(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.region.name})"

class Branch(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.district.name}"



# Buyurtma modeli
class Order(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    total_price = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return 'Order # %s' % (str(self.id))


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    total = models.IntegerField()
    

    def __str__(self):
        return '%s x%s - %s' % (self.product, self.amount, self.order.customer.username)


RATE_CHOICES = [
    (1, '🗑️ - Trash'),
    (2, '👎 - Bad'),
    (3, '😐 - Ok'),
    (4, '👍 - Good'),
    (5, '🌟 - Perfect'),
]


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=300, blank=True)
    rate = models.PositiveBigIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return self.user.username



class SearchImage(models.Model):
    keyword = models.CharField(max_length=255, unique=True, verbose_name="Qidiruv Kalit So'zi")
    image = models.ImageField(upload_to='search_images/', verbose_name="Rasm")
    is_pinned = models.BooleanField(default=True, verbose_name="Natijalarga Pinned qilsinmi?")

    def __str__(self):
        return f"{self.keyword} (Pinned: {self.is_pinned})"



