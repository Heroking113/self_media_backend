from django.conf import settings
from rest_framework import serializers

from .models import MoodManage, CommentManage

MEDIA_PATH = settings.DOMAIN + '/media/'

class MoodManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoodManage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
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
        img_paths = [MEDIA_PATH + item for item in img_paths]
        data.update(img_paths=img_paths)
        return data


class CommentManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentManage
        fields = '__all__'
