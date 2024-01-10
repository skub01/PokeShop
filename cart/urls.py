from django.urls import path
from .views import view_cart, delete_item

app_name = 'cart'

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
]
