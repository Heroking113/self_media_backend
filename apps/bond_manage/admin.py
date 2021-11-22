from django.contrib import admin

from .models import OwnConvertBond, DayProfitLossConvertBond, SelfChooseManage


@admin.register(SelfChooseManage)
class SelfChooseManageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'bond_abbr', 'bond_code', 'priority', 'create_time')
    list_per_page = 100


@admin.register(OwnConvertBond)
class OwnConvertBondAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'uid',
                    'bond_abbr',
                    'bond_code',
                    'hold_num',
                    'hold_cost',
                    'priority',
                    'create_time')
    list_per_page = 100


@admin.register(DayProfitLossConvertBond)
class DayProfitLossConvertBondAdmin(admin.ModelAdmin):
    list_display = ('id', 'convert_id', 'bond_abbr', 'bond_code', 'quote_change', 'pre_day_fund', 'create_time')
    list_per_page = 100
