from django.contrib import admin
from .models import Business

# Register your models here.


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'owner', 'is_verified', 'average_rating')
    list_filter = ('category', 'city', 'is_verified', 'is_active')
    search_fields = ('name', 'description', 'address', 'city')
    readonly_fields = ('created_at', 'updated_at', 'average_rating', 'review_count')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'owner', 'category', 'description')
        }),
        ('Contact & Location', {
            'fields': ('email', 'phone', 'website', 'address', 'city', 'state', 'zip_code')
        }),
        ('Business Details', {
            'fields': ('hours_of_operation', 'logo')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Metrics', {
            'fields': ('average_rating', 'review_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )