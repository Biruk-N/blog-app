from django.contrib import admin
from .models import Post, Category, Tag, PostView

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""
    list_display = ['name', 'slug', 'created_at', 'post_count']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    def post_count(self, obj):
        return obj.posts.filter(status='published').count()
    post_count.short_description = 'Published Posts'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model"""
    list_display = ['name', 'slug', 'created_at', 'post_count']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    def post_count(self, obj):
        return obj.posts.filter(status='published').count()
    post_count.short_description = 'Published Posts'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model"""
    list_display = [
        'title', 'author', 'status', 'category', 'created_at',
        'published_at', 'view_count', 'is_featured'
    ]
    list_filter = [
        'status', 'is_featured', 'created_at', 'published_at',
        'category', 'tags'
    ]
    search_fields = ['title', 'content', 'excerpt', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('Author & Status', {
            'fields': ('author', 'status', 'published_at', 'scheduled_at')
        }),
        ('Organization', {
            'fields': ('category', 'tags', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'view_count']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')
    
    def unique_views_count(self, obj):
        return obj.get_unique_views_count()
    unique_views_count.short_description = 'Unique Views'
    
    def reading_time_display(self, obj):
        return f"{obj.reading_time} min"
    reading_time_display.short_description = 'Reading Time'

@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    """Admin interface for PostView model"""
    list_display = ['post', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at', 'post__status']
    search_fields = ['post__title', 'user__username', 'ip_address']
    date_hierarchy = 'viewed_at'
    ordering = ['-viewed_at']
    
    fieldsets = (
        ('View Information', {
            'fields': ('post', 'user', 'session_key', 'ip_address', 'user_agent')
        }),
        ('Timing', {
            'fields': ('viewed_at',)
        }),
    )
    
    readonly_fields = ['viewed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post', 'user')
