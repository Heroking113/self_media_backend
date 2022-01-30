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
        data.update(nickname=base64.b64decode(instance.nickname).decode('utf-8'))
        data.update(content=base64.b64decode(instance.content).decode('utf-8'))
        if instance.title:
            data.update(title=base64.b64decode(instance.title).decode('utf-8'))

        if 'https://thirdwx' not in instance.avatar_url:
            data.update(avatar_url=MEDIA_PATH+instance.avatar_url)

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(nickname=base64.b64decode(instance.nickname).decode('utf-8'))
        data.update(content=base64.b64decode(instance.content).decode('utf-8'))
        if instance.is_sec_comment:
            data.update(fir_comment_nickname=base64.b64decode(instance.fir_comment_nickname).decode('utf-8'))

        return data
