from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem
from orders.models import Order, OrderItem  # Import Order and OrderItem from orders.models
from products.models import Product
from promotions.models import Coupon  # Import the Coupon model


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'checkout/cart_detail.html', context)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Add items before checking out.")
        return redirect('cart_detail')

    total_price = sum(item.get_total_price() for item in cart_items)
    discount_amount = 0

    coupon_code = request.session.get('coupon_code')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            if coupon.is_valid():
                discount_amount = total_price * (coupon.discount / 100)
                total_price -= discount_amount
            else:
                del request.session['coupon_code']
        except Coupon.DoesNotExist:
            del request.session['coupon_code']

    # Check if an order exists or create a new one
    order = Order.objects.filter(user=request.user, status="Pending").first()
    if not order:
        order = Order.objects.create(user=request.user, total_price=total_price)

    if request.method == 'POST':
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.get_total_price()
            )
        cart_items.delete()

        if 'coupon_code' in request.session:
            del request.session['coupon_code']

        return redirect('payment_process', order_id=order.id)

    return render(request, 'checkout/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount_amount': discount_amount,
        'coupon_code': coupon_code,
        'order': order,  # Pass order to the template
    })
