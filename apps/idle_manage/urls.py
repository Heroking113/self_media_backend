from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IdleManageViewSet


router = DefaultRouter()
router.register(r'', IdleManageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
