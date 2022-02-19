import base64
import os
import shutil
from datetime import datetime
from random import randint

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.common import rand_nickname_list, set_uid
from utils.exceptions import HTTP_491_TOPIC_EXCEED_WORD_LIMIT, HTTP_496_MSG_SENSITIVE
from utils.pagination import TopicIdleJobPagination
from utils.wx_util import wx_msg_sec_check
from .models import IdleManage
from .serializers import IdleManageSerializer

BASE_DIR = str(settings.BASE_DIR)


class IdleManageViewSet(viewsets.ModelViewSet):
    queryset = IdleManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = IdleManageSerializer
    pagination_class = TopicIdleJobPagination

    def list(self, request, *args, **kwargs):
        return Response()

    @action(methods=['POST'], detail=False)
    def rand_spe_sch_data(self, request):
        """将指定学校的数据随机"""
        queryset = list(IdleManage.objects.filter(school='4'))
        rand_nickname = rand_nickname_list()
        rand_avatar_path = BASE_DIR + '/media/tmp_avatars/'
        files = os.listdir(rand_avatar_path)
        with transaction.atomic():
            for q in queryset:
                nick_index = randint(0, len(rand_nickname) - 1)
                file_index = randint(0, len(files) - 1)
                nickname = rand_nickname[nick_index]
                nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
                nickname = nickname_encoder.decode('utf-8')
                avatar_url = 'tmp_avatars/' + files[file_index]
                uid = set_uid()
                update_data = {
                    'uid': uid,
                    'nickname': nickname,
                    'avatar_url': avatar_url
                }
                # IdleManage.objects.select_for_update().filter(id=q.id).update(**update_data)
        return Response()

    @action(methods=['POST'], detail=False)
    def copy_data_to_sll_school(self, request):
        """将数据复制到所有学校"""
        MEDIA_ROOT = BASE_DIR + '/media/'
        TAR_IMG_PATH = MEDIA_ROOT + 'photos/2022-02-15/'
        rand_nickname = rand_nickname_list()
        rand_avatar_path = MEDIA_ROOT + 'tmp_avatars/'
        files = os.listdir(rand_avatar_path)

        base_queryset = list(IdleManage.objects.filter(school='4'))
        copy_to_school = ['1', '2', '3', '6', '7', '8', '9', '11']
        for sch in copy_to_school:
            create_data = []
            with transaction.atomic():
                for bi in base_queryset:
                    tmp_img_paths = bi.img_paths.split(',') if bi.img_paths else ''
                    t_img_paths = []
                    for ii in tmp_img_paths:
                        if not ii:
                            break
                        ini_img = MEDIA_ROOT + ii
                        img_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.now()) + str(randint(1000000, 9999999)) + '.jpg'
                        tar_img = TAR_IMG_PATH + img_name
                        # shutil.copyfile(ini_img, tar_img)
                        t_img_paths.append('photos/2022-02-15/' + img_name)

                    nick_index = randint(0, len(rand_nickname) - 1)
                    file_index = randint(0, len(files) - 1)
                    nickname = rand_nickname[nick_index]
                    nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
                    nickname = nickname_encoder.decode('utf-8')
                    avatar_url = 'tmp_avatars/' + files[file_index]
                    uid = set_uid()
                    create_data.append(IdleManage(
                        uid=uid,
                        nickname=nickname,
                        avatar_url=avatar_url,
                        phone=bi.phone,
                        wechat=bi.wechat,
                        content=bi.content,
                        price=bi.price,
                        idle_type=bi.idle_type,
                        school=sch,
                        img_paths=','.join(t_img_paths)
                    ))

                # IdleManage.objects.bulk_create(create_data)

        return Response()

    def create(self, request, *args, **kwargs):
        # 文本是否违规检测
        data = request.data
        openid = data.pop('openid', '')
        content = data.get('content', '')
        school = data.get('school', '')

        # 内容不能超过500个字
        if len(content) > 500:
            raise HTTP_491_TOPIC_EXCEED_WORD_LIMIT('描述内容长度超限')

        ret = wx_msg_sec_check(school, openid, content)
        if ret['suggest'] != 'pass':
            raise HTTP_496_MSG_SENSITIVE('描述含违规信息')

        nickname = data.get('nickname', '')
        nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
        data['nickname'] = nickname_encoder.decode('utf-8')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=False)
    def sch_list(self, request):
        school = request.query_params.get('school', '0')
        idle_type = request.query_params.get('idle_type', None)
        if idle_type:
            queryset = IdleManage.objects.filter(
                Q(school=school) & Q(idle_type=idle_type) & Q(is_deleted=False)).order_by('-create_time')
        else:
            queryset = IdleManage.objects.filter(Q(school=school) & Q(is_deleted=False)).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=False)
    def person_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = IdleManage.objects.filter(uid=uid).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_inst(self, request):
        uid = request.data.get('uid', '')
        inst_id = int(request.data.get('inst_id', 0))
        img_paths = request.data.get('img_paths', [])
        with transaction.atomic():
            IdleManage.objects.select_for_update().filter(Q(id=inst_id) & Q(uid=uid)).delete()
            if img_paths:
                MEDIA_ROOT = settings.MEDIA_ROOT
                try:
                    for path in img_paths:
                        if '.jpg' in path or '.png' in path:
                            img_abs_path = MEDIA_ROOT + path.split('media')[1]
                            os.remove(img_abs_path)
                except:
                    pass
            return Response()
