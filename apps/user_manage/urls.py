from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserManageViewSet


router = DefaultRouter()
router.register(r'bs', UserManageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
