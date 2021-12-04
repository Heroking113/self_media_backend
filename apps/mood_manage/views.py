from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MoodManage
from .serializers import MoodManageSerializer


class MoodManageViewSet(viewsets.ModelViewSet):
    queryset = MoodManage.objects.all()
    serializer_class = MoodManageSerializer
    pagination_class = None
