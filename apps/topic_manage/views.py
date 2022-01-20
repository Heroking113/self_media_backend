# -*- coding: utf-8 -*-

import base64
import os
import shutil
from datetime import datetime
from random import randint

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.common import random_date
from utils.exceptions import HTTP_496_MSG_SENSITIVE
from utils.pagination import CommentMsgPagination, TopicPagination
from utils.wx_util import wx_msg_sec_check
from .models import TopicManage, CommentManage
from .serializers import TopicManageSerializer, CommentManageSerializer
from ..common_manage.models import Configuration
from ..file_manage.models import ImageFile


class TopicManageViewSet(viewsets.ModelViewSet):
    queryset = TopicManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = TopicManageSerializer
    pagination_class = TopicPagination

    @action(methods=['POST'], detail=False)
    def test(self, request):
        openid = request.data.get('openid', '')
        content = request.data.get('content', '')
        school = request.data.get('school', '')
        title = request.data.get('title', '')
        ret = wx_msg_sec_check(school, openid, content, title)
        if ret['suggest'] == 'pass':
            raise HTTP_496_MSG_SENSITIVE('存在违规/敏感信息')
        return Response()

    @action(methods=['POST'], detail=False)
    def fast_bulk_create(self, request):
        """
        快速将测试数据复制到别的学校
        """
        MEDIA_ROOT = '/Users/heroking/Documents/convertible_bond/cb_backend/media/'
        TAR_PATH = '/Users/heroking/Documents/convertible_bond/cb_backend/media/photos/2022-01-15/'
        start_time = '2021-12-24 08:00:00'
        end_time = '2021-12-25 02:00:00'
        nickname_list = Configuration.objects.get(key='nickname_list').uni_val
        nickname_list = nickname_list.split(',')
        root_path = '/Users/heroking/Documents/convertible_bond/cb_backend/media/tmp_avatars/'
        files = os.listdir(root_path)

        base_school_2_query = list(TopicManage.objects.filter(school='2'))
        create_data = []
        for bi in base_school_2_query:
            tmp_img_paths = bi.img_paths.split(',') if bi.img_paths else ''
            t_img_paths = []
            for ii in tmp_img_paths:
                if not ii:
                    break
                ini_img = MEDIA_ROOT + ii
                img_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.now()) + str(randint(1000000, 9999999)) + '.jpg'
                tar_img = TAR_PATH + img_name
                # shutil.copyfile(ini_img, tar_img)
                t_img_paths.append('photos/2022-01-15/'+img_name)

            nick_index = randint(0, len(nickname_list) - 1)
            file_index = randint(0, len(files) - 1)
            nickname = nickname_list[nick_index]
            nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
            nickname = nickname_encoder.decode('utf-8')
            avatar_url = 'tmp_avatars/' + files[file_index]
            create_data.append(TopicManage(
                uid='4wftqz5nbm3',
                nickname=nickname,
                avatar_url=avatar_url,
                title=bi.title,
                content=bi.content,
                topic_type=bi.topic_type,
                school='6',
                view_count=bi.view_count,
                img_paths=','.join(t_img_paths),
                create_time=random_date(start_time, end_time)
            ))

        # TopicManage.objects.bulk_create(create_data)
        return Response()

    @action(methods=['POST'], detail=False)
    def bulk_update_user_profile(self, request):
        """
            批量更新帖子的用户昵称和头像
        """
        nickname_list = Configuration.objects.get(key='nickname_list').uni_val
        nickname_list = nickname_list.split(',')

        root_path = '/Users/heroking/Documents/convertible_bond/cb_backend/media/tmp_avatars/'
        files = os.listdir(root_path)

        ids = [i[0] for i in TopicManage.objects.filter(school='3').values_list('id')]
        with transaction.atomic():
            for id in ids:
                nick_index = randint(0, len(nickname_list) - 1)
                file_index = randint(0, len(files) - 1)
                nickname = nickname_list[nick_index]
                nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
                nickname = nickname_encoder.decode('utf-8')
                avatar_url = 'tmp_avatars/' + files[file_index]
                # TopicManage.objects.select_for_update().filter(id=id).update(nickname=nickname, avatar_url=avatar_url)

        return Response()

    def create(self, request, *args, **kwargs):
        # 文本是否违规检测
        data = request.data
        openid = data.get('openid', '')
        content = data.get('content', '')
        school = data.get('school', '')
        title = data.get('title', '')
        ret = wx_msg_sec_check(school, openid, content, title)
        if ret['suggest'] != 'pass':
            raise HTTP_496_MSG_SENSITIVE('内容含违规信息')

        data.pop('openid')
        nickname = data.get('nickname', '')
        nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
        nickname = nickname_encoder.decode('utf-8')
        data['nickname'] = nickname
        serializer = self.get_serializer(data=data)
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
        school = int(request.data.get('school', '0'))
        uid = request.data.get('uid', '')
        inst_id = request.data.get('inst_id', 0)
        view_count = request.data.get('view_count', 0)

        limit_query = eval(Configuration.objects.get(key='topic_view_count_limit').uni_val)
        is_limit_open = True if limit_query[school][1] == 'open' else False
        with transaction.atomic():
            topic_query = TopicManage.objects.select_for_update().filter(id=inst_id)
            if not is_limit_open:
                topic_query.update(view_count=view_count)
                # 浏览量加1
                return Response({'up_status': 'plus'})
            view_uids = topic_query[0].view_uids
            view_uids = view_uids if view_uids else ''
            if uid in view_uids:
                # 浏览量不变
                return Response({'up_status': 'original'})
            view_uids = view_uids + uid + ','
            topic_query.update(view_uids=view_uids, view_count=view_count)
            # 浏览量加1
            return Response({'up_status': 'plus'})


    @action(methods=['GET'], detail=False)
    def person_data(self, request):
        uid = request.query_params.get('uid', '')
        topic_type = request.query_params.get('topic_type', '0')
        queryset = TopicManage.objects.filter(Q(uid=uid) & Q(topic_type=topic_type) & Q(is_deleted=False)).order_by('-create_time')
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

    def create(self, request, *args, **kwargs):
        # 文本是否违规检测
        data = request.data
        openid = data.pop('openid', '')
        content = data.get('content', '')
        school = data.pop('school', '')
        ret = wx_msg_sec_check(school, openid, content)
        if ret['suggest'] != 'pass':
            raise HTTP_496_MSG_SENSITIVE('内容含违规信息')

        nickname = data.get('nickname', '')
        nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
        nickname = nickname_encoder.decode('utf-8')
        data['nickname'] = nickname
        if data.get('is_sec_comment', False):
            fir_comment_nickname = data['fir_comment_nickname']
            fir_comment_nickname_encoder = base64.b64encode(fir_comment_nickname.encode('utf-8'))
            fir_comment_nickname = fir_comment_nickname_encoder.decode('utf-8')
            data['fir_comment_nickname'] = fir_comment_nickname
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['GET'], detail=False)
    def person_comment_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = CommentManage.objects.filter(Q(uid=uid) | Q(fir_comment_uid=uid)).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_comment(self, request):
        comment_id = int(request.data.get('comment_id', 0))
        with transaction.atomic():
            CommentManage.objects.select_for_update().filter(id=comment_id).delete()
            return Response()
