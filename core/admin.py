from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Category,
    Brand,
    Color,
    Size,
    Product,
    ProductImage,
    CartItem,
    Order,
)

# Register your models here.

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Color)
class ColorAdmin(ModelAdmin):
    list_display = ("name", "html_code")
    search_fields = ("name",)

@admin.register(Size)
class SizeAdmin(ModelAdmin):
    list_display = ("name",)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "category",
        "brand",
        "seller",
        "price",
        "discount",
        "is_active",
        "created_at",
    )
    list_filter = ("category", "brand", "is_active", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category", "brand", "seller")
    filter_horizontal = ("colors", "sizes")
    inlines = (ProductImageInline,)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "category", "brand", "seller")
        }),
        ("Description", {
            "fields": ("description", "additional_description")
        }),
        ("Pricing", {
            "fields": ("price", "discount")
        }),
        ("Options", {
            "fields": ("colors", "sizes", "is_active")
        }),
        ("Dates", {
            "fields": ("created_at",)
        }),
    )

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "order",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("user__username", "product__name")
    readonly_fields = (
        "user",
        "product",
        "color",
        "size",
        "quantity",
        "order",
        "created_at",
        "updated_at",
    )

class OrderItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = (
        "product",
        "color",
        "size",
        "quantity",
    )

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "payment_method",
        "subtotal",
        "total_price",
        "created_at",
    )
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("id", "user__username", "email")
    readonly_fields = (
        "user",
        "subtotal",
        "total_price",
        "created_at",
        "updated_at",
    )
    inlines = (OrderItemInline,)

    fieldsets = (
        ("User", {
            "fields": ("user",)
        }),
        ("Billing Info", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "phone",
                "country",
                "state",
                "city",
                "address",
                "apartment",
                "postcode",
            )
        }),
        ("Order Info", {
            "fields": (
                "status",
                "payment_method",
                "note",
            )
        }),
        ("Prices", {
            "fields": (
                "subtotal",
                "total_price",
            )
        }),
        ("Dates", {
            "fields": ("created_at", "updated_at")
        }),
    )

