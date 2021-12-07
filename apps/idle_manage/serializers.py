from rest_framework import serializers
from django.conf import settings

from .models import IdleManage

MEDIA_PATH = settings.DOMAIN + '/media/'


class IdleManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = IdleManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(order_status=instance.get_order_status_display())

        create_time = str(instance.create_time).split('.')[0]
        y_m_d, h_m_s = create_time.split(' ')
        _, m, d = y_m_d.split('-')
        m_d = '-'.join([m, d])
        h, mm, _ = h_m_s.split(':')
        h_m = ':'.join([h, mm])
        create_time = ' '.join([m_d, h_m])
        # data.update(create_time=str(instance.create_time).split(' ')[0])
        data.update(create_time=create_time)

        img_paths = instance.img_paths.split(',')
        img_paths = [MEDIA_PATH+item for item in img_paths]
        data.update(img_paths=img_paths)
        return data