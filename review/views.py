from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from item.models import Item
from .models import User, Review
from django.contrib.auth import get_user_model
from .forms import NewReviewForm, EditReviewForm
from django.db.models import Avg
from random import shuffle


def user_reviews(request, username):
    seller = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(seller=seller)
    items = list(Item.objects.filter(created_by=seller))
    shuffle(items)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    average_rating = round(average_rating, 2) if average_rating is not None else 0.0
    user_profile = get_user_model().objects.get(username=username)
    has_left_review = Review.objects.filter(reviewer=request.user, seller=user_profile).exists()

    return render(request, 'review/review.html', {
        'reviews': reviews, 
        'username': username,
        'items': items,
        'average_rating': average_rating,
        'has_left_review': has_left_review,
    })

@login_required
def new(request, username):
    if request.method == 'POST':
        form = NewReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.seller = User.objects.get(username=username) 
            review.save()

            return redirect(reverse('review:user_reviews', kwargs={'username': username}))
    else:
        form = NewReviewForm()

    return render(request, 'review/form.html', {
        'form': form,
        'title': 'New review',
        'seller': User.objects.get(username=username) 
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Review, pk=pk, created_by= request.user)

    if request.method == 'POST':
        form = EditReviewForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('user', pk=User.id)
    else:
        form = EditReviewForm(instance=item)

    return render(request, 'review/form.html', {
        'form': form,
        'title': 'Edit review',
    })

@login_required
def delete(request, pk):
    review = get_object_or_404(Review, pk=pk, created_by= request.user)
    review.delete()

    return redirect('dashboard:index')
