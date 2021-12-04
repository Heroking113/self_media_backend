from rest_framework import serializers

from .models import MoodManage


class MoodManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoodManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(create_time=str(instance.create_time).split('.')[0])
        return data