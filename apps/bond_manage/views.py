from datetime import datetime, timedelta
from random import randint, uniform

from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.exceptions import HTTP_499_DATA_EXIST
from .models import OwnConvertBond, DayProfitLossConvertBond, SelfChooseManage

from .serializers import OwnConvertBondSerializer, DayProfitLossConvertBondSerializer, SelfChooseManageSerializer
from ..base_convert.models import BaseConvert
from ..base_convert.serializers import BaseConvertSerializer


class SelfChooseManageViewSet(viewsets.ModelViewSet):
    queryset = SelfChooseManage.objects.all()
    serializer_class = SelfChooseManageSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        dic_bond_codes = list(SelfChooseManage.objects.filter(uid=uid).values('bond_code'))
        bond_codes = [item['bond_code'] for item in dic_bond_codes]
        base_bd_query = BaseConvert.objects.filter(bond_code__in=bond_codes)
        serializer = BaseConvertSerializer(base_bd_query, many=True)
        return Response(serializer.data)


class OwnConvertBondViewSet(viewsets.ModelViewSet):
    queryset = OwnConvertBond.objects.all()
    serializer_class = OwnConvertBondSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        data = request.data
        uid = data.get('uid', '')
        bond_code = data.get('bond_code', '')
        query = OwnConvertBond.objects.filter(Q(bond_code=bond_code) & Q(uid=uid))
        if query:
            raise HTTP_499_DATA_EXIST('该条数据已存在')
        return super(OwnConvertBondViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        query = OwnConvertBond.objects.filter(uid=uid)
        serializer = self.get_serializer(query, many=True)
        ret_data = OwnConvertBond.handle_serializer_data(serializer.data)
        return Response(ret_data)

    @action(methods=['GET'], detail=False)
    def bulk_create(self, request):
        """批量创建测试数据"""
        uid = request.query_params.get('uid', '')
        li = [{"id": 1, "bond_abbr": "麒麟转债", "bond_code": "127050"},
              {"id": 2, "bond_abbr": "苏租转债", "bond_code": "110083"},
              {"id": 3, "bond_abbr": "设研转债", "bond_code": "123130"},
              {"id": 4, "bond_abbr": "希望转2", "bond_code": "127049"},
              {"id": 5, "bond_abbr": "天合转债", "bond_code": "118002"},
              {"id": 7, "bond_abbr": "宏发转债", "bond_code": "110082"},
              {"id": 8, "bond_abbr": "中大转债", "bond_code": "127048"},
              {"id": 9, "bond_abbr": "皖天转债", "bond_code": "113631"},
              {"id": 10, "bond_abbr": "锦鸡转债", "bond_code": "123129"},
              {"id": 11, "bond_abbr": "山玻转债", "bond_code": "111001"},
              {"id": 17, "bond_abbr": "耐普转债", "bond_code": "123127"}]
        create_data = []
        for i in range(10):
            for item in li:
                create_data.append(DayProfitLossConvertBond(
                    uid=uid,
                    convert_id=item['id'],
                    bond_abbr=item['bond_abbr'],
                    bond_code=item['bond_code'],
                    quote_change=round(uniform(-0.5, 0.5), 2),
                    pre_day_fund=randint(100, 5000),
                    create_time=datetime.today() + timedelta(-(i+1))
                ))

        with transaction.atomic():
            DayProfitLossConvertBond.objects.bulk_create(create_data)
            # raise Exception('error test')
        return Response()


class DayProfitLossConvertBondViewSet(viewsets.ModelViewSet):
    queryset = DayProfitLossConvertBond.objects.all()
    serializer_class = DayProfitLossConvertBondSerializer
    pagination_class = None


    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        ownConvertIds = OwnConvertBond.objects.filter(uid=uid).values('id')
        before_days = int(request.query_params.get('before_days', 0))
        if not before_days:
            queryset = DayProfitLossConvertBond.objects.filter(uid=uid).order_by('-id')
        else:
            before_date = datetime.today() + timedelta(-(before_days+1))
            queryset = DayProfitLossConvertBond.objects.filter(Q(uid=uid) & Q(create_time__gte=before_date)).order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        data = DayProfitLossConvertBond.format_res_data(ownConvertIds, serializer.data)
        return Response(data)

