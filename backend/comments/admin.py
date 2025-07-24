from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model"""
    list_display = [
        'content_preview', 'author', 'post', 'status', 'parent',
        'created_at', 'likes_count', 'reply_count'
    ]
    list_filter = [
        'status', 'is_edited', 'created_at', 'updated_at',
        'post__category', 'author'
    ]
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at', 'likes_count']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('content', 'post', 'author', 'parent')
        }),
        ('Moderation', {
            'fields': ('status', 'is_edited')
        }),
        ('Statistics', {
            'fields': ('likes_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        """Show a preview of the comment content"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def reply_count(self, obj):
        """Show the number of replies"""
        return obj.replies.count()
    reply_count.short_description = 'Replies'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post', 'parent')
    
    actions = ['approve_comments', 'reject_comments', 'mark_as_spam']
    
    def approve_comments(self, request, queryset):
        """Approve selected comments"""
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} comments were successfully approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def reject_comments(self, request, queryset):
        """Reject selected comments"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} comments were successfully rejected.')
    reject_comments.short_description = "Reject selected comments"
    
    def mark_as_spam(self, request, queryset):
        """Mark selected comments as spam"""
        updated = queryset.update(status='spam')
        self.message_user(request, f'{updated} comments were marked as spam.')
    mark_as_spam.short_description = "Mark selected comments as spam"
