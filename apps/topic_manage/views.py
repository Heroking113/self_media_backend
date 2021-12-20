import base64
import os

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.pagination import CommentMsgPagination, TopicPagination
from .models import TopicManage, CommentManage
from .serializers import TopicManageSerializer, CommentManageSerializer
from ..file_manage.models import ImageFile


class TopicManageViewSet(viewsets.ModelViewSet):
    queryset = TopicManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = TopicManageSerializer
    pagination_class = TopicPagination

    def create(self, request, *args, **kwargs):
        data = request.data
        nickname = data.get('nickname', '')
        nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
        nickname = nickname_encoder.decode('utf-8')
        data['nickname'] = nickname
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=False)
    def sch_list(self, request):
        school=request.query_params.get('school', '0')
        topic_type = request.query_params.get('topic_type', None)
        if topic_type:
            queryset = TopicManage.objects.filter(Q(school=school) & Q(topic_type=topic_type) & Q(is_deleted=False)).order_by('-create_time')
        else:
            queryset = TopicManage.objects.filter(Q(school=school) & Q(is_deleted=False)).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def update_detail(self, request):
        inst_id = request.data.get('inst_id', 0)
        view_count = request.data.get('view_count', 0)
        with transaction.atomic():
            TopicManage.objects.select_for_update().filter(id=inst_id).update(view_count=view_count)
            return Response({'status': 'success'})

    @action(methods=['GET'], detail=False)
    def person_data(self, request):
        uid = request.query_params.get('uid', '')
        topic_type = request.query_params.get('topic_type', '0')
        queryset = TopicManage.objects.filter(Q(uid=uid) & Q(topic_type=topic_type)).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_topic(self, request):
        topic_id = int(request.data.get('topic_id', 0))
        with transaction.atomic():
            topic_query = TopicManage.objects.select_for_update().filter(id=topic_id)
            if not topic_query:
                return Response()
            img_paths = topic_query[0].img_paths.split(',')
            try:
                for item in img_paths:
                    os.remove(settings.MEDIA_ROOT + '/' + item)
            except:
                pass
            ImageFile.objects.select_for_update().filter(file_path__in=img_paths).delete()
            CommentManage.objects.select_for_update().filter(inst_id=topic_id).delete()
            topic_query.delete()
            return Response()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentManage.objects.all()
    serializer_class = CommentManageSerializer
    pagination_class = CommentMsgPagination

    def get_queryset(self):
        inst_id = int(self.request.query_params.get('inst_id', 0))
        return CommentManage.objects.filter(Q(inst_id=inst_id) & Q(is_deleted=False))

    @action(methods=['GET'], detail=False)
    def person_comment_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = CommentManage.objects.filter(Q(uid=uid) | Q(fir_comment_uid=uid))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_comment(self, request):
        comment_id = int(request.data.get('comment_id', 0))
        with transaction.atomic():
            CommentManage.objects.select_for_update().filter(id=comment_id).delete()
            return Response()
