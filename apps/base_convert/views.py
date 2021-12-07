import json

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.common import update_base_convert_data
from utils.redis_cli import redisCli
from .models import BaseConvert
from .serializers import BaseConvertSerializer
from .tasks import rm_7days_before, update_base_convert_close_price


class BaseConvertViewSet(viewsets.ModelViewSet):
    queryset = BaseConvert.objects.all()
    serializer_class = BaseConvertSerializer

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        ret_data = BaseConvert.format_ret_data(uid, serializer.data)
        return self.get_paginated_response(ret_data)

    @action(methods=['GET'], detail=False)
    def update_base_convert_save_file(self, request):
        update_base_convert_close_price()
        return Response({
            'api url': '/bc/update_base_convert_save_file/',
            'status': 'success'
        })

    @action(methods=['GET'], detail=False)
    def cus_inquire(self, request):
        uid = request.query_params.get('uid', '')
        s_val = request.query_params.get('s_val', '')
        s_query = BaseConvert.objects.filter(Q(bond_code__contains=s_val) | Q(bond_abbr__contains=s_val) | Q(underly_abbr__contains=s_val))
        page = self.paginate_queryset(s_query)
        serializer = self.get_serializer(page, many=True)
        ret_data = BaseConvert.format_ret_data(uid, serializer.data)
        return self.get_paginated_response(ret_data)

    @action(methods=['GET'], detail=False)
    def double_low_data(self, request):
        page = int(request.query_params.get('page', 1))
        dl_pages = redisCli.get('dl_pages')

        if dl_pages:
            if page > dl_pages:
                return Response({
                    'next': '',
                    'results': []
                })
            ret_data = redisCli.get('dl_data')[page-1]
            next_page = '' if page == dl_pages else '/bc/double_low_data/?page=' + str(page+1)
            return Response({
                'next': next_page,
                'results': ret_data
            })

        ret_data = BaseConvert.get_save_double_low_data()
        return Response(ret_data)


