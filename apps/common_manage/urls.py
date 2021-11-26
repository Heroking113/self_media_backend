from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import fetch_spe_config, held_chosen_status

urlpatterns = [
    path('fetch_spe_config/', fetch_spe_config),
    path('held_chosen_status/', held_chosen_status)
]
