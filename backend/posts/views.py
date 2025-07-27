from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from .models import Post, Category, Tag
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    CategorySerializer,
    TagSerializer
)

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors to edit their posts"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the author
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model"""
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'category', 'tags', 'is_featured']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'view_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
        
        # If user is not authenticated, only show published posts
        if not self.request.user.is_authenticated:
            return queryset.filter(status='published', published_at__lte=timezone.now())
        
        # If user is authenticated, show their own posts + published posts
        if self.request.user.is_staff:
            return queryset  # Staff can see all posts
        else:
            return queryset.filter(
                Q(status='published', published_at__lte=timezone.now()) |
                Q(author=self.request.user)
            )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    def perform_create(self, serializer):
        """Set the author when creating a post"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a draft post"""
        post = self.get_object()
        
        if post.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only publish your own posts'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if post.status == 'published':
            return Response(
                {'error': 'Post is already published'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        post.status = 'published'
        post.published_at = timezone.now()
        post.save()
        
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to automatically record views for published posts"""
        post = self.get_object()
        
        # Record view for published posts
        if post.is_published:
            post.record_view(request)
        
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """Increment view count for a post (manual increment)"""
        post = self.get_object()
        post.record_view(request)
        return Response({
            'message': 'View count incremented',
            'view_count': post.view_count
        })
    
    @action(detail=True, methods=['get'])
    def debug_views(self, request, pk=None):
        """Debug endpoint to check view recording"""
        post = self.get_object()
        views = post.views.all()
        return Response({
            'post_id': str(post.id),
            'post_title': post.title,
            'view_count': post.view_count,
            'total_views_recorded': views.count(),
            'views': [
                {
                    'id': str(view.id),
                    'user': view.user.username if view.user else 'Anonymous',
                    'session_key': view.session_key,
                    'ip_address': view.ip_address,
                    'viewed_at': view.viewed_at
                }
                for view in views[:10]  # Show first 10 views
            ]
        })
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Get analytics data for a post"""
        post = self.get_object()
        
        # Check permissions - only author or staff can see analytics
        if post.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You can only view analytics for your own posts'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get analytics data
        total_views = post.view_count
        unique_views = post.get_unique_views_count()
        recent_views = post.get_recent_views(days=7).count()
        
        # Get views by day for the last 30 days
        from django.db.models import Count
        from django.utils import timezone
        from datetime import timedelta
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_views = post.views.filter(
            viewed_at__gte=thirty_days_ago
        ).extra(
            select={'day': 'date(viewed_at)'}
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        analytics_data = {
            'total_views': total_views,
            'unique_views': unique_views,
            'recent_views_7_days': recent_views,
            'reading_time': post.reading_time,
            'word_count': post.word_count,
            'character_count': post.character_count,
            'daily_views': list(daily_views),
        }
        
        return Response(analytics_data)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """Get current user's posts"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        posts = self.get_queryset().filter(author=request.user)
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def drafts(self, request):
        """Get current user's draft posts"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        posts = self.get_queryset().filter(
            author=request.user,
            status='draft'
        )
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured posts"""
        posts = self.get_queryset().filter(
            is_featured=True,
            status='published',
            published_at__lte=timezone.now()
        )
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Category model (read-only)"""
    queryset = Category.objects.annotate(post_count=Count('posts', filter=Q(posts__status='published')))
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """Get posts for a specific category"""
        category = self.get_object()
        posts = Post.objects.filter(
            category=category,
            status='published',
            published_at__lte=timezone.now()
        ).select_related('author').prefetch_related('tags')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Tag model (read-only)"""
    queryset = Tag.objects.annotate(post_count=Count('posts', filter=Q(posts__status='published')))
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def posts(self, request, slug=None):
        """Get posts for a specific tag"""
        tag = self.get_object()
        posts = Post.objects.filter(
            tags=tag,
            status='published',
            published_at__lte=timezone.now()
        ).select_related('author').prefetch_related('tags')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
