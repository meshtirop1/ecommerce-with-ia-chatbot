from django.urls import path
from . import views

urlpatterns = [
    path('', views.popular_products, name='popular_products'),
    path('total-sales/', views.total_sales, name='total_sales'),
]
