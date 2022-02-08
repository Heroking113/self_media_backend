import base64

from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.exceptions import HTTP_496_MSG_SENSITIVE
from utils.pagination import TopicIdleJobPagination
from utils.wx_util import wx_msg_sec_check
from .models import JobManage
from .serializers import JobManageSerializer


class JobManageViewSet(viewsets.ModelViewSet):
    queryset = JobManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = JobManageSerializer
    pagination_class = TopicIdleJobPagination

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
        queryset = JobManage.objects.filter(uid=uid)
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
