from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin Configuration"""
    list_display = ('username', 'email',
                    'user_type', 'bio',
                    'is_staff', 'date_joined'
                    )
    list_filter = ('user_type', 'is_staff',
                   'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('user_type', 'phone_number', 'bio', 'profile_picture')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('user_type', 'phone_number', 'bio', 'profile_picture')
        }),
    )
