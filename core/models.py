from django.db import models
from authentication.models import CustomUser
from django.utils.text import slugify
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='catgories')
    
    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=5, unique=True)
    
    def __str__(self):
        return self.name
        
class Brand(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    slug = models.SlugField(unique=True, primary_key=True)
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    seller_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    desc = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField()
    sizes = models.ManyToManyField(Size, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to="products")
    discount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def is_sale(self):
        return self.discount > 0
    
    @property
    def discounted_price(self):
        return self.price * Decimal(((100 - self.discount) / 100))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='products')
    
    def __str__(self):
        return f'{self.product.name} - {self.id}'
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    town = models.CharField(max_length=50)
    postcode = models.PositiveIntegerField()
    notes = models.CharField(max_length=150, blank=True, null=True)
    subtotal_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username    
    
    def total_price(self):
        return self.subtotal_price * Decimal('0.01') + self.subtotal_price * Decimal('0.05')

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="items")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_price(self):
        if self.product.is_sale:
            return self.quantity * self.product.discounted_price
        return self.quantity * self.product.price
