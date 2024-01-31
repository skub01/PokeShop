from django.urls import path
from .views import view_cart, add_to_cart, delete_item, checkout, order

app_name = 'cart'

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('checkout', checkout, name='checkout'),
    path('order/<int:order_id>/', checkout, name='order'),
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
]
