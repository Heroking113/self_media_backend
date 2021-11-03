from rest_framework import serializers

from .models import UserManage


class UserManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserManage
        fields = '__all__'
