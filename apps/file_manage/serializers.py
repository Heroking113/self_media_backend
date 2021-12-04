from rest_framework import serializers

from .models import ImageFile


class ImageFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageFile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(inst_type=instance.get_inst_type_display())
        data.update(create_time=str(instance.create_time).split('.')[0])
        return data