from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Reaction

User = get_user_model()

class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user serializer for reaction relationships"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar']

class ReactionSerializer(serializers.ModelSerializer):
    """Serializer for Reaction model"""
    user = UserMinimalSerializer(read_only=True)
    reaction_emoji = serializers.SerializerMethodField()
    
    class Meta:
        model = Reaction
        fields = ['id', 'post', 'user', 'reaction_type', 'reaction_emoji', 'created_at']
        read_only_fields = ['user', 'created_at']
    
    def get_reaction_emoji(self, obj):
        """Get the emoji for the reaction type"""
        return dict(Reaction.REACTION_CHOICES).get(obj.reaction_type, '')

class ReactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating reactions"""
    
    class Meta:
        model = Reaction
        fields = ['post', 'reaction_type']
    
    def validate(self, attrs):
        """Validate reaction data"""
        user = self.context['request'].user
        post = attrs.get('post')
        reaction_type = attrs.get('reaction_type')
        
        # Check if reaction type is valid
        valid_types = [choice[0] for choice in Reaction.REACTION_CHOICES]
        if reaction_type not in valid_types:
            raise serializers.ValidationError(f"Invalid reaction type. Must be one of: {', '.join(valid_types)}")
        
        # Check if user already has this reaction on this post
        existing_reaction = Reaction.objects.filter(
            user=user,
            post=post,
            reaction_type=reaction_type
        ).first()
        
        if existing_reaction:
            raise serializers.ValidationError("You have already reacted with this emoji to this post")
        
        return attrs
    
    def create(self, validated_data):
        """Create the reaction"""
        validated_data['user'] = self.context['request'].user
        return Reaction.objects.create(**validated_data)

class ReactionCountSerializer(serializers.Serializer):
    """Serializer for reaction counts"""
    reaction_type = serializers.CharField()
    reaction_emoji = serializers.SerializerMethodField()
    count = serializers.IntegerField()
    user_reacted = serializers.BooleanField()
    
    def get_reaction_emoji(self, obj):
        """Get the emoji for the reaction type"""
        return dict(Reaction.REACTION_CHOICES).get(obj['reaction_type'], '')

class PostReactionsSerializer(serializers.Serializer):
    """Serializer for post reactions summary"""
    reaction_counts = ReactionCountSerializer(many=True)
    total_reactions = serializers.IntegerField()
    user_reactions = serializers.ListField(child=serializers.CharField())

class ReactionToggleSerializer(serializers.Serializer):
    """Serializer for toggling reactions"""
    reaction_type = serializers.CharField()
    
    def validate_reaction_type(self, value):
        """Validate reaction type"""
        valid_types = [choice[0] for choice in Reaction.REACTION_CHOICES]
        if value not in valid_types:
            raise serializers.ValidationError(f"Invalid reaction type. Must be one of: {', '.join(valid_types)}")
        return value 