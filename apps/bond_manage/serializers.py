from rest_framework import serializers

from .models import SelfChooseManage, OwnConvertBond, DayProfitLossConvertBond


class SelfChooseManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelfChooseManage
        fields = ('id', 'uid', 'bond_abbr', 'bond_code', 'priority', 'create_time')


class OwnConvertBondSerializer(serializers.ModelSerializer):

    class Meta:
        model = OwnConvertBond
        fields = '__all__'

    def to_representation(self, instance):
        """
        """
        data = super().to_representation(instance)
        data.update(create_time=str(instance.create_time).split('.')[0])
        return data


class DayProfitLossConvertBondSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayProfitLossConvertBond
        fields = '__all__'
