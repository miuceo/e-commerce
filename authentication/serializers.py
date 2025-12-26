from rest_framework import serializers
from .models import CustomUser
import re

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "role",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
        )
        read_only_fields = ("id", "is_staff", "is_superuser", "date_joined")

    def validate_phone(self, value: str):
        if not value:
            raise serializers.ValidationError("Phone number cannot be empty!")
        if not value.startswith(("+998", "998")):
            raise serializers.ValidationError("Phone number must start with +998 or 998")
        
        if not value[1:].isdigit():
            raise serializers.ValidationError("Phone must be only number!")
        
        if not (len(value) >= 12 or len(value)<=13):
            raise serializers.ValidationError("Phone nuber mus contain 12 numbers")
        
        return value


    def validate_role(self, value):
        if self.instance is None and value == "admin":
            request_user = self.context.get('request').user if 'request' in self.context else None
            if not (request_user and request_user.is_superuser):
                raise serializers.ValidationError("Faqat superuser admin role bera oladi")
        if value not in ["user", "seller", "admin"]:
            raise serializers.ValidationError("Role noto‘g‘ri")
        return value

    def validate_is_staff(self, value):
        if self.instance and not self.context.get('request').user.is_superuser:
            raise serializers.ValidationError("Faqat superuser is_staff maydonini o‘zgartirishi mumkin")
        return value

    def validate_is_superuser(self, value):
        if self.instance and not self.context.get('request').user.is_superuser:
            raise serializers.ValidationError("Faqat superuser is_superuser maydonini o‘zgartirishi mumkin")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Parol kamida 1 raqam bo‘lishi kerak")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Parol kamida 1 katta harf bo‘lishi kerak")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Parol kamida 1 kichik harf bo‘lishi kerak")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Parol kamida 1 maxsus belgi bo‘lishi kerak")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
