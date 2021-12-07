import os

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.pagination import CommentMsgPagination
from .models import MoodManage, CommentManage
from .serializers import MoodManageSerializer, CommentManageSerializer
from ..file_manage.models import ImageFile


class MoodManageViewSet(viewsets.ModelViewSet):
    queryset = MoodManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = MoodManageSerializer

    @action(methods=['POST'], detail=False)
    def update_detail(self, request):
        mood_id = request.data.get('mood_id', 0)
        view_count = request.data.get('view_count', 0)
        with transaction.atomic():
            MoodManage.objects.select_for_update().filter(id=mood_id).update(view_count=view_count)
            return Response({'status': 'success'})

    @action(methods=['GET'], detail=False)
    def person_mood_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = MoodManage.objects.filter(uid=uid).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_mood(self, request):
        mood_id = int(request.data.get('mood_id', 0))
        with transaction.atomic():
            mood_query = MoodManage.objects.select_for_update().filter(id=mood_id)
            if not mood_query:
                return Response()
            img_paths = mood_query[0].img_paths.split(',')
            print(img_paths)
            try:
                for item in img_paths:
                    os.remove(settings.MEDIA_ROOT + '/' + item)
            except:
                pass
            ImageFile.objects.select_for_update().filter(file_path__in=img_paths).delete()
            CommentManage.objects.select_for_update().filter(mood_id=mood_id).delete()
            mood_query.delete()
            return Response()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentManage.objects.all()
    serializer_class = CommentManageSerializer
    pagination_class = CommentMsgPagination

    def get_queryset(self):
        mood_id = int(self.request.query_params.get('mood_id', 0))
        return CommentManage.objects.filter(Q(mood_id=mood_id) & Q(is_deleted=False))

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
