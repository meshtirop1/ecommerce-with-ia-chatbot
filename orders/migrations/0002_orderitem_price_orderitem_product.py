# orders/migrations/0002_orderitem_price_orderitem_product.py

from django.db import migrations, models
from decimal import Decimal

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(default=Decimal('0.00'), max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='products.Product'),
        ),
    ]