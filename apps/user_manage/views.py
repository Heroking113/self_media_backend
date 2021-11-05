from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.common import set_uid
from utils.wx_util import get_openid_session_key_by_code
from .models import UserManage
from .serializers import UserManageSerializer


class UserManageViewSet(viewsets.ModelViewSet):
    queryset = UserManage.objects.all()
    serializer_class = UserManageSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        js_code = request.data.get('js_code', '')
        # 获取 session_key 和 openid
        dic_session_key_openid = get_openid_session_key_by_code(js_code)
        session_key = dic_session_key_openid['session_key']
        openid = dic_session_key_openid['openid']

        query = UserManage.objects.filter(openid=openid)
        if query:
            serializer = self.get_serializer(query[0])
        else:
            query = UserManage.objects.create(session_key=session_key, openid=openid, uid=set_uid())
            serializer = self.get_serializer(query)

        return Response(serializer.data)


