# Posts System

This module handles blog posts with advanced view tracking and analytics.

## Features

- **View Tracking**: Automatic view counting with session and user tracking
- **Read Time Calculation**: Intelligent reading time estimation
- **Analytics**: Detailed analytics for post authors
- **Content Statistics**: Word count, character count, and more
- **Duplicate Prevention**: Prevents duplicate views from same user/session

## Models

### Post Model
The main blog post model with enhanced view tracking and analytics.

**Key Fields:**
- `view_count`: Total number of views
- `reading_time`: Calculated reading time in minutes
- `word_count`: Number of words in content
- `character_count`: Number of characters in content

**Key Methods:**
- `record_view(request)`: Record a view with session tracking
- `get_unique_views_count()`: Get count of unique views
- `get_recent_views(days=7)`: Get views from last N days

### PostView Model
Tracks individual views with detailed information.

**Fields:**
- `post`: Reference to the post
- `user`: User who viewed (if authenticated)
- `session_key`: Session identifier for anonymous users
- `ip_address`: IP address of viewer
- `user_agent`: Browser/device information
- `viewed_at`: Timestamp of view

## API Endpoints

### Get Post Details (with automatic view tracking)
```http
GET /api/posts/{post_id}/
```
Automatically records a view when retrieving published posts.

### Manual View Increment
```http
POST /api/posts/{post_id}/increment_view/
```
Manually increment view count (useful for AJAX calls).

### Post Analytics
```http
GET /api/posts/{post_id}/analytics/
```
Get detailed analytics (author/staff only).

**Response:**
```json
{
  "total_views": 150,
  "unique_views": 120,
  "recent_views_7_days": 25,
  "reading_time": 5,
  "word_count": 1125,
  "character_count": 5625,
  "daily_views": [
    {"day": "2025-01-27", "count": 10},
    {"day": "2025-01-26", "count": 15}
  ]
}
```

## View Tracking Logic

### Automatic View Recording
Views are automatically recorded when:
1. A published post is retrieved via the API
2. The user is not the author of the post
3. The view hasn't been recorded for this user/session

### Duplicate Prevention
The system prevents duplicate views by:
- Using unique constraints on `[post, user]` and `[post, session_key]`
- Only recording one view per user/session per post

### Session Handling
- **Authenticated users**: Tracked by user ID
- **Anonymous users**: Tracked by session key
- **IP tracking**: Additional IP address logging for analytics

## Reading Time Calculation

### Algorithm
1. **HTML Cleaning**: Removes all HTML tags from content
2. **Word Counting**: Splits cleaned text into words
3. **Speed Calculation**: Uses 225 words per minute (industry standard)
4. **Minimum Time**: Returns at least 1 minute

### Example
```python
# Content: "<p>This is a test post.</p> " * 100  # ~600 words
post.reading_time  # Returns: 3 (600 words / 225 wpm)
```

## Content Statistics

### Word Count
- Removes HTML tags before counting
- Splits on whitespace
- Returns total word count

### Character Count
- Removes HTML tags before counting
- Returns total character count (excluding whitespace)

## Usage Examples

### Recording a View
```python
# Automatic (in views.py)
post.record_view(request)

# Manual
post.increment_view_count()
```

### Getting Analytics
```python
# Get unique views count
unique_views = post.get_unique_views_count()

# Get recent views
recent_views = post.get_recent_views(days=7)

# Get reading time
reading_time = post.reading_time
```

### Creating a Post with View Tracking
```python
post = Post.objects.create(
    title="My Blog Post",
    content="<p>This is my content.</p>",
    author=user,
    status='published'
)

# View tracking is automatic when post is retrieved
```

## Admin Interface

### Post Admin
- Displays view count and reading time
- Shows unique views count
- Reading time in minutes format

### PostView Admin
- Lists all individual views
- Filterable by date and post status
- Searchable by post title, username, and IP

## Testing

Run the comprehensive test suite:

```bash
# Test view tracking functionality
python manage.py test posts.tests.PostViewTrackingTestCase

# Test model properties
python manage.py test posts.tests.PostModelTestCase

# Test all post functionality
python manage.py test posts
```

## Performance Considerations

### Database Indexes
- Indexes on `[post, viewed_at]` for analytics queries
- Indexes on `[user, viewed_at]` for user-specific queries
- Indexes on `[session_key, viewed_at]` for session tracking

### Query Optimization
- Uses `select_related` for author and category
- Uses `prefetch_related` for tags
- Efficient view counting with database constraints

### Caching Strategy
- Consider caching view counts for high-traffic posts
- Cache reading time calculations for static content
- Use Redis for real-time analytics if needed

## Configuration

### Settings
Add to your Django settings if needed:

```python
# View tracking settings
POST_VIEW_TRACKING_ENABLED = True
POST_VIEW_SESSION_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds
POST_VIEW_WORDS_PER_MINUTE = 225  # Reading speed
```

## Recent Updates (2025-01-27)

### Added Features
1. **PostView Model**: Detailed view tracking with session and user info
2. **Automatic View Recording**: Views recorded on post retrieval
3. **Enhanced Analytics**: Daily views, unique views, content statistics
4. **Improved Read Time**: Better HTML cleaning and word counting
5. **Duplicate Prevention**: Unique constraints prevent duplicate views

### Backend Changes
- `posts/models.py`: Added PostView model and enhanced Post model
- `posts/views.py`: Added analytics endpoint and automatic view recording
- `posts/serializers.py`: Added new fields for analytics
- `posts/admin.py`: Added PostView admin interface
- `posts/tests.py`: Comprehensive test suite

### API Enhancements
- Automatic view tracking on post retrieval
- New analytics endpoint for detailed statistics
- Enhanced response data with unique views and content stats 