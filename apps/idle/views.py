import base64
import os

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.exceptions import HTTP_491_TOPIC_EXCEED_WORD_LIMIT, HTTP_496_MSG_SENSITIVE
from utils.pagination import TopicIdleJobPagination
from utils.wx_util import wx_msg_sec_check
from .models import IdleManage
from .serializers import IdleManageSerializer
from ..file_manage.models import ImageFile


class IdleManageViewSet(viewsets.ModelViewSet):
    queryset = IdleManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = IdleManageSerializer
    pagination_class = TopicIdleJobPagination

    def create(self, request, *args, **kwargs):
        # 文本是否违规检测
        data = request.data
        openid = data.pop('openid', '')
        content = data.get('content', '')
        school = data.get('school', '')

        # 内容不能超过300个字
        if len(content) > 300:
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
        queryset = IdleManage.objects.filter(uid=uid)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_inst(self, request):
        inst_id = int(request.data.get('inst_id', 0))
        img_paths = request.data.get('img_paths')
        media_root = settings.MEDIA_ROOT
        with transaction.atomic():
            try:
                for path in img_paths:
                    img_abs_path = media_root + path.split('media')[1]
                    os.remove(img_abs_path)
            except:
                pass
            IdleManage.objects.select_for_update().filter(id=inst_id).delete()
            return Response()
