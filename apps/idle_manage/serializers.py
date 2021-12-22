from rest_framework import serializers
from django.conf import settings

from utils.common import format_datetime
from .models import IdleManage

MEDIA_PATH = settings.DOMAIN + '/media/'


class IdleManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = IdleManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(order_status=instance.get_order_status_display())

        create_time = format_datetime(instance.create_time)
        data.update(create_time=create_time)

        img_paths = instance.img_paths.split(',')
        img_paths = [MEDIA_PATH+item for item in img_paths]
        data.update(img_paths=img_paths)
        return data