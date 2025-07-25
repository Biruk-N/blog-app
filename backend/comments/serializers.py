from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment

User = get_user_model()

class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user serializer for comment relationships"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']

class CommentReplySerializer(serializers.ModelSerializer):
    """Serializer for comment replies (nested)"""
    author = UserMinimalSerializer(read_only=True)
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'parent', 'status',
            'created_at', 'updated_at', 'is_edited', 'likes_count',
            'reply_count'
        ]
        read_only_fields = ['author', 'status', 'created_at', 'updated_at', 'likes_count']
    
    def get_reply_count(self, obj):
        return obj.replies.filter(status='approved').count()

class CommentListSerializer(serializers.ModelSerializer):
    """Serializer for listing comments"""
    author = UserMinimalSerializer(read_only=True)
    replies = CommentReplySerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'parent', 'status',
            'created_at', 'updated_at', 'is_edited', 'likes_count',
            'replies', 'reply_count'
        ]
        read_only_fields = ['author', 'status', 'created_at', 'updated_at', 'likes_count']
    
    def get_reply_count(self, obj):
        return obj.replies.filter(status='approved').count()

class CommentDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed comment view"""
    author = UserMinimalSerializer(read_only=True)
    replies = CommentReplySerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'parent', 'status',
            'created_at', 'updated_at', 'is_edited', 'likes_count',
            'replies', 'reply_count'
        ]
        read_only_fields = ['author', 'status', 'created_at', 'updated_at', 'likes_count']
    
    def get_reply_count(self, obj):
        return obj.replies.filter(status='approved').count()

class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating comments"""
    post_id = serializers.UUIDField(required=True)
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    
    class Meta:
        model = Comment
        fields = ['content', 'post_id', 'parent_id']
    
    def validate_post_id(self, value):
        """Validate post exists"""
        from posts.models import Post
        try:
            Post.objects.get(id=value)
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post does not exist")
        return value
    
    def validate_parent_id(self, value):
        """Validate parent comment exists and belongs to same post"""
        if value:
            try:
                parent_comment = Comment.objects.get(id=value)
                # Check if parent comment is approved
                if parent_comment.status != 'approved':
                    raise serializers.ValidationError("Cannot reply to an unapproved comment")
            except Comment.DoesNotExist:
                raise serializers.ValidationError("Parent comment does not exist")
        return value
    
    def create(self, validated_data):
        parent_id = validated_data.pop('parent_id', None)
        post_id = validated_data.pop('post_id')
        
        # Set the author
        validated_data['author'] = self.context['request'].user
        
        # Get the post
        from posts.models import Post
        try:
            post = Post.objects.get(id=post_id)
            validated_data['post'] = post
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post does not exist")
        
        # Set parent if provided
        if parent_id:
            validated_data['parent_id'] = parent_id
        
        return Comment.objects.create(**validated_data)

class CommentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating comments"""
    
    class Meta:
        model = Comment
        fields = ['content']
    
    def validate(self, attrs):
        """Only allow editing own comments"""
        user = self.context['request'].user
        comment = self.instance
        
        if comment.author != user:
            raise serializers.ValidationError("You can only edit your own comments")
        
        return attrs

class CommentModerationSerializer(serializers.ModelSerializer):
    """Serializer for moderating comments (admin only)"""
    
    class Meta:
        model = Comment
        fields = ['status']
    
    def validate_status(self, value):
        """Validate status change"""
        comment = self.instance
        if comment.status == 'spam' and value != 'spam':
            # Allow unmarking spam
            return value
        elif comment.status == 'rejected' and value == 'approved':
            # Allow approving rejected comments
            return value
        elif comment.status == 'pending' and value in ['approved', 'rejected', 'spam']:
            # Allow moderating pending comments
            return value
        else:
            raise serializers.ValidationError("Invalid status transition") 