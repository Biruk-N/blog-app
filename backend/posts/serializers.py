from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Category, Tag

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'post_count']
        read_only_fields = ['slug', 'created_at']
    
    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()

class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at', 'post_count']
        read_only_fields = ['slug', 'created_at']
    
    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()

class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user serializer for post relationships"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']

class PostListSerializer(serializers.ModelSerializer):
    """Serializer for listing posts (minimal info)"""
    author = UserMinimalSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'category',
            'tags', 'featured_image', 'status', 'published_at',
            'created_at', 'view_count', 'is_featured', 'reading_time',
            'comment_count', 'reaction_count'
        ]
        read_only_fields = ['slug', 'created_at', 'published_at', 'view_count']
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_reaction_count(self, obj):
        return obj.reactions.count()

class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed post view"""
    author = UserMinimalSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author',
            'category', 'tags', 'featured_image', 'status',
            'meta_title', 'meta_description', 'published_at',
            'scheduled_at', 'created_at', 'updated_at', 'view_count',
            'is_featured', 'reading_time', 'comment_count', 'reaction_count'
        ]
        read_only_fields = [
            'slug', 'created_at', 'updated_at', 'published_at',
            'view_count', 'comment_count', 'reaction_count'
        ]
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_reaction_count(self, obj):
        return obj.reactions.count()

class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating posts"""
    category_id = serializers.IntegerField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list
    )
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'category_id', 'tag_ids',
            'featured_image', 'status', 'meta_title', 'meta_description',
            'scheduled_at'
        ]
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        
        # Set the author
        validated_data['author'] = self.context['request'].user
        
        # Create the post
        post = Post.objects.create(**validated_data)
        
        # Set category if provided
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                post.category = category
                post.save()
            except Category.DoesNotExist:
                pass
        
        # Set tags if provided
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            post.tags.set(tags)
        
        return post

class PostUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating posts"""
    category_id = serializers.IntegerField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'category_id', 'tag_ids',
            'featured_image', 'status', 'meta_title', 'meta_description',
            'scheduled_at'
        ]
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', None)
        
        # Update the post
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update category if provided
        if category_id is not None:
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                    instance.category = category
                except Category.DoesNotExist:
                    instance.category = None
            else:
                instance.category = None
        
        instance.save()
        
        # Update tags if provided
        if tag_ids is not None:
            tags = Tag.objects.filter(id__in=tag_ids)
            instance.tags.set(tags)
        
        return instance 