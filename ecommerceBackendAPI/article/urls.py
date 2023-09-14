from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, SendNotificationView

# Create a router and register the ArticleModelViewSet
router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-notification/<int:id>/',
         SendNotificationView.as_view(), name='send-notification'),
]
