from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
import re

User = get_user_model()

class Category(models.Model):
    """Category model for organizing posts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    """Tag model for post tagging"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class PostView(models.Model):
    """Model for tracking post views with session and user tracking"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['post', 'viewed_at']),
            models.Index(fields=['user', 'viewed_at']),
            models.Index(fields=['session_key', 'viewed_at']),
        ]
        # Prevent duplicate views from same user/session within 24 hours
        unique_together = [['post', 'session_key'], ['post', 'user']]
    
    def __str__(self):
        return f"View of {self.post.title} at {self.viewed_at}"

class Post(models.Model):
    """Post model for blog posts"""
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]
    
    # Primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic fields
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text=_('Short summary of the post'))
    
    # Author and status
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # Categories and tags
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )
    
    # Media
    featured_image = models.ImageField(
        upload_to='posts/featured/',
        blank=True,
        null=True,
        help_text=_('Featured image for the post')
    )
    
    # SEO and metadata
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('SEO title (if different from post title)')
    )
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        help_text=_('SEO description')
    )
    
    # Publishing
    published_at = models.DateTimeField(blank=True, null=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Engagement
    view_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['author', 'status']),
            models.Index(fields=['category', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            self.excerpt = self.content[:200] + '...' if len(self.content) > 200 else self.content
        
        # Auto-generate meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.excerpt
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
    def increment_view_count(self):
        """Increment the view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def record_view(self, request):
        """Record a view with session and user tracking"""
        try:
            # Get user and session info
            user = request.user if request.user.is_authenticated else None
            session_key = request.session.session_key
            ip_address = self._get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Create view record
            PostView.objects.create(
                post=self,
                user=user,
                session_key=session_key,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Increment view count
            self.increment_view_count()
            
        except Exception as e:
            # Log error but don't break the request
            print(f"Error recording view: {e}")
    
    def _get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_unique_views_count(self):
        """Get count of unique views (by user or session)"""
        return self.views.count()
    
    def get_recent_views(self, days=7):
        """Get views from the last N days"""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.views.filter(viewed_at__gte=cutoff_date)
    
    @property
    def is_published(self):
        """Check if post is published"""
        return self.status == 'published' and self.published_at is not None
    
    @property
    def reading_time(self):
        """Estimate reading time in minutes with improved calculation"""
        # Remove HTML tags for better word counting
        clean_content = re.sub(r'<[^>]+>', '', self.content)
        # Remove extra whitespace and split into words
        words = clean_content.strip().split()
        word_count = len(words)
        
        # Average reading speed: 200-250 words per minute
        # Use 225 as a middle ground
        words_per_minute = 225
        
        # Calculate reading time
        reading_time = word_count / words_per_minute
        
        # Return at least 1 minute, round to nearest minute
        return max(1, round(reading_time))
    
    @property
    def word_count(self):
        """Get the word count of the post content"""
        clean_content = re.sub(r'<[^>]+>', '', self.content)
        words = clean_content.strip().split()
        return len(words)
    
    @property
    def character_count(self):
        """Get the character count of the post content"""
        clean_content = re.sub(r'<[^>]+>', '', self.content)
        return len(clean_content)
