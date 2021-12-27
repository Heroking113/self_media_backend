import base64
import os
from datetime import timedelta, datetime
from random import randint

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.redis_cli import redisCli
from .models import UserManage, AssetManage
from .serializers import UserManageSerializer, AssetManageSerializer

from utils.common import set_uid, upload_path_handler
from .models import SchUserManage
from .serializers import SchUserManageSerializer
from ..common_manage.tasks import update_user_profile
from utils.wx_util import get_openid_session_key_by_code

FLAG = 1


class SchUserManageViewSet(viewsets.ModelViewSet):
    queryset = SchUserManage.objects.all()
    serializer_class = SchUserManageSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        query = SchUserManage.objects.filter(uid=uid)
        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        js_code = request.data.get('js_code', '')
        school = int(request.data.get('school', 0))
        SCH_ID_SECRET = settings.SCH_ID_SECRET[school]
        # 获取 session_key 和 openid
        app_id = SCH_ID_SECRET['APP_ID']
        app_secret = SCH_ID_SECRET['APP_SECRET']
        dic_session_key_openid = get_openid_session_key_by_code(js_code, app_id, app_secret)
        session_key = dic_session_key_openid['session_key']
        openid = dic_session_key_openid['openid']

        query = SchUserManage.objects.filter(Q(openid=openid) & Q(school=school))
        if query:
            serializer = self.get_serializer(query[0])
        else:
            query = SchUserManage.objects.create(session_key=session_key,
                                                 openid=openid,
                                                 school=school,
                                                 uid=set_uid())
            serializer = self.get_serializer(query)

        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def update_profile(self, request):
        data = request.data
        nickname = data.get('nickname', '')
        if not nickname:
            queryset = SchUserManage.objects.get(uid=data['uid'])
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)

        nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
        nickname = nickname_encoder.decode('utf-8')
        data['nickname'] = nickname
        update_data = {'nickname': nickname}
        if 'avatar_url' in data:
            update_data['avatar_url'] = data['avatar_url']
        with transaction.atomic():
            SchUserManage.objects.select_for_update().filter(uid=data['uid']).update(**update_data)
            update_user_profile.delay(data, is_update_userprofile=False)
            queryset = SchUserManage.objects.get(uid=data['uid'])
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def identity_authenticate(self, request):
        uid = request.data.get('uid', '')
        school_card = request.FILES.get('school_card', '')

        today_dir = upload_path_handler('school_card') + '/'
        img_dir = settings.MEDIA_ROOT + '/' + today_dir
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        img_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.now()) + str(randint(1000000, 9999999)) + '.jpg'

        rela_img_path = today_dir + img_name
        abs_img_path = img_dir + img_name

        with transaction.atomic():
            sch_query = SchUserManage.objects.select_for_update().filter(uid=uid)
            sch_query.update(school_card=rela_img_path)
            with open(abs_img_path, 'wb') as f:
                # 多次写入
                for i in school_card.chunks():
                    f.write(i)
            SchUserManage.handle_school_card_authenticate(abs_img_path, sch_query)
            serializer = self.get_serializer(sch_query[0])
        return Response(serializer.data)


class UserManageViewSet(viewsets.ModelViewSet):
    queryset = UserManage.objects.all()
    serializer_class = UserManageSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', '')
        query = UserManage.objects.filter(uid=uid)
        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        js_code = request.data.get('js_code', '')
        # 获取 session_key 和 openid
        app_id = settings.APP_ID
        app_secret = settings.APP_SECRET
        dic_session_key_openid = get_openid_session_key_by_code(js_code, app_id, app_secret)
        session_key = dic_session_key_openid['session_key']
        openid = dic_session_key_openid['openid']

        query = UserManage.objects.filter(openid=openid)
        if query:
            serializer = self.get_serializer(query[0])
        else:
            query = UserManage.objects.create(session_key=session_key, openid=openid, uid=set_uid())
            serializer = self.get_serializer(query)

        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def update_info(self, request):
        data = request.data
        nickname = data.get('nickname', '')
        nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
        nickname = nickname_encoder.decode('utf-8')
        data['nickname'] = nickname
        uid = data.pop('uid', '')
        with transaction.atomic():
            UserManage.objects.select_for_update().filter(uid=uid).update(**data)
        query = UserManage.objects.filter(uid=uid)[0]
        serializer = self.get_serializer(query)
        return Response(serializer.data)


class AssetManageViewSet(viewsets.ModelViewSet):
    queryset = AssetManage.objects.all().order_by('-create_time')
    serializer_class = AssetManageSerializer
    pagination_class = None

    def get_queryset(self):
        uid = self.request.query_params.get('uid', '')
        before_days = int(self.request.query_params.get('before_days', 0))
        if not before_days:
            return AssetManage.objects.filter(uid=uid).order_by('-id')

        before_date = datetime.today() + timedelta(-before_days)
        return AssetManage.objects.filter(Q(uid=uid) & Q(create_time__gte=before_date)).order_by('-id')



    @action(methods=['GET'], detail=False)
    def bulk_create(self, request):
        from random import randint
        bk_data = [AssetManage(
            uid='4alug9vxig9',
            day_asset=randint(100, 10000),
            day_pl=randint(100, 10000),
            create_time=datetime.today() + timedelta(-i)
        ) for i in range(100)]
        AssetManage.objects.bulk_create(bk_data)
        return Response()

