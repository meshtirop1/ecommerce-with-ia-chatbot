from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from django.http import HttpResponseForbidden
from functools import wraps
from .models import ProductView, SalesSummary
from products.models import Product

def superuser_required(view_func):
    """
    Decorator to restrict access to superusers only.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@login_required
@superuser_required
def popular_products(request):
    """
    Fetch and display the top 10 most viewed products.
    """
    popular_products = (
        Product.objects.annotate(view_count=Count('views'))
        .order_by('-view_count')[:10]
    )
    return render(request, 'analytics/popular_products.html', {'popular_products': popular_products})


@login_required
@superuser_required
def total_sales(request):
    """
    Calculate and display the total sales.
    """
    total_sales = SalesSummary.objects.aggregate(total_price_sum=Sum('total_price'))['total_price_sum'] or 0
    return render(request, 'analytics/total_sales.html', {'total_sales': total_sales})
