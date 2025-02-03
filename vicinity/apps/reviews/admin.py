from django.contrib import admin
from .models import Review, ReviewImage

# Register your models here.

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('business', 'user', 'rating', 'created_at', 'is_published')
    list_filter = ('rating', 'is_published', 'created_at')
    search_fields = ('business__name', 'user__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReviewImageInline]
