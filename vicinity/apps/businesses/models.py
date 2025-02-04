from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Business(models.Model):
    """
    Model representing a business in the Vicinity platform.
    """

    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('retail', 'Retail'),
        ('service', 'Service'),
        ('entertainment', 'Entertainment'),
        ('health', 'Health & Wellness'),
        ('professional', 'Professional Services'),
        ('other', 'Other'),
    ]

    # Basic Information
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_businesses'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()

    # Contact & Location
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    # Business Hours
    hours_of_operation = models.JSONField(default=dict, blank=True)

    # Media
    logo = models.ImageField(
        upload_to='business_logos/',
        null=True,
        blank=True,
    )

    # Metrics
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    review_count = models.PositiveIntegerField(default=0)

    # Status and Verification
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name

class BusinessImage(models.Model):
    """
    Model for storing multiple images for a business.
    """
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="business_images/")
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    craeted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Business Image'
        verbose_name_plural = 'Business Images'
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f'Image for {self.business.name}'
    
    def save(self, *args, **kwargs):
        # ensure only one primary image per business
        if self.is_primary:
            self.__class__.objects.filter(
                business=self.business,
                is_primary=True
            ).update(is_primary=False)
        super().save(*args, **kwargs)
