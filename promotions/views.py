from django.shortcuts import redirect
from django.contrib import messages
from .models import Coupon
from orders.models import Order


def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()  # Get and clean the coupon code
        if not code:
            messages.error(request, "Please enter a valid coupon code.")
            return redirect('checkout')

        try:
            # Validate coupon
            coupon = Coupon.objects.get(code=code, active=True)
            if not coupon.is_valid():
                messages.error(request, "This coupon is not valid or has expired.")
                return redirect('checkout')

            # Check for active order in session
            order_id = request.session.get('order_id')
            if not order_id:
                messages.error(request, "No active order found. Please try again.")
                return redirect('checkout')

            try:
                # Retrieve the order and apply the coupon
                order = Order.objects.get(id=order_id)

                # Prevent re-applying the same coupon
                if request.session.get('coupon_code') == code:
                    messages.info(request, "This coupon is already applied to your order.")
                    return redirect('checkout')

                discount_amount = order.total_price * (coupon.discount / 100)
                order.total_price -= discount_amount
                order.save()

                # Save coupon in session and show success message
                request.session['coupon_code'] = coupon.code
                messages.success(request, f"Coupon applied! You saved {coupon.discount}%.")
                return redirect('checkout')

            except Order.DoesNotExist:
                messages.error(request, "Order not found.")
                return redirect('checkout')

        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or inactive coupon code.")
            return redirect('checkout')

    messages.error(request, "Invalid request method.")
    return redirect('checkout')
