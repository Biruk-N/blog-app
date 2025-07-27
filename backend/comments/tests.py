from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Post, Category
from .models import Comment

User = get_user_model()

class CommentAPITestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            author=self.user,
            category=self.category,
            status='published'
        )
        
        # Create test comments
        self.comment1 = Comment.objects.create(
            content='First comment',
            author=self.user,
            post=self.post,
            status='approved'
        )
        
        self.comment2 = Comment.objects.create(
            content='Second comment',
            author=self.user,
            post=self.post,
            status='approved'
        )
        
        # Create replies
        self.reply1 = Comment.objects.create(
            content='Reply to first comment',
            author=self.user,
            post=self.post,
            parent=self.comment1,
            status='approved'
        )
        
        self.reply2 = Comment.objects.create(
            content='Reply to reply',
            author=self.user,
            post=self.post,
            parent=self.reply1,
            status='approved'
        )

    def test_get_comments_for_post_returns_only_top_level(self):
        """Test that the API returns only top-level comments with nested replies"""
        url = f'/api/comments/for_post/?post_id={self.post.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        
        # Should return only 2 top-level comments
        self.assertEqual(len(data), 2)
        
        # Check that comment1 has replies
        comment1_data = next(c for c in data if c['id'] == str(self.comment1.id))
        self.assertEqual(len(comment1_data['replies']), 1)
        
        # Check that reply1 has its own replies
        reply1_data = comment1_data['replies'][0]
        self.assertEqual(len(reply1_data['replies']), 1)
        
        # Check that comment2 has no replies
        comment2_data = next(c for c in data if c['id'] == str(self.comment2.id))
        self.assertEqual(len(comment2_data['replies']), 0)

    def test_get_comments_with_post_filter_returns_only_top_level(self):
        """Test that the regular comments endpoint with post filter returns only top-level comments"""
        url = f'/api/comments/?post={self.post.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        
        # Should return only 2 top-level comments
        self.assertEqual(len(data), 2)
        
        # Check that comment1 has replies
        comment1_data = next(c for c in data if c['id'] == str(self.comment1.id))
        self.assertEqual(len(comment1_data['replies']), 1)
        
        # Check that comment2 has no replies
        comment2_data = next(c for c in data if c['id'] == str(self.comment2.id))
        self.assertEqual(len(comment2_data['replies']), 0)
