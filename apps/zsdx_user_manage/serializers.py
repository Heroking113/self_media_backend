from rest_framework import serializers

from .models import ZsdxUserManage


class ZsdxUserManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ZsdxUserManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(gender=instance.get_gender_display())
        data.update(create_time=str(instance.create_time).split('.')[0])
        data.update(lasted_time=str(instance.lasted_time).split('.')[0])
        return data