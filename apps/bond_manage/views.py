from datetime import datetime, timedelta
from random import randint, uniform

from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.exceptions import HTTP_499_DATA_EXIST
from utils.format_ret_data import format_bond_manage_ocb_list_ret_data
from .models import OwnConvertBond, DayProfitLossConvertBond, SelfChooseManage

from .serializers import OwnConvertBondSerializer, DayProfitLossConvertBondSerializer, SelfChooseManageSerializer
from .tasks import statistic_day_bond_pl
from ..base_convert.models import BaseConvert
from ..base_convert.serializers import BaseConvertSerializer
from ..user_manage.models import AssetManage


class SelfChooseManageViewSet(viewsets.ModelViewSet):
    queryset = SelfChooseManage.objects.all()
    serializer_class = SelfChooseManageSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        dic_bond_codes = list(SelfChooseManage.objects.filter(uid=uid).values('bond_code', 'priority'))
        bond_codes = [item['bond_code'] for item in dic_bond_codes]
        base_bd_query = BaseConvert.objects.filter(bond_code__in=bond_codes)
        serializer = BaseConvertSerializer(base_bd_query, many=True)

        if not dic_bond_codes[0]['priority']:
            return Response(serializer.data)

        ret_data = []
        for item in serializer.data:
            item = dict(item)
            for i_ in dic_bond_codes:
                if item['bond_code'] == i_['bond_code']:
                    item['priority'] = i_['priority']
                    ret_data.append(item)
                    break

        ret_data = sorted(ret_data, key=lambda e: e.__getitem__('priority'))
        ret_data.reverse()
        return Response(ret_data)

    @action(methods=['GET'], detail=False)
    def indv_data(self, request):
        uid = request.query_params.get('uid', '')
        query = SelfChooseManage.objects.filter(uid=uid).values('bond_abbr', 'bond_code', 'priority')
        if not query:
            return Response([])
        if query[0]['priority']:
            query = sorted(query, key=lambda e: e.__getitem__('priority'))
            query.reverse()
        return Response(query)

    @action(methods=['POST'], detail=False)
    def update_sort(self, request):
        uid = request.data.get('uid', '')
        code_priority = request.data.get('code_priority', [])
        with transaction.atomic():
            for item in code_priority:
                ret = SelfChooseManage.objects.select_for_update().get(Q(uid=uid) & Q(bond_code=item['code']))
                ret.priority = item['priority']
                ret.save()
        return Response()

    @action(methods=['POST'], detail=False)
    def bulk_del(self, request):
        uid = request.data.get('uid', '')
        bond_codes = request.data.get('bond_codes', [])
        with transaction.atomic():
            SelfChooseManage.objects.select_for_update().filter(Q(uid=uid) & Q(bond_code__in=bond_codes)).delete()
        return Response()


class OwnConvertBondViewSet(viewsets.ModelViewSet):
    queryset = OwnConvertBond.objects.all()
    serializer_class = OwnConvertBondSerializer
    pagination_class = None

    # @action(methods=['GET'], detail=False)
    # def test(self,request):
    #     # statistic_day_bond_pl()
    #     return Response({'api url: /bm/ocb/test/'})

    def create(self, request, *args, **kwargs):
        """
        创建数据：
            如果当天已经有总资产数据，则更新总资产数据
        """
        data = request.data
        uid = data.get('uid', '')
        bond_code = data.get('bond_code', '')
        query = OwnConvertBond.objects.filter(Q(bond_code=bond_code) & Q(uid=uid))
        if query:
            raise HTTP_499_DATA_EXIST('该条数据已存在')

        serializer = self.get_serializer(data=data)
        with transaction.atomic():
            # 创建新数据
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # 更新总资产数据
            cur_bond_price = BaseConvert.objects.get(bond_code=bond_code).cur_bond_price
            hold_num = int(data.get('hold_num', 0))

            asset_query = AssetManage.objects.select_for_update().filter(
                Q(uid=uid) & Q(create_time__gte=datetime.now().date())
            )
            if asset_query:
                day_asset = float(asset_query[0].day_asset) + float(cur_bond_price) * hold_num
                asset_query.update(day_asset=day_asset)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        query = OwnConvertBond.objects.filter(uid=uid).order_by('-priority')
        serializer = self.get_serializer(query, many=True)
        ret_data = format_bond_manage_ocb_list_ret_data(serializer.data)
        return Response(ret_data)

    @action(methods=['GET'], detail=False)
    def indv_data(self, request):
        uid = request.query_params.get('uid', '')
        query = OwnConvertBond.objects.filter(uid=uid).values('bond_abbr', 'bond_code', 'priority')
        if not query:
            return Response([])
        if query[0]['priority']:
            query = sorted(query, key = lambda e:e.__getitem__('priority'))
            query.reverse()
        return Response(query)

    @action(methods=['GET'], detail=False)
    def bulk_create(self, request):
        """批量创建测试数据"""
        uid = request.query_params.get('uid', '')
        hold_bonds = OwnConvertBond.objects.filter(uid=uid).values('bond_code', 'bond_abbr')

        create_data = []
        for item in hold_bonds:
            for i in range(100):
                create_data.append(DayProfitLossConvertBond(
                    uid=uid,
                    bond_code=item['bond_code'],
                    bond_abbr=item['bond_abbr'],
                    day_quote_change=round(uniform(-0.5, 0.5), 2),
                    day_pl=randint(100, 5000),
                    create_time=datetime.today() + timedelta(-(i + 1))
                ))
        DayProfitLossConvertBond.objects.bulk_create(create_data)
        return Response()

    @action(methods=['POST'], detail=False)
    def update_sort(self, request):
        uid = request.data.get('uid', '')
        code_priority = request.data.get('code_priority', [])
        with transaction.atomic():
            for item in code_priority:
                ret = OwnConvertBond.objects.select_for_update().get(Q(uid=uid) & Q(bond_code=item['code']))
                ret.priority = item['priority']
                ret.save()
        return Response()

    @action(methods=['POST'], detail=False)
    def bulk_del(self, request):
        """
        批量删除可转债：
            当天如果有总资产数据，则更新；
            删除相关的可转债日盈亏数据；
            删除该批可转债数据。
        """
        uid = request.data.get('uid', '')
        bond_codes = request.data.get('bond_codes', [])
        with transaction.atomic():
            # 更新当日总资产
            base_convert = BaseConvert.objects.filter(bond_code__in=bond_codes).values('bond_code', 'cur_bond_price')
            own_convert = list(OwnConvertBond.objects.select_for_update().filter(Q(uid=uid) & Q(bond_code__in=bond_codes)))
            reduced_asset = 0
            for bc in base_convert:
                for oc in own_convert:
                    if bc['bond_code'] == oc.bond_code:
                        asset = 0 if not bc['cur_bond_price'] else float(bc['cur_bond_price']) * oc.hold_num
                        reduced_asset += asset
                        break
            query = AssetManage.objects.select_for_update().filter(Q(uid=uid) & Q(create_time__gte=datetime.now().date()))
            if query:
                day_asset = float(query[0].day_asset) - reduced_asset
                day_asset = day_asset if day_asset >=0 else 0
                query.update(day_asset=day_asset)

            # 删除可转债的日盈亏数据
            DayProfitLossConvertBond.objects.select_for_update().filter(Q(uid=uid) & Q(bond_code__in=bond_codes)).delete()

            # 删除可转债
            OwnConvertBond.objects.select_for_update().filter(Q(uid=uid) & Q(bond_code__in=bond_codes)).delete()
        return Response()


class DayProfitLossConvertBondViewSet(viewsets.ModelViewSet):
    queryset = DayProfitLossConvertBond.objects.all()
    serializer_class = DayProfitLossConvertBondSerializer
    pagination_class = None


    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        before_days = int(request.query_params.get('before_days', 0))
        if not before_days:
            queryset = DayProfitLossConvertBond.objects.filter(uid=uid).order_by('-id')
        else:
            before_date = datetime.today() + timedelta(-(before_days+1))
            queryset = DayProfitLossConvertBond.objects.filter(Q(uid=uid) & Q(create_time__gte=before_date)).order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
