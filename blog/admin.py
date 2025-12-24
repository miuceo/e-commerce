from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *

# Register your models here.

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('tag',)
    search_fields = ('tag',)
    ordering = ('tag',)
    
@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ('title', 'author', 'slug', "created_at", "updated_at")
    search_fields = ('title', 'author', 'text')
    list_filter = ('tags', 'author')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    ordering = ('title',)
    
