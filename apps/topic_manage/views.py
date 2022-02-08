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
from utils.exceptions import HTTP_496_MSG_SENSITIVE, HTTP_491_TOPIC_EXCEED_WORD_LIMIT
from utils.pagination import CommentMsgPagination, TopicIdleJobPagination
from utils.wx_util import wx_msg_sec_check
from .models import TopicManage, CommentManage
from .serializers import TopicManageSerializer, CommentManageSerializer
from .tasks import async_del_topic
from ..common_manage.models import Configuration
from ..file_manage.models import ImageFile


class TopicManageViewSet(viewsets.ModelViewSet):
    queryset = TopicManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = TopicManageSerializer
    pagination_class = TopicIdleJobPagination

    @action(methods=['POST'], detail=False)
    def test(self, request):
        """更新所有的帖子标题和内容为base64编码"""
        # with transaction.atomic():
        #     queryset = list(TopicManage.objects.select_for_update().all())
        #     for qi in queryset:
        #         content = base64.b64encode(qi.content.encode('utf-8'))
        #         kwargs = {'content': content.decode('utf-8')}
        #         if qi.title:
        #             title = base64.b64encode(qi.title.encode('utf-8'))
        #             kwargs['title'] = title.decode('utf-8')
        #         TopicManage.objects.select_for_update().filter(id=qi.id).update(**kwargs)

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
        openid = data.pop('openid', '')
        content = data.get('content', '')
        school = data.get('school', '')
        title = data.get('title', '')

        # title不能超过30个字；内容不能超过200个字
        if len(title) > 30 or len(content) > 200:
            raise HTTP_491_TOPIC_EXCEED_WORD_LIMIT('标题/内容长度超限')

        ret = wx_msg_sec_check(school, openid, content, title)
        if ret['suggest'] != 'pass':
            raise HTTP_496_MSG_SENSITIVE('内容含违规信息')

        if title:
            title_encoder = base64.b64encode(title.encode('utf-8'))
            data['title'] = title_encoder.decode('utf-8')

        content_encoder = base64.b64encode(content.encode('utf-8'))
        data['content'] = content_encoder.decode('utf-8')

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
        queryset = TopicManage.objects.filter(uid=uid).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_inst(self, request):
        inst_id = int(request.data.get('inst_id', 0))
        img_paths = request.data.get('img_paths')
        # async_del_topic.delay(inst_id, img_paths)
        media_root = settings.MEDIA_ROOT
        with transaction.atomic():
            try:
                for path in img_paths:
                    img_abs_path = media_root + path.split('media')[1]
                    os.remove(img_abs_path)
            except:
                pass
            TopicManage.objects.select_for_update().filter(id=inst_id).delete()
            return Response()

    @action(methods=['POST'], detail=False)
    def soft_del(self, request):
        inst_id = int(request.data.get('inst_id', '0'))
        TopicManage.objects.filter(id=inst_id).update(is_deleted=True)
        return Response()

    @action(methods=['GET'], detail=False)
    def search(self, request):
        search_str = request.query_params.get('search_str', '')
        search_str = base64.b64encode(search_str.encode('utf-8')).decode('utf-8')
        school = request.query_params.get('school', '0')
        queryset = TopicManage.objects.filter(Q(school=school) & (Q(title__icontains=search_str) | Q(content__icontains=search_str))).order_by('-create_time')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = CommentManage.objects.all()
    serializer_class = CommentManageSerializer
    pagination_class = CommentMsgPagination

    @action(methods=['POST'], detail=False)
    def test(self, request):
        """更新所有的评论为base64编码"""
        # with transaction.atomic():
        #     queryset = list(CommentManage.objects.select_for_update().all())
        #     for qi in queryset:
        #         content = base64.b64encode(qi.content.encode('utf-8'))
        #         kwargs = {'content': content.decode('utf-8')}
        #         CommentManage.objects.select_for_update().filter(id=qi.id).update(**kwargs)

        return Response()

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

        # 评论不能超过100个字
        if len(content) > 100:
            raise HTTP_491_TOPIC_EXCEED_WORD_LIMIT('评论长度超限')

        if ret['suggest'] != 'pass':
            raise HTTP_496_MSG_SENSITIVE('内容含违规信息')

        content_encoder = base64.b64encode(content.encode('utf-8'))
        data['content'] = content_encoder.decode('utf-8')

        nickname = data.get('nickname', '')
        nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
        data['nickname'] = nickname_encoder.decode('utf-8')
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
    def person_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = CommentManage.objects.filter(Q(uid=uid) | Q(fir_comment_uid=uid)).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_inst(self, request):
        inst_id = int(request.data.get('inst_id', 0))
        with transaction.atomic():
            CommentManage.objects.select_for_update().filter(id=inst_id).delete()
            return Response()
