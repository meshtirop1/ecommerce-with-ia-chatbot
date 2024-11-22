from django.contrib import admin
from .models import Product, Category  # Assuming you have Product and Category models

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_featured')
    search_fields = ('name', 'description')
    list_filter = ('category', 'is_featured')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
