from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentsViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'comments', CommentsViewSet, basename='comment')

urlpatterns = [
    # Include the router's URLs
    path('', include(router.urls)),
]
