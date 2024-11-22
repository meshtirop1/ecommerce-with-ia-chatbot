# orders/migrations/0003_alter_orderitem_product.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem_price_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='products.Product'),
        ),
    ]