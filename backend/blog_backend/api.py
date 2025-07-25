from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from posts.views import PostViewSet, CategoryViewSet, TagViewSet
from comments.views import CommentViewSet
from reactions.views import ReactionViewSet

# Create the main API router
api_router = DefaultRouter()

# Register all ViewSets
api_router.register(r'users', UserViewSet, basename='user')
api_router.register(r'posts', PostViewSet, basename='post')
api_router.register(r'categories', CategoryViewSet, basename='category')
api_router.register(r'tags', TagViewSet, basename='tag')
api_router.register(r'comments', CommentViewSet, basename='comment')
api_router.register(r'reactions', ReactionViewSet, basename='reaction')

# Export the URL patterns
urlpatterns = api_router.urls 