from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.

from .models import *

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 3

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'image')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)} 

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Size)
class SizeAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'category', 'brand', 'seller_id', 'price', 'discount', 'is_sale', 'quantity', 'created_at', 'updated_at')
    list_filter = ('category', 'brand', 'sizes', 'created_at')
    search_fields = ('name', 'slug', 'category__name', 'brand__name', 'seller_id__username')
    prepopulated_fields = {"slug": ("name","brand","category")}
    inlines = [ProductImagesInline]
    filter_horizontal = ('sizes',)

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'user', 'status', 'subtotal_price', 'total_price', 'created_at', "payment_model")
    list_filter = ('status', 'country', 'created_at')
    search_fields = ('user__username', 'country', 'town', 'postcode')
    
@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ('id', 'user', 'product', 'order', 'quantity', 'total_price_display')
    search_fields = ('user__username', 'product__name', 'order__id')
    list_filter = ('order', 'product')

    @admin.display(description="Total Price")
    def total_price_display(self, obj):
        return obj.total_price

    total_price_display.short_description = 'Total Price'
