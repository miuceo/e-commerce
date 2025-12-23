from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "role",
        "is_staff",
        "is_active",
        "is_superuser",
    )

    list_display_links = (
        "id",
        "username",
        "email",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
        "is_superuser",
        "groups",
    )

    search_fields = (
        "username",
        "email",
        "phone",
    )

    ordering = ("id",)

    fieldsets = (
        ("Auth Info", {
            "fields": ("username", "password"),
        }),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "email", "phone"),
        }),
        ("Permissions", {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined"),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "phone",
                "role",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )

    show_full_result_count = True
    save_on_top = True
