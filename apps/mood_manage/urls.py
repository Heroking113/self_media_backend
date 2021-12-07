from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MoodManageViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'bs', MoodManageViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
