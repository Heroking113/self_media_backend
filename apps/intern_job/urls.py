from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import JobManageViewSet


router = DefaultRouter()
router.register(r'', JobManageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
