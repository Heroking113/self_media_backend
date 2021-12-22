import json
import os
from datetime import datetime
from random import randint

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import serializers

from .models import ImageFile
from .tasks import async_img_sec_check
from ..idle_manage.models import IdleManage
from ..topic_manage.models import TopicManage
from ..common_manage.tasks import update_user_profile


class ImageFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageFile
        fields = '__all__'

    # 字段校验
    imgs = serializers.ListField(
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=True), write_only=True
    )

    def create(self, validated_data):
        imgs = validated_data.get('imgs')
        inst_type = self.initial_data.get('inst_type', '0')
        inst_id = self.initial_data.get('inst_id', '0')
        school = self.initial_data.get('school', '0')

        if inst_type == '4':
            with transaction.atomic():
                pre_query = ImageFile.objects.select_for_update().filter(Q(inst_id=inst_id)
                                                                         & Q(inst_type=inst_type)
                                                                         & Q(school=school))
                if pre_query:
                    for item in pre_query:
                        os.remove(settings.MEDIA_ROOT + '/' + item.file_path.name)
                    pre_query.delete()

        img_list = []
        li_params = []
        for index, url in enumerate(imgs):
            pic_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.now()) + str(randint(1000000, 9999999))
            url.name = pic_name + '.jpg'
            img_list.append(ImageFile(
                file_path=url,
                inst_type=inst_type,
                inst_id=inst_id,
                school=school
            ))
            # 检测图片
            now_date = datetime.now().strftime('%Y-%m-%d')
            li_params.append({
                'file_path': str(settings.MEDIA_ROOT) + '/photos/' + now_date + '/' + url.name,
                'inst_type': inst_type,
                'inst_id': inst_id,
                'school': school
            })

        ret = ImageFile.objects.bulk_create(img_list)
        with transaction.atomic():
            if inst_type == '2':
                # 帖子
                base_img_paths = TopicManage.objects.select_for_update().get(id=inst_id).img_paths
                img_paths = base_img_paths + ',' + ','.join(
                    [item.file_path.name for item in ret]) if base_img_paths else ','.join(
                    [item.file_path.name for item in ret])
                TopicManage.objects.select_for_update().filter(id=inst_id).update(img_paths=img_paths)
            elif inst_type == '3':
                # 闲置
                base_img_paths = IdleManage.objects.select_for_update().get(id=inst_id).img_paths
                img_paths = base_img_paths + ',' + ','.join(
                    [item.file_path.name for item in ret]) if base_img_paths else ','.join(
                    [item.file_path.name for item in ret])
                IdleManage.objects.select_for_update().filter(id=inst_id).update(img_paths=img_paths)

        if inst_type == '4':
            # avatar
            user_profile = {
                'avatar_url': ret[0].file_path.name,
                'uid': inst_id,
                'school': school
            }
            update_user_profile.delay(user_profile)
        # 图片违规检测
        async_img_sec_check.delay(json.dumps(li_params))

        # 必须要有个返回值，不然报错
        return ret