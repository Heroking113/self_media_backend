from __future__ import absolute_import

from datetime import datetime

from celery import shared_task
from django.db import transaction
from django.db.models import Q

from apps.base_convert.models import BaseConvert
from apps.bond_manage.models import OwnConvertBond, DayProfitLossConvertBond


@shared_task
def statistic_day_bond_pl():
    own_query = OwnConvertBond.objects.all()
    dic_bond_codes = own_query.values('bond_code')
    bond_codes = list(set([i['bond_code'] for i in dic_bond_codes]))
    base_query = BaseConvert.objects.filter(bond_code__in=bond_codes).values('bond_code', 'cur_bond_price', 'yes_close_price')
    own_query = list(own_query)
    with transaction.atomic():
        for item in own_query:
            for jtm in base_query:
                if item.bond_code == jtm['bond_code']:
                    day_quote_change = (float() - float()) / float()
                    day_pl = item['hold_num'] * day_quote_change
                    update_data = {
                        'day_quote_change': round(day_quote_change, 4),
                        'day_pl': round(day_pl, 2)
                    }
                    DayProfitLossConvertBond.objects.select_for_update().filter(Q(uid=item.uid) & Q(bond_code=item.bond_code)).update(**update_data)
                    break


