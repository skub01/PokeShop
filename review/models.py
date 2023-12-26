from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
    
class Review(models.Model):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5

    STAR_CHOICES = [
        (ONE_STAR, '1 star'),
        (TWO_STARS, '2 stars'),
        (THREE_STARS, '3 stars'),
        (FOUR_STARS, '4 stars'),
        (FIVE_STARS, '5 stars'),
    ]

    rating = models.IntegerField(choices=STAR_CHOICES)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(User, related_name='reviews_written', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='reviews_received', on_delete=models.CASCADE)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.seller.username}"
    
    def display_stars(self):
        full_stars = '★' * self.rating
        empty_stars = '☆' * (5 - self.rating)
        return full_stars + empty_stars
    
    def average_rating(self):
        seller_reviews = Review.objects.filter(seller=self.seller)
        average = seller_reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average, 2) if average is not None else 0.0
