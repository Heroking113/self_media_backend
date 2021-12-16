from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ImageFileViewSet


router = DefaultRouter()
router.register(r'img', ImageFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
