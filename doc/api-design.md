# API Endpoints and Design Notes ✅ UPDATED

This document tracks all API endpoints, request/response formats, and design decisions for the DRF backend.

## 🔗 Base URL
```
http://localhost:8000/api/
```

## 🔐 Authentication
Currently using Django's session authentication. JWT authentication planned for future.

## 📋 API Endpoints Overview

### 👤 Users API (`/api/users/`)

#### User Registration
```http
POST /api/users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer and blogger",
  "website": "https://johndoe.dev",
  "location": "San Francisco, CA"
}
```

#### Get Current User Profile
```http
GET /api/users/me/
Authorization: Session
```

#### Update Profile
```http
PATCH /api/users/update_profile/
Authorization: Session
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith",
  "bio": "Updated bio",
  "website": "https://newwebsite.com"
}
```

#### Get User List
```http
GET /api/users/
```

#### Get Specific User Profile
```http
GET /api/users/{user_id}/profile/
```

### 📝 Posts API (`/api/posts/`)

#### Get Posts List
```http
GET /api/posts/
Query Parameters:
- status: draft|published|archived
- author: user_id
- category: category_id
- tags: tag_id
- search: search_term
- ordering: created_at|updated_at|published_at|view_count
```

#### Create Post
```http
POST /api/posts/
Authorization: Session
Content-Type: application/json

{
  "title": "My First Blog Post",
  "content": "# Hello World\n\nThis is my first blog post...",
  "excerpt": "A brief summary of the post",
  "category_id": 1,
  "tag_ids": [1, 2, 3],
  "status": "draft",
  "featured_image": null,
  "meta_title": "SEO Title",
  "meta_description": "SEO Description"
}
```

#### Get Post Detail
```http
GET /api/posts/{post_id}/
```

#### Update Post
```http
PUT /api/posts/{post_id}/
Authorization: Session (Author only)
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content...",
  "status": "published"
}
```

#### Publish Draft Post
```http
POST /api/posts/{post_id}/publish/
Authorization: Session (Author only)
```

#### Get User's Posts
```http
GET /api/posts/my_posts/
Authorization: Session
```

#### Get Draft Posts
```http
GET /api/posts/drafts/
Authorization: Session
```

#### Get Featured Posts
```http
GET /api/posts/featured/
```

#### Increment View Count
```http
POST /api/posts/{post_id}/increment_view/
```

### 🏷️ Categories API (`/api/categories/`)

#### Get Categories List
```http
GET /api/categories/
```

#### Get Category Posts
```http
GET /api/categories/{category_slug}/posts/
```

### 🏷️ Tags API (`/api/tags/`)

#### Get Tags List
```http
GET /api/tags/
```

#### Get Tag Posts
```http
GET /api/tags/{tag_slug}/posts/
```

### 💬 Comments API (`/api/comments/`)

#### Get Comments List
```http
GET /api/comments/
Query Parameters:
- post: post_id
- author: user_id
- status: pending|approved|rejected|spam
- parent: parent_comment_id
```

#### Create Comment
```http
POST /api/comments/
Authorization: Session
Content-Type: application/json

{
  "content": "Great post! Thanks for sharing.",
  "post_id": 1,
  "parent_id": null  // For replies
}
```

#### Update Comment
```http
PUT /api/comments/{comment_id}/
Authorization: Session (Author only)
Content-Type: application/json

{
  "content": "Updated comment content"
}
```

#### Like/Unlike Comment
```http
POST /api/comments/{comment_id}/like/
POST /api/comments/{comment_id}/unlike/
Authorization: Session
```

#### Moderate Comment (Admin)
```http
POST /api/comments/{comment_id}/moderate/
Authorization: Session (Admin only)
Content-Type: application/json

{
  "status": "approved"
}
```

#### Get User's Comments
```http
GET /api/comments/my_comments/
Authorization: Session
```

#### Get Pending Comments (Admin)
```http
GET /api/comments/pending/
Authorization: Session (Admin only)
```

### ❤️ Reactions API (`/api/reactions/`)

#### Toggle Reaction
```http
POST /api/reactions/toggle/
Authorization: Session
Content-Type: application/json

{
  "post_id": 1,
  "reaction_type": "like"
}
```

#### Get Post Reactions
```http
GET /api/reactions/post_reactions/?post_id=1
```

#### Get User's Reactions
```http
GET /api/reactions/my_reactions/
Authorization: Session
```

#### Get Popular Reactions
```http
GET /api/reactions/popular_reactions/?post_id=1&limit=5
```

#### Get Reaction Analytics (Admin)
```http
GET /api/reactions/analytics/
Authorization: Session (Admin only)
```

## 📊 Response Formats

### Standard Success Response
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/posts/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

### User Profile Response
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "bio": "Software developer and blogger",
  "avatar": "http://localhost:8000/media/avatars/john.jpg",
  "website": "https://johndoe.dev",
  "location": "San Francisco, CA",
  "date_of_birth": "1990-01-01",
  "is_verified": false,
  "date_joined": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z",
  "post_count": 5
}
```

### Post Response
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "slug": "my-first-blog-post",
  "content": "# Hello World\n\nThis is my first blog post...",
  "excerpt": "A brief summary of the post",
  "author": {
    "id": 1,
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": "http://localhost:8000/media/avatars/john.jpg"
  },
  "category": {
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "Tech-related posts"
  },
  "tags": [
    {
      "id": 1,
      "name": "Django",
      "slug": "django"
    }
  ],
  "featured_image": "http://localhost:8000/media/posts/featured/image.jpg",
  "status": "published",
  "meta_title": "SEO Title",
  "meta_description": "SEO Description",
  "published_at": "2024-01-15T10:00:00Z",
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z",
  "view_count": 150,
  "is_featured": false,
  "reading_time": 5,
  "comment_count": 12,
  "reaction_count": 25
}
```

## 🔍 Filtering and Search

### Available Filters
- **Posts**: `status`, `author`, `category`, `tags`, `is_featured`
- **Comments**: `status`, `author`, `post`, `parent`, `is_edited`
- **Reactions**: `post`, `user`, `reaction_type`

### Search Fields
- **Posts**: `title`, `content`, `excerpt`
- **Comments**: `content`

### Ordering Options
- **Posts**: `created_at`, `updated_at`, `published_at`, `view_count`
- **Comments**: `created_at`, `updated_at`, `likes_count`
- **Reactions**: `created_at`

## 🔒 Permissions

### Public Endpoints
- `GET /api/posts/` (published posts only)
- `GET /api/categories/`
- `GET /api/tags/`
- `GET /api/comments/` (approved comments only)
- `GET /api/reactions/post_reactions/`

### Authenticated Endpoints
- All user profile endpoints
- Post creation and management
- Comment creation and management
- Reaction management

### Admin Only Endpoints
- Comment moderation
- Reaction analytics
- All admin operations

## 📝 API Design Decisions

### RESTful Design
- Use standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Consistent URL patterns
- Proper HTTP status codes

### Serialization Strategy
- Separate serializers for different operations (create, update, list, detail)
- Nested serialization for related objects
- Computed fields for derived data

### Pagination
- Page-based pagination with 20 items per page
- Consistent pagination metadata

### Error Handling
- Comprehensive validation error messages
- Proper HTTP status codes
- Consistent error response format

### Performance Considerations
- Database query optimization with select_related and prefetch_related
- Efficient filtering and search
- Proper indexing on database fields
