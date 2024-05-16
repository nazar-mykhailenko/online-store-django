from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.models import Item

from .models import CartItem

@login_required
def cart(request):
    current_user_id = request.user.id
    cart_items = CartItem.objects.filter(user_id=current_user_id)
    total = sum(map(lambda cart_item: cart_item.get_total(), cart_items))
    return render(request, 'cart/cart.html', {
        "cart_empty": len(cart_items) == 0,
        "cart_items": cart_items,
        "total": total
    })


@login_required
def cart_add(request, product_id):
    current_user_id = request.user.id
    product_count = Item.objects.filter(id=product_id).count()
    if product_count == 0:
        return redirect('cart:cart')

    cart_item = CartItem.objects.filter(user_id=current_user_id).filter(product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem.objects.create(user=request.user, product_id=product_id, quantity=1)

    return redirect('cart:cart')


@login_required
def cart_remove(request, product_id):
    current_user_id = request.user.id
    cart_item = CartItem.objects.filter(user_id=current_user_id).filter(product_id=product_id).first()
    if not cart_item:
        return redirect('cart:cart')

    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart:cart')


@login_required
def cart_remove_completely(request, product_id):
    current_user_id = request.user.id
    cart_item = CartItem.objects.filter(user_id=current_user_id).filter(product_id=product_id).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart:cart')
