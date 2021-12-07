from django.db import transaction
from django.conf import settings

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.common import set_uid
from .models import ZsdxUserManage
from .serializers import ZsdxUserManageSerializer
from utils.wx_util import get_openid_session_key_by_code


class ZsdxUserManageViewSet(viewsets.ModelViewSet):
    queryset = ZsdxUserManage.objects.all()
    serializer_class = ZsdxUserManageSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        query = ZsdxUserManage.objects.filter(uid=uid)
        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        js_code = request.data.get('js_code', '')
        # 获取 session_key 和 openid
        app_id = settings.ZSDX_APP_ID
        app_secret = settings.ZSDX_APP_SECRET
        dic_session_key_openid = get_openid_session_key_by_code(js_code, app_id, app_secret)
        session_key = dic_session_key_openid['session_key']
        openid = dic_session_key_openid['openid']

        query = ZsdxUserManage.objects.filter(openid=openid)
        if query:
            serializer = self.get_serializer(query[0])
        else:
            query = ZsdxUserManage.objects.create(session_key=session_key, openid=openid, uid=set_uid())
            serializer = self.get_serializer(query)

        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def update_info(self, request):
        data = request.data
        uid = data.pop('uid', '')
        with transaction.atomic():
            ZsdxUserManage.objects.select_for_update().filter(uid=uid).update(**data)
        query = ZsdxUserManage.objects.filter(uid=uid)[0]
        serializer = self.get_serializer(query)
        return Response(serializer.data)
