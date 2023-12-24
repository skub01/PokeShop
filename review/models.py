from django.contrib.auth.models import User
from django.db import models
    
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
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(User, related_name='reviews_written', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='reviews_received', on_delete=models.CASCADE)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.seller.username}"