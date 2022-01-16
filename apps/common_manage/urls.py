from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (fetch_spe_config,
                    held_chosen_status,
                    asset_info,
                    fetch_spe_sch_config,
                    SchSwiperViewSet,
                    sentence_recognition)

urlpatterns = [
    path('fetch_spe_config/', fetch_spe_config),
    path('held_chosen_status/', held_chosen_status),
    path('asset_info/', asset_info),
    path('fetch_spe_sch_config/', fetch_spe_sch_config),
    path('sentence_recognition/', sentence_recognition)
]

router = DefaultRouter()
router.register(r'', SchSwiperViewSet)
urlpatterns += [
    path('sch-swiper/', include(router.urls)),
]