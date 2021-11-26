from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Configuration
from apps.bond_manage.models import SelfChooseManage, OwnConvertBond


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