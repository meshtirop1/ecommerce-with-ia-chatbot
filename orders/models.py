from decimal import Decimal

from django.db import models
from django.conf import settings
from products.models import Product
from checkout.models import CartItem  # Import CartItem from checkout

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    items = models.ManyToManyField(CartItem, through='OrderItem', related_name='orders')  # Set a unique related_name


    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def calculate_total_price(self):
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)  # Set a unique related_name
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,blank=True)  # Ensure this field exists
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'))  # Ensure this field exists


    def __str__(self):
        return f"{self.quantity} of {self.cart_item.product.name}"

class ShippingStatus(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered')
    ], default='Pending')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipping status for Order {self.order.id}"
