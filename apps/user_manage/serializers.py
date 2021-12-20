import base64

from rest_framework import serializers

from .models import UserManage, AssetManage, SchUserManage


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
        data.update(gender=instance.get_gender_display())
        data.update(create_time=str(instance.create_time).split('.')[0])
        data.update(lasted_time=str(instance.lasted_time).split('.')[0])
        return data