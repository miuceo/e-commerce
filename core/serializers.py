from rest_framework import serializers
from .models import Category, Brand, Size, Product, ProductImages, CartItem, Order
from authentication.models import CustomUser
from authentication.serializers import CustomUserSerializer
from django.utils.text import slugify
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["slug", "name", "image"]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Category name cannot be empty")
        if len(value) > 30:
            raise serializers.ValidationError("Category name cannot exceed 30 characters")
        return value

    def create(self, validated_data):
        if not validated_data.get("slug"):
            base_slug = slugify(validated_data.get("name", ""))
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            validated_data["slug"] = slug
        return super().create(validated_data)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["slug", "name"]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Brand name cannot be empty")
        if len(value) > 50:
            raise serializers.ValidationError("Brand name cannot exceed 50 characters")
        return value

    def create(self, validated_data):
        if not validated_data.get("slug"):
            base_slug = slugify(validated_data.get("name", ""))
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            validated_data["slug"] = slug
        return super().create(validated_data)


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id", "name"]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Size name cannot be empty")
        if len(value) > 5:
            raise serializers.ValidationError("Size name cannot exceed 5 characters")
        if not value.isalnum():
            raise serializers.ValidationError("Size name must be alphanumeric")
        return value


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True, read_only=True)
    size_ids = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(),
        many=True,
        write_only=True,
        source="sizes"
    )
    images = ProductImagesSerializer(many=True, read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    is_sale = serializers.ReadOnlyField()
    discounted_price = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "slug", "name", "category", "seller_id", "brand", "desc", "quantity",
            "sizes", "size_ids", "price", "main_image", "discount",
            "is_sale", "discounted_price", "images", "created_at", "updated_at"
        ]
        read_only_fields = ["slug", "is_sale", "discounted_price", "created_at", "updated_at"]


    def validate(self, attrs):
        price = attrs.get("price")
        quantity = attrs.get("quantity")
        discount = attrs.get("discount")

        if price is not None and price < 0:
            raise serializers.ValidationError({"price": "Price must be positive"})
        if quantity is not None and quantity < 0:
            raise serializers.ValidationError({"quantity": "Quantity must be positive"})
        if discount is not None and not (0 <= discount <= 100):
            raise serializers.ValidationError({"discount": "Discount must be between 0 and 100"})
        return attrs

    def validate_slug(self, value):
        if not value:
            value = slugify(self.initial_data.get("name", ""))
        qs = Product.objects.filter(slug=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Slug must be unique")
        return value

    def create(self, validated_data):
        sizes = validated_data.pop("sizes", [])
        product = super().create(validated_data)
        product.sizes.set(sizes)
        return product

    def update(self, instance, validated_data):
        sizes = validated_data.pop("sizes", None)
        instance = super().update(instance, validated_data)
        if sizes is not None:
            instance.sizes.set(sizes)
        return instance


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source="user",
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id", "product", "product_id", "user", "user_id", "order",
            "quantity", "size", "total_price", "created_at", "updated_at"
        ]
        read_only_fields = ["total_price", "created_at", "updated_at"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def validate(self, attrs):
        product = attrs.get("product")
        size_name = attrs.get("size")
        quantity = attrs.get("quantity")

        if size_name and not product.sizes.filter(name=size_name).exists():
            raise serializers.ValidationError({"size": f"Size '{size_name}' is not available for this product"})

        if quantity > product.quantity:
            raise serializers.ValidationError({"quantity": f"Cannot order more than available stock ({product.quantity})"})

        return attrs


class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Order
        fields = [
            "id", "user", "country", "address", "town", "postcode", "notes",
            "subtotal_price", "total_price", "status", "payment_model", "items",
            "created_at", "updated_at"
        ]
        read_only_fields = ["total_price", "created_at", "updated_at"]

    def get_total_price(self, obj):
        return obj.total_price()

    def validate_subtotal_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Subtotal price must be positive")
        return value

    def validate_status(self, value):
        if value not in dict(Order.STATUS_CHOICES):
            raise serializers.ValidationError("Invalid order status")
        return value

    def validate_payment_model(self, value):
        if value not in dict(Order.PAYMENT):
            raise serializers.ValidationError("Invalid payment method")
        return value
    
class OrderCreateSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=100)
    town = serializers.CharField(max_length=50)
    postcode = serializers.IntegerField()
    notes = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True
    )
    payment_model = serializers.ChoiceField(
        choices=Order.PAYMENT
    )

    def validate_postcode(self, value):
        if value <= 0:
            raise serializers.ValidationError("Postcode noto‘g‘ri")
        return value

