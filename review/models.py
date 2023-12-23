from django.contrib.auth.models import User
from django.db import models

class Rating(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return self.name
    
class Review(models.Model):
    rating = models.ForeignKey(Rating, related_name='reviews', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(User, related_name='reviews_written', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='reviews_received', on_delete=models.CASCADE)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.seller.username}"