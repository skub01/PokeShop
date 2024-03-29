from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from item.models import Item
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.quantity * item.item.price for item in cart_items)

    return render(request, 'cart/cart_view.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:view_cart')

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:view_cart')

@login_required
def process_payment(request):
    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.items.all()
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    user_cart.items.all().delete()

    return render(request, 'checkout/order.html', {'ordered_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.quantity * item.item.price for item in cart_items)

    return render(request, 'cart/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def order(request, order_id):
    ordered_items = CartItem.objects.filter(order__id=order_id)
    total_price = sum(item.quantity * item.item.price for item in ordered_items)

    context = {
        'ordered_items': ordered_items,
        'total_price': total_price,
    }

    return render(request, 'checkout/order.html', context)