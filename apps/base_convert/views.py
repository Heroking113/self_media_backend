import json

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.redis_cli import redisCli
from .models import BaseConvert
from .serializers import BaseConvertSerializer


class BaseConvertViewSet(viewsets.ModelViewSet):
    queryset = BaseConvert.objects.all().order_by('-id')
    serializer_class = BaseConvertSerializer

    @action(methods=['GET'], detail=False)
    def test(self, request):

        # dic = {'a': 1}
        # redisCli.set('dic', dic)
        # li_dic = [{'a': 1}, {'b': 2, 'c': 3}]
        # redisCli.set('li_dic', li_dic)
        # ret = redisCli.get('li_dic')
        return Response()

    @action(methods=['GET'], detail=False)
    def cus_inquire(self, request):
        s_val = request.query_params.get('s_val')
        s_query = BaseConvert.objects.filter(Q(bond_code__contains=s_val) | Q(bond_abbr__contains=s_val) | Q(underly_abbr__contains=s_val))
        page = self.paginate_queryset(s_query)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=False)
    def double_low_data(self, request):
        page = int(request.query_params.get('page', 1))
        dl_pages = redisCli.get('dl_pages')
        if page > 3:
            return Response({
                'next': '',
                'results': []
            })
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

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        ret_data = BaseConvert.get_double_low_data(serializer.data)
        return Response(ret_data)


