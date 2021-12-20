from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserManageViewSet, AssetManageViewSet, SchUserManageViewSet


router = DefaultRouter()
router.register(r'bs', UserManageViewSet)
router.register(r'am', AssetManageViewSet)
router.register(r'sch', SchUserManageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
