from rest_framework import serializers

from .models import BaseConvert


class BaseConvertSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseConvert
        fields = ['bond_code',
                  'bond_abbr',
                  'underly_abbr',
                  'underly_price',
                  'conversion_price',
                  'conversion_value',
                  'cur_bond_price',
                  'yes_close_price',
                  'conversion_preminum_rate']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 转股价值、转股溢价率
        if instance.conversion_value:
            data.update(conversion_value=round(float(instance.conversion_value), 3))
        if instance.conversion_preminum_rate:
            data.update(conversion_preminum_rate=round(float(instance.conversion_preminum_rate), 3))
        return data
