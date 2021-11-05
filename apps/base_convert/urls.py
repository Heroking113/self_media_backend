from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BaseConvertViewSet


router = DefaultRouter()
router.register(r'', BaseConvertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
