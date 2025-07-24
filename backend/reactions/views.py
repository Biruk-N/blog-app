from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Reaction
from .serializers import (
    ReactionSerializer,
    ReactionCreateSerializer,
    PostReactionsSerializer,
    ReactionToggleSerializer
)

class ReactionViewSet(viewsets.ModelViewSet):
    """ViewSet for Reaction model"""
    queryset = Reaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'user', 'reaction_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = Reaction.objects.select_related('user', 'post')
        
        # If user is staff, show all reactions
        if self.request.user.is_staff:
            return queryset
        
        # If user is authenticated, show their own reactions + public reactions
        return queryset.filter(
            user=self.request.user
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReactionCreateSerializer
        return ReactionSerializer
    
    def perform_create(self, serializer):
        """Set the user when creating a reaction"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle a reaction (add if not exists, remove if exists)"""
        serializer = ReactionToggleSerializer(data=request.data)
        if serializer.is_valid():
            reaction_type = serializer.validated_data['reaction_type']
            post_id = request.data.get('post_id')
            
            if not post_id:
                return Response(
                    {'error': 'post_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                from posts.models import Post
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response(
                    {'error': 'Post not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Toggle the reaction
            added, action = Reaction.toggle_reaction(
                user=request.user,
                post=post,
                reaction_type=reaction_type
            )
            
            # Get updated reaction data
            reaction_counts = Reaction.get_reaction_counts(post)
            user_reactions = Reaction.get_user_reactions(request.user, post)
            
            # Format response
            formatted_counts = []
            for count_data in reaction_counts:
                formatted_counts.append({
                    'reaction_type': count_data['reaction_type'],
                    'count': count_data['count'],
                    'user_reacted': count_data['reaction_type'] in user_reactions
                })
            
            return Response({
                'message': f'Reaction {action}',
                'reaction_counts': formatted_counts,
                'user_reactions': list(user_reactions),
                'total_reactions': sum(count['count'] for count in reaction_counts)
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def post_reactions(self, request):
        """Get reactions for a specific post"""
        post_id = request.query_params.get('post_id')
        
        if not post_id:
            return Response(
                {'error': 'post_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from posts.models import Post
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get reaction counts
        reaction_counts = Reaction.get_reaction_counts(post)
        user_reactions = []
        
        # Get user reactions if authenticated
        if request.user.is_authenticated:
            user_reactions = Reaction.get_user_reactions(request.user, post)
        
        # Format response
        formatted_counts = []
        for count_data in reaction_counts:
            formatted_counts.append({
                'reaction_type': count_data['reaction_type'],
                'count': count_data['count'],
                'user_reacted': count_data['reaction_type'] in user_reactions
            })
        
        return Response({
            'reaction_counts': formatted_counts,
            'user_reactions': list(user_reactions),
            'total_reactions': sum(count['count'] for count in reaction_counts)
        })
    
    @action(detail=False, methods=['get'])
    def my_reactions(self, request):
        """Get current user's reactions"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        reactions = self.get_queryset().filter(user=request.user)
        serializer = ReactionSerializer(reactions, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular_reactions(self, request):
        """Get popular reactions across all posts"""
        post_id = request.query_params.get('post_id')
        limit = int(request.query_params.get('limit', 5))
        
        if post_id:
            # Get popular reactions for specific post
            try:
                from posts.models import Post
                post = Post.objects.get(id=post_id)
                popular_reactions = Reaction.get_popular_reactions(post, limit)
            except Post.DoesNotExist:
                return Response(
                    {'error': 'Post not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Get popular reactions across all posts
            popular_reactions = Reaction.objects.values('reaction_type').annotate(
                count=Count('reaction_type')
            ).order_by('-count')[:limit]
        
        return Response(popular_reactions)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def analytics(self, request):
        """Get reaction analytics (admin only)"""
        total_reactions = Reaction.objects.count()
        reactions_by_type = Reaction.objects.values('reaction_type').annotate(
            count=Count('reaction_type')
        ).order_by('-count')
        
        # Get reactions by date (last 30 days)
        from django.utils import timezone
        from datetime import timedelta
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_reactions = Reaction.objects.filter(
            created_at__gte=thirty_days_ago
        ).count()
        
        return Response({
            'total_reactions': total_reactions,
            'recent_reactions': recent_reactions,
            'reactions_by_type': reactions_by_type
        })
