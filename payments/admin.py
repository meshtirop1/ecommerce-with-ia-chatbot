from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at')
    search_fields = ('user__username', 'transaction_id')
    list_filter = ('payment_method', 'status', 'created_at')
