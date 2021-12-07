import os

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import IdleManage
from .serializers import IdleManageSerializer
from ..file_manage.models import ImageFile


class IdleManageViewSet(viewsets.ModelViewSet):
    queryset = IdleManage.objects.filter(Q(order_status='1') & Q(is_deleted=False)).order_by('-create_time')
    serializer_class = IdleManageSerializer

    @action(methods=['GET'], detail=False)
    def person_idle_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = IdleManage.objects.filter(uid=uid)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def update_info(self, request):
        idle_id = int(request.data.get('idle_id', 0))
        order_status = request.data.get('order_status', '3')
        update_data = {}
        update_data.update(order_status=order_status)
        with transaction.atomic():
            IdleManage.objects.select_for_update().filter(id=idle_id).update(**update_data)
            return Response()

    @action(methods=['POST'], detail=False)
    def del_idle(self, request):
        idle_id = int(request.data.get('idle_id', 0))
        with transaction.atomic():
            idle_query = IdleManage.objects.select_for_update().filter(id=idle_id)
            if not idle_query:
                return Response()
            img_paths = idle_query[0].img_paths.split(',')
            try:
                for item in img_paths:
                    os.remove(settings.MEDIA_ROOT + '/' + item)
            except:
                pass
            ImageFile.objects.select_for_update().filter(file_path__in=img_paths).delete()
            idle_query.delete()
            return Response()

