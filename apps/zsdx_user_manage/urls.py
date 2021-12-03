from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import index


router = DefaultRouter()
# router.register(r'am', AssetManageViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('', index)
]
