from django.shortcuts import render, get_object_or_404

from analytics.models import ProductView
from .models import Product, Category


def shop(request):
    products = Product.objects.all()
    return render(request, 'products/shop.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        products = products.filter(category__slug=selected_category)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        ProductView.objects.create(product=product, user=request.user)
    else:
        ProductView.objects.create(product=product)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)
