from django.shortcuts import render
from .models import Review

def seller_info(request):
    reviews_received = Review.objects.filter(seller=request.user)

    return render(request, 'dashboard/seller_info.html', {
        'reviews_received': reviews_received,
    })
