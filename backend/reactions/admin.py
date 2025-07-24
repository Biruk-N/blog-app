from django.contrib import admin
from .models import Reaction

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    """Admin interface for Reaction model"""
    list_display = [
        'user', 'post', 'reaction_type', 'reaction_emoji',
        'created_at'
    ]
    list_filter = [
        'reaction_type', 'created_at', 'post__category',
        'user'
    ]
    search_fields = ['user__username', 'post__title', 'reaction_type']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Reaction Details', {
            'fields': ('user', 'post', 'reaction_type')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def reaction_emoji(self, obj):
        """Show the emoji for the reaction type"""
        return dict(Reaction.REACTION_CHOICES).get(obj.reaction_type, '')
    reaction_emoji.short_description = 'Emoji'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'post')
    
    actions = ['delete_selected']
    
    def has_add_permission(self, request):
        """Disable adding reactions from admin"""
        return False
