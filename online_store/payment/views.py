import json

from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect, render

from cart.models import CartItem
from .models import Order, OrderDetails

import braintree

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
      braintree.Environment.Sandbox,
      merchant_id=settings.BRAINTREE_MERCHANT_ID,
      public_key=settings.BRAINTREE_PUBLIC_KEY,
      private_key=settings.BRAINTREE_PRIVATE_KEY
  )
)


@login_required
def billing(request, amount):
    client_payment_token = gateway.client_token.generate()
    context = {
        "client_token": client_payment_token,
        "amount": amount
    }
    return render(request, "payment/payment.html", context=context)


@login_required
def complete_payment(request):
    if request.method == "POST":
        post_data = json.loads(request.body)

        nonce = post_data.get("paymentMethodNonce", None)
        amount = post_data.get("amount", None)

        result = gateway.transaction.sale({
            'amount': amount,
            "payment_method_nonce": nonce,
            'options': {
                "submit_for_settlement": True
            }
        })

        if result.is_success or result.transaction:
            save_order(request.user.id, amount)
            print("suc")
            return redirect("payment:payment_success")
        else:
            print("not")
            return HttpResponse(
                json.dumps({"result": "error", "message": result["message"]}),
                content_type="application/json",
            )


def save_order(current_user_id, amount):
    cart_items = CartItem.objects.filter(user_id=current_user_id)

    if not cart_items.exists():
        return

    order = Order.objects.create(
        user_id=current_user_id,
        date=timezone.now().date(),
        unit_price=amount,
        status='payed'
    )

    for cart_item in cart_items:
        OrderDetails.objects.create(
            order=order,
            item=cart_item.product,
            quantity=cart_item.quantity
        )
        cart_item.delete()


def payment_success(request):
    return render(request, 'payment/payment_success.html')
