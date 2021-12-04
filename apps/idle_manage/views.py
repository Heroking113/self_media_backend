from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import IdleManage
from .serializers import IdleManageSerializer


class IdleManageViewSet(viewsets.ModelViewSet):
    queryset = IdleManage.objects.all()
    serializer_class = IdleManageSerializer
    pagination_class = None
