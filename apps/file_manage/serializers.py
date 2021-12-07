from datetime import datetime

from django.conf import settings
from django.db import transaction
from rest_framework import serializers

from .models import ImageFile
from ..idle_manage.models import IdleManage
from ..mood_manage.models import MoodManage


class ImageFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageFile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(inst_type=instance.get_inst_type_display())
        data.update(create_time=str(instance.create_time).split('.')[0])
        return data

    # 字段校验
    imgs = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=True), write_only=True
    )

    def create(self, validated_data):
        imgs = validated_data.get('imgs')
        inst_type = self.initial_data.get('inst_type', '0')
        inst_id = int(self.initial_data.get('inst_id', 0))

        img_list = []
        li_params = []
        for index, url in enumerate(imgs):
            pic_name = url.name
            pic_name += '_{0:%Y%m%d%H%M%S%f}'.format(datetime.now())
            url.name = pic_name + '.jpg'
            img_list.append(ImageFile(
                file_path=url,
                inst_type=inst_type,
                inst_id=inst_id
            ))
            li_params.append({
                'file_path': str(settings.BASE_DIR) + '/media/photos/' + url.name,
                'inst_type': inst_type,
                'inst_id': inst_id
            })

        ret = ImageFile.objects.bulk_create(img_list)
        with transaction.atomic():
            if inst_type == '1':
                # 闲置
                base_img_paths = IdleManage.objects.select_for_update().get(id=inst_id).img_paths
                img_paths = base_img_paths + ',' + ','.join(
                    [item.file_path.name for item in ret]) if base_img_paths else ','.join(
                    [item.file_path.name for item in ret])
                IdleManage.objects.select_for_update().filter(id=inst_id).update(img_paths=img_paths)
            elif inst_type == '2':
                # 帖子
                base_img_paths = MoodManage.objects.select_for_update().get(id=inst_id).img_paths
                img_paths = base_img_paths + ',' + ','.join(
                    [item.file_path.name for item in ret]) if base_img_paths else ','.join(
                    [item.file_path.name for item in ret])
                MoodManage.objects.select_for_update().filter(id=inst_id).update(img_paths=img_paths)
        # 图片违规检测
        # async_img_sec_check.delay(json.dumps(li_params))

        # 必须要有个返回值，不然报错
        return ret[0]