from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import fetch_spe_config, held_chosen_status, asset_info, test, SchSwiperViewSet

urlpatterns = [
    path('fetch_spe_config/', fetch_spe_config),
    path('held_chosen_status/', held_chosen_status),
    path('asset_info/', asset_info),
    path('test/', test)
]

router = DefaultRouter()
router.register(r'', SchSwiperViewSet)
urlpatterns += [
    path('sch-swiper/', include(router.urls)),
]