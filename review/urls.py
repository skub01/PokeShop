from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('<str:username>/', views.user_reviews, name='user_reviews'),
    path('<str:username>/new/', views.new, name='new'),
    path('<str:username>/delete/<int:pk>/', views.delete, name='delete'),
    path('<str:username>/edit/<int:pk>/', views.edit, name='edit'),
]