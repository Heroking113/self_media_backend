from rest_framework import serializers

from .models import UserManage


class UserManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserManage
        fields = ['uid', 'nickname', 'avatar_url', 'unionid', 'openid', 'gender', 'city', 'province']
