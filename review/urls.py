from django.urls import path
from .views import user_reviews

app_name = 'review'

urlpatterns = [
    path('<str:username>/', user_reviews, name='user_reviews'),
]