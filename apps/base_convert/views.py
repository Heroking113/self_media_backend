import pandas as pd

from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import akshare as ak
from sqlalchemy import create_engine

from utils.common import update_base_convert_data
from utils.wx_util import get_openid_session_key_by_code
from .models import BaseConvert
from .serializers import BaseConvertSerializer


class BaseConvertViewSet(viewsets.ModelViewSet):
    queryset = BaseConvert.objects.all()
    serializer_class = BaseConvertSerializer

    @action(methods=['GET'], detail=False)
    def test(self, request):
        update_base_convert_data()
        return Response()
