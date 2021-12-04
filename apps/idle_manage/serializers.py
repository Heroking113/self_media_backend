from rest_framework import serializers

from .models import IdleManage


class IdleManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = IdleManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(order_status=instance.get_order_status_display())
        data.update(create_time=str(instance.create_time).split('.')[0])
        return data