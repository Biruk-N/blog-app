from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from posts.models import Post
import uuid

User = get_user_model()

class Reaction(models.Model):
    """Reaction model for emoji reactions on posts"""
    REACTION_CHOICES = [
        ('like', '👍'),
        ('love', '❤️'),
        ('laugh', '😂'),
        ('wow', '😮'),
        ('sad', '😢'),
        ('angry', '😠'),
        ('fire', '🔥'),
        ('rocket', '🚀'),
        ('eyes', '👀'),
        ('clap', '👏'),
        ('pray', '🙏'),
        ('muscle', '💪'),
        ('brain', '🧠'),
        ('heart_eyes', '😍'),
        ('sunglasses', '😎'),
        ('party', '🎉'),
        ('star', '⭐'),
        ('thumbs_up', '👍'),
        ('thumbs_down', '👎'),
        ('check', '✅'),
    ]
    
    # Primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    
    # Reaction type
    reaction_type = models.CharField(
        max_length=20,
        choices=REACTION_CHOICES,
        help_text=_('Type of reaction')
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user', 'reaction_type']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'reaction_type']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['post', 'user']),
        ]
    
    def __str__(self):
        return f'{self.user.username} reacted {self.get_reaction_type_display()} to {self.post.title}'
    
    @classmethod
    def get_reaction_counts(cls, post):
        """Get reaction counts for a post"""
        return cls.objects.filter(post=post).values('reaction_type').annotate(
            count=models.Count('reaction_type')
        ).order_by('-count')
    
    @classmethod
    def get_user_reactions(cls, user, post):
        """Get user's reactions for a specific post"""
        return cls.objects.filter(user=user, post=post).values_list('reaction_type', flat=True)
    
    @classmethod
    def toggle_reaction(cls, user, post, reaction_type):
        """Toggle a reaction (add if not exists, remove if exists)"""
        reaction, created = cls.objects.get_or_create(
            user=user,
            post=post,
            reaction_type=reaction_type
        )
        
        if not created:
            # Reaction already exists, remove it
            reaction.delete()
            return False, 'removed'
        
        return True, 'added'
    
    @classmethod
    def get_popular_reactions(cls, post, limit=5):
        """Get most popular reactions for a post"""
        return cls.objects.filter(post=post).values('reaction_type').annotate(
            count=models.Count('reaction_type')
        ).order_by('-count')[:limit]
