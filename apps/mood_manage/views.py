from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MoodManage, CommentManage
from .serializers import MoodManageSerializer, CommentManageSerializer


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
        queryset = MoodManage.objects.filter(uid=uid)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentManage.objects.all()
    serializer_class = CommentManageSerializer

    def get_queryset(self):
        mood_id = int(self.request.query_params.get('mood_id', 0))
        return CommentManage.objects.filter(Q(mood_id=mood_id) & Q(is_deleted=False))

    @action(methods=['GET'], detail=False)
    def person_comment_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = CommentManage.objects.filter(uid=uid)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)



