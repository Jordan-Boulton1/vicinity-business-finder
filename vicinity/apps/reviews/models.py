from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.businesses.models import Business

# Create your models here.

class Review(models.Model):
    """
    Model for storing business reviews and ratings
    """
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=255)
    content = models.TextField()

    # review status
    is_published = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']
        # ensure unique reviews per user per business
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'business'],
                name='unique_user_business_review'
            )
        ]
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.business.name}."
    
    def save(self, *args, **kwargs):
        # update business average rating
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # recalculate business average rating
        business = self.business
        avg_rating = business.reviews.filter(is_published=True).aggregate(
            models.Avg('rating'))['rating__avg'] or 0
        business.average_rating = round(avg_rating, 2)

        # update review count for new reviews
        if is_new:
            business.review_count = business.reviews.filter(is_published=True).count()

        business.save()

class ReviewImage(models.Model):
    """
    Model for storing images associated with reviews
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="review_images/")
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review Image'
        verbose_name_plural = 'Review Images'
        ordering = ['created_at']

    def __str__(self):
        return f'Image for {self.review}'
