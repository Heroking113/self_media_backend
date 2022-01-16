from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ImageFileViewSet, AudioFileViewSet

router = DefaultRouter()
router.register(r'img', ImageFileViewSet)
router.register(r'audio', AudioFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
