from rest_framework import serializers

from .models import UserManage, AssetManage


class UserManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserManage
        fields = ['uid', 'nickname', 'avatar_url', 'unionid', 'gender', 'city', 'province']

    def to_representation(self, instance):
        data = super().to_representation(instance)
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
