import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .models import Payment
import logging
logger = logging.getLogger(__name__)



# Configure PayPal SDK with credentials
paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})


@login_required
def payment_process(request, order_id):
    """
    Handles PayPal payment creation for a specific order.
    """
    # Validate the order
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        # Create PayPal payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri('/payments/execute/').replace("http://", "https://"),
                "cancel_url": request.build_absolute_uri('/payments/cancel/').replace("http://", "https://")
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"Order {order.id}",
                        "sku": f"order-{order.id}",
                        "price": str(order.total_price),
                        "currency": "USD",  # Replace "USD" with dynamic currency if needed
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(order.total_price),
                    "currency": "USD"  # Replace "USD" with dynamic currency if needed
                },
                "description": f"Payment for Order {order.id}"
            }]
        })

        if payment.create():
            # Find approval URL and redirect the user
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
            messages.error(request, "PayPal approval URL not found.")
        else:
            # Log error details and show error message
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating PayPal payment: {payment.error}")
            messages.error(request, "An error occurred while creating the PayPal payment. Please try again.")

    # Render payment processing page with order details
    return render(request, 'payments/payment_process.html', {'order': order})

@login_required
def payment_execute(request, order_id=None):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        messages.error(request, "Missing payment details.")
        return redirect('cart_detail')

    try:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            # Validate transaction details
            try:
                order_id = payment.transactions[0].item_list.items[0].name.split(" ")[1]
                order = get_object_or_404(Order, id=order_id, user=request.user)
            except (IndexError, AttributeError):
                messages.error(request, "Invalid order information in the payment response.")
                return redirect('cart_detail')

            # Record payment
            Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price,
                payment_method="PayPal",
                status="Completed",
                transaction_id=payment.id
            )

            # Update order status
            order.status = "Paid"
            order.save()

            messages.success(request, "Payment completed successfully.")
            return redirect('payment_confirmation', payment_id=payment.id)
        else:
            messages.error(request, f"Payment execution failed: {payment.error}")
            return redirect('payment_process', order_id=order_id)

    except paypalrestsdk.ResourceNotFound:
        messages.error(request, "Payment not found.")
        return redirect('cart_detail')
    except Exception as e:
        logger.error(f"Unexpected error during payment execution: {e}")
        messages.error(request, "An unexpected error occurred during payment processing.")
        return redirect('cart_detail')

@login_required
def payment_confirmation(request, payment_id):
    """
    Displays payment confirmation details.
    """
    payment = get_object_or_404(Payment, transaction_id=payment_id, user=request.user)
    return render(request, 'payments/payment_confirmation.html', {'payment': payment})
