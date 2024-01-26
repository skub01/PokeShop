from django.db import models
from django.contrib.auth.models import User
from item.models import Item
from django.shortcuts import render

def process_payment(request):
    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.items.all()
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    user_cart.items.all().delete()

    return render(request, 'checkout/order.html', {'ordered_items': cart_items, 'total_price': total_price})

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.cart}"
