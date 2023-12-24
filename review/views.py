from django.shortcuts import render, get_object_or_404
from .models import Review
from django.contrib.auth.models import User

def user_reviews(request, username):
    seller = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(seller=seller)

    return render(request, 'review.html', {'reviews': reviews, 'username': username})
