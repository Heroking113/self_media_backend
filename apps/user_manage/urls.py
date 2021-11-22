from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserManageViewSet, AssetManageViewSet


router = DefaultRouter()
router.register(r'bs', UserManageViewSet)
router.register(r'am', AssetManageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
