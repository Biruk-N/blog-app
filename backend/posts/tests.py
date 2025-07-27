from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from .models import Post, Category, Tag, PostView

User = get_user_model()

class PostViewTrackingTestCase(APITestCase):
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
            content='This is a test post with some content. ' * 50,  # ~300 words
            author=self.user,
            category=self.category,
            status='published',
            published_at=timezone.now()
        )
        
        self.factory = RequestFactory()

    def test_reading_time_calculation(self):
        """Test reading time calculation"""
        # Test with HTML content
        html_content = '<p>This is a test post with some content.</p> ' * 50
        self.post.content = html_content
        self.post.save()
        
        # Should calculate reading time based on text content, not HTML
        self.assertGreater(self.post.reading_time, 0)
        self.assertLess(self.post.reading_time, 10)  # Should be reasonable
        
        # Test word count
        self.assertGreater(self.post.word_count, 0)
        
        # Test character count
        self.assertGreater(self.post.character_count, 0)

    def test_view_counting(self):
        """Test view counting functionality"""
        initial_count = self.post.view_count
        
        # Create a mock request
        request = self.factory.get('/')
        request.user = self.user
        request.session = type('Session', (), {'session_key': 'test_session'})()
        request.META = {'REMOTE_ADDR': '127.0.0.1', 'HTTP_USER_AGENT': 'Test Browser'}
        
        # Record a view
        self.post.record_view(request)
        
        # Check that view count increased
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, initial_count + 1)
        
        # Check that PostView was created
        self.assertTrue(PostView.objects.filter(post=self.post).exists())
        
        # Check unique views count
        self.assertEqual(self.post.get_unique_views_count(), 1)

    def test_duplicate_view_prevention(self):
        """Test that duplicate views from same user/session are prevented"""
        request = self.factory.get('/')
        request.user = self.user
        request.session = type('Session', (), {'session_key': 'test_session'})()
        request.META = {'REMOTE_ADDR': '127.0.0.1', 'HTTP_USER_AGENT': 'Test Browser'}
        
        # Record first view
        self.post.record_view(request)
        initial_count = self.post.view_count
        
        # Try to record another view from same user
        self.post.record_view(request)
        
        # View count should not increase due to unique constraint
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, initial_count)

    def test_automatic_view_recording_on_retrieve(self):
        """Test that views are automatically recorded when retrieving published posts"""
        url = f'/api/posts/{self.post.id}/'
        
        # Make a GET request to retrieve the post
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that view count increased
        self.post.refresh_from_db()
        self.assertGreater(self.post.view_count, 0)

    def test_analytics_endpoint(self):
        """Test the analytics endpoint"""
        # Create some views first
        request = self.factory.get('/')
        request.user = self.user
        request.session = type('Session', (), {'session_key': 'test_session'})()
        request.META = {'REMOTE_ADDR': '127.0.0.1', 'HTTP_USER_AGENT': 'Test Browser'}
        
        self.post.record_view(request)
        
        # Test analytics endpoint
        url = f'/api/posts/{self.post.id}/analytics/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        
        # Check that analytics data is returned
        self.assertIn('total_views', data)
        self.assertIn('unique_views', data)
        self.assertIn('reading_time', data)
        self.assertIn('word_count', data)
        self.assertIn('character_count', data)
        self.assertIn('daily_views', data)

    def test_analytics_permissions(self):
        """Test that only post author or staff can access analytics"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        url = f'/api/posts/{self.post.id}/analytics/'
        
        # Test with unauthorized user
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with post author
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post with some content.',
            author=self.user,
            category=self.category,
            status='draft'
        )

    def test_reading_time_property(self):
        """Test reading time property calculation"""
        # Test with short content
        self.post.content = 'Short content'
        self.post.save()
        self.assertEqual(self.post.reading_time, 1)  # Minimum 1 minute
        
        # Test with longer content
        long_content = 'This is a longer test post. ' * 100  # ~600 words
        self.post.content = long_content
        self.post.save()
        
        # Should be around 3 minutes (600 words / 225 wpm)
        self.assertGreaterEqual(self.post.reading_time, 2)
        self.assertLessEqual(self.post.reading_time, 4)

    def test_word_count_property(self):
        """Test word count property"""
        self.post.content = 'This is a test post with five words.'
        self.post.save()
        self.assertEqual(self.post.word_count, 7)

    def test_character_count_property(self):
        """Test character count property"""
        test_content = 'Test content'
        self.post.content = test_content
        self.post.save()
        self.assertEqual(self.post.character_count, len(test_content))

    def test_is_published_property(self):
        """Test is_published property"""
        # Draft post should not be published
        self.assertFalse(self.post.is_published)
        
        # Published post should be published
        self.post.status = 'published'
        self.post.published_at = timezone.now()
        self.post.save()
        self.assertTrue(self.post.is_published)
