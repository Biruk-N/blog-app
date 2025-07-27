# Comments System

This module handles the nested comments system for blog posts.

## Features

- **Nested Comments**: Support for unlimited levels of comment replies
- **Moderation**: Comments can be pending, approved, rejected, or marked as spam
- **User Permissions**: Users can only edit their own comments
- **Admin Moderation**: Staff can moderate all comments
- **Performance Optimized**: Uses select_related and prefetch_related for efficient queries

## API Endpoints

### Get Comments for a Post
```http
GET /api/comments/for_post/?post_id={post_id}
```
Returns only top-level comments with their nested replies in a hierarchical structure.

### Get Comments (with filters)
```http
GET /api/comments/?post={post_id}
```
Returns top-level comments filtered by post, with nested replies.

### Create Comment
```http
POST /api/comments/
Content-Type: application/json

{
  "content": "Comment text",
  "post_id": "post-uuid",
  "parent_id": "parent-comment-uuid"  // Optional, for replies
}
```

### Get Replies for a Comment
```http
GET /api/comments/{comment_id}/replies/
```
Returns all replies for a specific comment.

## Data Structure

Comments are returned in a hierarchical structure:

```json
[
  {
    "id": "comment-uuid",
    "content": "Top-level comment",
    "author": { ... },
    "replies": [
      {
        "id": "reply-uuid",
        "content": "Reply to comment",
        "author": { ... },
        "replies": [
          {
            "id": "nested-reply-uuid",
            "content": "Reply to reply",
            "author": { ... },
            "replies": []
          }
        ]
      }
    ]
  }
]
```

## Recent Changes (2025-01-27)

### Problem
The API was returning a flat list of all comments (including replies) in the `results` array, causing confusion in the frontend where replies were displayed as top-level comments.

### Solution
1. **Modified `get_queryset()` in `CommentViewSet`**: Now returns only top-level comments (where `parent` is `null`)
2. **Updated Serializers**: Modified `CommentListSerializer`, `CommentDetailSerializer`, and `CommentReplySerializer` to properly handle nested replies
3. **Added New Endpoint**: Created `/api/comments/for_post/` for clearer API usage
4. **Enhanced Prefetching**: Added proper prefetch_related for better performance

### Backend Changes
- `comments/views.py`: Updated queryset filtering and added new actions
- `comments/serializers.py`: Modified serializers to handle nested structure properly
- `comments/tests.py`: Added comprehensive tests

### Frontend Changes
- Updated `BlogDetail.tsx` to use the new `/api/comments/for_post/` endpoint
- The existing `CommentItem.tsx` component already handled nested replies correctly

## Testing

Run the tests to verify the functionality:

```bash
python manage.py test comments.tests.CommentAPITestCase -v 2
```

## Usage Examples

### Creating a Top-Level Comment
```python
comment = Comment.objects.create(
    content="Great post!",
    author=user,
    post=post,
    status='approved'
)
```

### Creating a Reply
```python
reply = Comment.objects.create(
    content="I agree!",
    author=user,
    post=post,
    parent=comment,  # This makes it a reply
    status='approved'
)
```

### Getting Comments for a Post
```python
# Get only top-level comments with nested replies
top_level_comments = Comment.objects.filter(
    post=post,
    parent__isnull=True
).prefetch_related('replies__author')
``` 