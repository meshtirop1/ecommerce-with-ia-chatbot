# ecommerce/views.py
from django.shortcuts import render


def about(request):
    return render(request, 'pages/about.html')

def privacy(request):
    return render(request, 'pages/privacy.html')

def terms(request):
    return render(request, 'pages/terms.html')
