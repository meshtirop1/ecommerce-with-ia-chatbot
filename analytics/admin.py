from django.contrib import admin
from .models import ProductView, SalesSummary

@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'timestamp')
    search_fields = ('product__name', 'user__username')
    list_filter = ('timestamp',)

@admin.register(SalesSummary)
class SalesSummaryAdmin(admin.ModelAdmin):
    list_display = ('order', 'total_price', 'date')
    search_fields = ('order__user__username',)
    list_filter = ('date',)
