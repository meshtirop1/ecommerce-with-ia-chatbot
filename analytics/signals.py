from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product
from orders.models import Order
from .models import ProductView, SalesSummary

@receiver(post_save, sender=Order)
def create_sales_summary(sender, instance, created, **kwargs):
    if created:
        SalesSummary.objects.create(order=instance, total_price=instance.total_price)
