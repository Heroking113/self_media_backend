from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OwnConvertBondViewSet, DayProfitLossConvertBondViewSet, SelfChooseManageViewSet


router = DefaultRouter()
router.register(r'ocb', OwnConvertBondViewSet)
router.register(r'dpl', DayProfitLossConvertBondViewSet)
router.register(r'scm', SelfChooseManageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
