from django.contrib import admin

from .models import BaseConvert


@admin.register(BaseConvert)
class BaseConvertAdmin(admin.ModelAdmin):
    list_display = ('id','bond_code','bond_abbr','purchase_date','purchase_code','purchase_limit','underly_code','underly_abbr','underly_price','conversion_price','conversion_value','cur_bond_price', 'yes_close_price', 'conversion_preminum_rate','abos_erd','abos_aps','issurance_scale','ido_wln','win_rate','time_market','lasted_time')
    list_per_page = 100
