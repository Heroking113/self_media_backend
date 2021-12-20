from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TopicManageViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'bs', TopicManageViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
