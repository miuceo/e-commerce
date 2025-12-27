from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import Group, Permission

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, phone=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username majburiy")
        if not phone:
            raise ValueError("Phone majburiy")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True bo‘lishi kerak")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True bo‘lishi kerak")

        return self.create_user(username, email, phone, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("seller", "Seller"),
        ("admin", "Admin"),
    )

    REQUIRED_FIELDS = ["email", "phone"]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # unique name
        blank=True,
        help_text="User groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # unique name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return f'{self.username} - {self.role}'