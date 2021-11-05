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
                  'conversion_preminum_rate']
