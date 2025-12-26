from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import Product, Size

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role": self.user.role
        }
        data['success'] = True
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user'] = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "phone": user.phone,
            "email": user.email,
        }
        
        return token
    

class AddToCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        required=True,
        min_value=1,
        help_text="Quantity of the product to add to cart"
    )
    size = serializers.CharField(
        required=True,
        max_length=5,
        help_text="Size of the product"
    )

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def validate_size(self, value):
        if not value:
            raise serializers.ValidationError("Size cannot be empty")
        if len(value) > 5:
            raise serializers.ValidationError("Size cannot exceed 5 characters")
        return value

    def validate(self, attrs):
        product = self.context.get("product")
        if not product:
            raise serializers.ValidationError("Product context is required")

        quantity = attrs.get("quantity")
        size = attrs.get("size")

        if quantity > product.quantity:
            raise serializers.ValidationError(f"Cannot order more than available stock ({product.quantity})")

        if not product.sizes.filter(name=size).exists():
            raise serializers.ValidationError(f"This product doesn't have size '{size}'")

        return attrs
