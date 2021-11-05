from __future__ import absolute_import
from celery import shared_task

import akshare as ak
from django.db import transaction

from .models import BaseConvert


@shared_task
def update_base_convert():
    with transaction.atomic():
        bond_zh_cov_df = ak.bond_zh_cov()
        BaseConvert.objects.all().delete()
        base_convert_list_to_insert = list()
        for r in bond_zh_cov_df.values:
            base_convert_list_to_insert.append(BaseConvert(
                bond_code=str(r[0]),
                bond_abbr=str(r[1]),
                purchase_date=str(r[2]),
                purchase_code=str(r[3]),
                purchase_limit=str(r[4]),
                underly_code=str(r[5]),
                underly_abbr=str(r[6]),
                underly_price='' if str(r[7]) == 'nan' else str(r[7]),
                conversion_price='' if str(r[8]) == 'nan' else str(r[8]),
                conversion_value='' if str(r[9]) == 'nan' else str(r[9]),
                cur_bond_price='' if str(r[10]) == 'nan' else str(r[10]),
                conversion_preminum_rate='' if str(r[11]) == 'nan' else str(r[11]),
                abos_erd=str(r[12]),
                abos_aps=str(r[13]),
                issurance_scale='' if str(r[14]) == 'nan' else str(r[14]),
                ido_wln=str(r[15]),
                win_rate='' if str(r[16]) == 'nan' else str(r[16]),
                time_market='' if str(r[17]) == 'NaT' else str(r[17])
            ))
        BaseConvert.objects.bulk_create(base_convert_list_to_insert)
