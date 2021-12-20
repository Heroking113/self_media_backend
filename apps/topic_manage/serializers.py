import base64

from django.conf import settings
from rest_framework import serializers

from utils.common import format_datetime
from .models import TopicManage, CommentManage

MEDIA_PATH = settings.DOMAIN + '/media/'

class TopicManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data.update(nickname=base64.b64decode(instance.nickname).decode('utf-8'))
        except:
            pass

        create_time = format_datetime(instance.create_time)
        data.update(create_time=create_time)

        if instance.img_paths:
            img_paths = instance.img_paths.split(',')
            img_paths = [MEDIA_PATH + item for item in img_paths]
            data.update(img_paths=img_paths)
        return data


class CommentManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentManage
        fields = '__all__'
