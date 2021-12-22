import base64

from django.conf import settings
from rest_framework import serializers

from .models import UserManage, AssetManage, SchUserManage

MEDIA_PATH = settings.DOMAIN + '/media/'


class UserManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserManage
        fields = ['uid', 'nickname', 'avatar_url', 'unionid', 'gender', 'city', 'province']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(nickname=base64.b64decode(instance.nickname).decode('utf-8'))
        data.update(gender=instance.get_gender_display())
        data.update(create_time=str(instance.create_time).split('.')[0])
        return data


class AssetManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetManage
        fields = ['day_asset', 'day_pl', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(create_time=str(instance.create_time).split(' ')[0].replace('-', '·'))
        return data


class SchUserManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchUserManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(nickname=base64.b64decode(instance.nickname).decode('utf-8'))
        data.update(create_time=str(instance.create_time).split('.')[0])
        data.update(lasted_time=str(instance.lasted_time).split('.')[0])
        if 'https://thirdwx' not in instance.avatar_url and instance.avatar_url:
            data.update(avatar_url=MEDIA_PATH+instance.avatar_url)
        return data
