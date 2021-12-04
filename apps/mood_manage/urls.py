from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MoodManageViewSet


router = DefaultRouter()
router.register(r'', MoodManageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
