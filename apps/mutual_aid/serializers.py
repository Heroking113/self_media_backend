import base64

from rest_framework import serializers
from django.conf import settings

from utils.common import format_datetime
from .models import MutualManage

MEDIA_PATH = settings.DOMAIN + '/media/'


class MutualManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MutualManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)

        create_time = format_datetime(instance.create_time)
        data.update(create_time=create_time)
        data.update(nickname=base64.b64decode(instance.nickname).decode('utf-8'))
        data.update(mut_type=instance.get_mut_type_display())

        if instance.img_paths:
            img_paths = instance.img_paths.split(',')
            img_paths = [MEDIA_PATH + item for item in img_paths]
            data.update(img_paths=img_paths)

        if 'https://thirdwx' not in instance.avatar_url:
            data.update(avatar_url=MEDIA_PATH+instance.avatar_url)

        return data
