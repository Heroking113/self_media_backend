import logging
import re

from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.common import send_email
from utils.redis_cli import redisCli
from .models import Configuration
from apps.bond_manage.models import SelfChooseManage, OwnConvertBond
from .tasks import fetch_access_token
from ..base_convert.models import BaseConvert
from ..base_convert.serializers import BaseConvertSerializer

logger = logging.getLogger('cb_backend')


@api_view(['GET'])
def test(request):
    # access_token = fetch_access_token()
    # send_email('title', 'content')
    # logger.error('heroking')

    return Response()


@api_view(['POST'])
def fetch_spe_config(request):
    keys = request.data.get('keys', [])
    query = Configuration.objects.filter(key__in=keys).values('key',
                                                              'uni_val',
                                                              'opt_val_one')
    return Response(query)


@api_view(['GET'])
def held_chosen_status(request):
    uid = request.query_params.get('uid', '')
    bond_code = request.query_params.get('bond_code', '')

    held_query = OwnConvertBond.objects.filter(Q(uid=uid) & Q(bond_code=bond_code))
    chosen_query = SelfChooseManage.objects.filter(Q(uid=uid) & Q(bond_code=bond_code))

    ret_data = {
        'held_status': '已持有' if held_query else '未持有',
        'chosen_status': '已自选' if chosen_query else '未自选'
    }

    return Response(ret_data)


@api_view(['GET'])
def asset_info(request):
    """
    当日收益 = sum（每只可转债持有数量*（现价 - 昨日收盘价）/ 昨日收盘价）
    总资产 = sum（每只可转债持有的数量*现价）
    总收益 = 总资产 - 总的持有成本
    """
    day_income = 0
    account_asset = 0
    total_cost = 0

    uid = request.query_params.get('uid', '')
    own_query = list(OwnConvertBond.objects.filter(uid=uid))
    bond_codes = [item.bond_code for item in own_query]
    base_convert = BaseConvert.get_base_convert_in_codes(bond_codes)
    if not base_convert:
        base_query = BaseConvert.objects.all()
        base_serializer = BaseConvertSerializer(base_query, many=True)
        base_convert = [dict(i) for i in base_serializer.data if i['bond_code'] in bond_codes]

    for item in base_convert:
        for oitem in own_query:
            if item['bond_code'] == oitem.bond_code:
                hold_num = oitem.hold_num
                try:
                    cur_bond_price = float(item['cur_bond_price']) if not re.findall('[a-zA-Z]', item['cur_bond_price']) else 0
                except ValueError:
                    cur_bond_price = 0

                try:
                    yes_close_price = float(item['yes_close_price']) if not re.findall('[a-zA-Z]', item['yes_close_price']) else 0
                except ValueError:
                    yes_close_price = 0

                day_income += 0 if yes_close_price == 0 else hold_num * (cur_bond_price - yes_close_price) / yes_close_price
                account_asset += hold_num * cur_bond_price
                total_cost += oitem.hold_cost
                break

    res_data = {
        'day_income': round(day_income, 2),
        'account_asset': round(account_asset, 2),
        'total_income': round(account_asset - total_cost, 2)
    }
    return Response(res_data)