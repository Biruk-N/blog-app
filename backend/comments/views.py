from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Comment
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    CommentModerationSerializer
)

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors to edit their comments"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only to the author
        return obj.author == request.user

class IsModeratorOrReadOnly(permissions.BasePermission):
    """Custom permission for comment moderation"""
    
    def has_permission(self, request, view):
        # Allow read access to everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Require authentication for write operations
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Moderation permissions for staff
        if request.user.is_staff:
            return True
        
        # Write permissions only to the author
        return obj.author == request.user

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model"""
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsModeratorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'post', 'parent', 'is_edited']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at', 'likes_count']
    ordering = ['created_at']
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        # Get the post filter from query params
        post_filter = self.request.query_params.get('post')
        
        # Base queryset - only top-level comments (parent is null)
        queryset = Comment.objects.filter(parent__isnull=True)
        
        # Apply post filter if provided
        if post_filter:
            queryset = queryset.filter(post_id=post_filter)
        
        # Add related fields for performance
        queryset = queryset.select_related('author', 'post').prefetch_related(
            'replies__author',
            'replies__replies__author'
        )
        
        # If user is not authenticated, only show approved comments
        if not self.request.user.is_authenticated:
            return queryset.filter(status='approved')
        
        # If user is staff, show all comments
        if self.request.user.is_staff:
            return queryset
        
        # If user is authenticated, show approved comments + their own comments
        return queryset.filter(
            Q(status='approved') | Q(author=self.request.user)
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer
        elif self.action == 'retrieve':
            return CommentDetailSerializer
        elif self.action == 'moderate':
            return CommentModerationSerializer
        return CommentListSerializer
    
    def get_serializer_context(self):
        """Add context for serializers"""
        context = super().get_serializer_context()
        return context
    
    def perform_create(self, serializer):
        """Set the author when creating a comment"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a comment"""
        comment = self.get_object()
        comment.increment_likes()
        return Response({'message': 'Comment liked'})
    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a comment"""
        comment = self.get_object()
        comment.decrement_likes()
        return Response({'message': 'Comment unliked'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def moderate(self, request, pk=None):
        """Moderate a comment (admin only)"""
        comment = self.get_object()
        serializer = CommentModerationSerializer(
            comment,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Comment moderated successfully',
                'comment': CommentDetailSerializer(comment, context={'request': request}).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_comments(self, request):
        """Get current user's comments"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        comments = self.get_queryset().filter(author=request.user)
        serializer = CommentListSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def pending(self, request):
        """Get pending comments for moderation (admin only)"""
        comments = self.get_queryset().filter(status='pending')
        serializer = CommentListSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def spam(self, request):
        """Get spam comments (admin only)"""
        comments = self.get_queryset().filter(status='spam')
        serializer = CommentListSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get replies for a specific comment"""
        comment = self.get_object()
        replies = comment.replies.filter(status='approved').order_by('created_at')
        serializer = CommentReplySerializer(replies, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def for_post(self, request):
        """Get comments for a specific post (top-level only with nested replies)"""
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response(
                {'error': 'post_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get top-level comments for the post
        comments = Comment.objects.filter(
            post_id=post_id,
            parent__isnull=True
        ).select_related('author', 'post').prefetch_related(
            'replies__author',
            'replies__replies__author'
        )
        
        # Apply permission filtering
        if not request.user.is_authenticated:
            comments = comments.filter(status='approved')
        elif not request.user.is_staff:
            comments = comments.filter(
                Q(status='approved') | Q(author=request.user)
            )
        
        serializer = CommentListSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
