import base64
import os
from random import randint

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.common import rand_nickname_list, set_uid
from utils.exceptions import HTTP_496_MSG_SENSITIVE
from utils.pagination import TopicIdleJobPagination
from utils.wx_util import wx_msg_sec_check
from .models import JobManage
from .serializers import JobManageSerializer

BASE_DIR = str(settings.BASE_DIR)

class JobManageViewSet(viewsets.ModelViewSet):
    queryset = JobManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = JobManageSerializer
    pagination_class = TopicIdleJobPagination

    def list(self, request, *args, **kwargs):
        return Response()

    @action(methods=['POST'], detail=False)
    def rand_spe_sch_data(self, request):
        """将指定学校的数据随机"""
        queryset = list(JobManage.objects.filter(school='4'))
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
                # JobManage.objects.select_for_update().filter(id=q.id).update(**update_data)
        return Response()

    @action(methods=['POST'], detail=False)
    def copy_data_to_sll_school(self, request):
        """将数据复制到所有学校"""
        MEDIA_ROOT = BASE_DIR + '/media/'
        rand_nickname = rand_nickname_list()
        rand_avatar_path = MEDIA_ROOT + 'tmp_avatars/'
        files = os.listdir(rand_avatar_path)

        base_queryset = list(JobManage.objects.filter(school='4'))
        copy_to_school = ['1', '2', '3', '6', '7', '8', '9', '11']
        for sch in copy_to_school:
            create_data = []
            with transaction.atomic():
                for bi in base_queryset:
                    nick_index = randint(0, len(rand_nickname) - 1)
                    file_index = randint(0, len(files) - 1)
                    nickname = rand_nickname[nick_index]
                    nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
                    nickname = nickname_encoder.decode('utf-8')
                    avatar_url = 'tmp_avatars/' + files[file_index]
                    uid = set_uid()
                    create_data.append(JobManage(
                        uid=uid,
                        nickname=nickname,
                        avatar_url=avatar_url,
                        phone=bi.phone,
                        wechat=bi.wechat,
                        email=bi.email,
                        job_name=bi.job_name,
                        content=bi.content,
                        salary=bi.salary,
                        job_type=bi.job_type,
                        school=sch
                    ))

                # JobManage.objects.bulk_create(create_data)

        return Response()

    def create(self, request, *args, **kwargs):
        # 文本是否违规检测
        data = request.data
        openid = data.pop('openid', '')
        school = data.get('school', '')
        content = data.get('content', '')
        job_name = data.get('job_name', '')

        ret = wx_msg_sec_check(school, openid, content, job_name)
        if ret['suggest'] != 'pass':
            raise HTTP_496_MSG_SENSITIVE('招聘信息含违规内容')

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
        job_type = request.query_params.get('job_type', None)
        if job_type:
            queryset = JobManage.objects.filter(
                Q(school=school) & Q(job_type=job_type) & Q(is_deleted=False)).order_by('-create_time')
        else:
            queryset = JobManage.objects.filter(Q(school=school) & Q(is_deleted=False)).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=False)
    def person_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = JobManage.objects.filter(uid=uid).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_inst(self, request):
        inst_id = int(request.data.get('inst_id', 0))
        with transaction.atomic():
            query = JobManage.objects.select_for_update().filter(id=inst_id)
            query.delete()
            return Response()

    @action(methods=['POST'], detail=False)
    def soft_del(self, request):
        inst_id = int(request.data.get('inst_id', '0'))
        JobManage.objects.filter(id=inst_id).update(is_deleted=True)
        return Response()

    @action(methods=['GET'], detail=False)
    def search(self, request):
        search_str = request.query_params.get('search_str', '')
        school = request.query_params.get('school', '0')
        queryset = JobManage.objects.filter(Q(school=school) & Q(content__icontains=search_str)).order_by('-create_time')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
