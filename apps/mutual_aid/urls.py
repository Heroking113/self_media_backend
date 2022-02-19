from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MutualManageViewSet


router = DefaultRouter()
router.register(r'', MutualManageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
