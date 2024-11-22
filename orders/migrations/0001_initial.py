# Generated by Django 5.1.3 on 2024-11-14 13:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checkout', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.cartitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', through='orders.OrderItem', to='checkout.cartitem'),
        ),
        migrations.CreateModel(
            name='ShippingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=20)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]
