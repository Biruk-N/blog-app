from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin interface for CustomUser model"""
    
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_active', 'is_verified', 'date_joined'
    ]
    list_filter = [
        'is_staff', 'is_active', 'is_verified', 'date_joined',
        'groups', 'user_permissions'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'email', 'bio',
                'avatar', 'website', 'location', 'date_of_birth'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_verified', 'groups', 'user_permissions'
            ),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'is_staff', 'is_active'
            ),
        }),
    )
