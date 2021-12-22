from rest_framework import serializers
from django.conf import settings

from .models import SchSwiper

MEDIA_PATH = settings.DOMAIN + '/media/'


class SchSwiperSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchSwiper
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(school=instance.get_school_display())
        data.update(swiper_type=instance.get_swiper_type_display())
        data.update(img_path=MEDIA_PATH+instance.img_path.name)
        return data