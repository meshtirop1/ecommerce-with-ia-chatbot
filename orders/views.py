# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import Order, ShippingStatus
#
# @login_required
# def order_history(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'orders/order_history.html', {'orders': orders})
#
# @login_required
# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id, user=request.user)
#     shipping_status = ShippingStatus.objects.get(order=order)
#     return render(request, 'orders/order_detail.html', {
#         'order': order,
#         'shipping_status': shipping_status,
#     })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, ShippingStatus


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    try:
        shipping_status = ShippingStatus.objects.get(order=order)
    except ShippingStatus.DoesNotExist:
        shipping_status = None
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'shipping_status': shipping_status,
    })


