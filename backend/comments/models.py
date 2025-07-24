from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from posts.models import Post

User = get_user_model()

class Comment(models.Model):
    """Comment model for blog posts with nested comments support"""
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('spam', _('Spam')),
    ]
    
    # Basic fields
    content = models.TextField()
    
    # Relationships
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    # Nested comments
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # Moderation
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='approved'
    )
    is_edited = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Engagement
    likes_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'status', 'created_at']),
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['parent', 'created_at']),
        ]
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def save(self, *args, **kwargs):
        # Mark as edited if this is an update
        if self.pk:
            self.is_edited = True
        super().save(*args, **kwargs)
    
    @property
    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None
    
    @property
    def has_replies(self):
        """Check if this comment has replies"""
        return self.replies.exists()
    
    @property
    def reply_count(self):
        """Get the number of replies to this comment"""
        return self.replies.count()
    
    def get_replies(self):
        """Get approved replies to this comment"""
        return self.replies.filter(status='approved').order_by('created_at')
    
    def increment_likes(self):
        """Increment the likes count"""
        self.likes_count += 1
        self.save(update_fields=['likes_count'])
    
    def decrement_likes(self):
        """Decrement the likes count"""
        if self.likes_count > 0:
            self.likes_count -= 1
            self.save(update_fields=['likes_count'])
    
    def get_ancestors(self):
        """Get all ancestor comments (for nested display)"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return list(reversed(ancestors))
    
    def get_descendants(self):
        """Get all descendant comments"""
        descendants = []
        for reply in self.replies.all():
            descendants.append(reply)
            descendants.extend(reply.get_descendants())
        return descendants
