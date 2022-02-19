import base64
import json
import os
import logging
import shutil
from datetime import datetime
from random import randint

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.common import random_date, rand_nickname_list, set_uid
from utils.exceptions import HTTP_496_MSG_SENSITIVE, HTTP_491_TOPIC_EXCEED_WORD_LIMIT
from utils.pagination import CommentMsgPagination, TopicIdleJobPagination
from utils.wx_util import wx_msg_sec_check
from .models import TopicManage, CommentManage
from .serializers import TopicManageSerializer, CommentManageSerializer
from ..common_manage.models import Configuration

BASE_DIR = str(settings.BASE_DIR)

logger = logging.getLogger('cb_backend')

class TopicManageViewSet(viewsets.ModelViewSet):
    queryset = TopicManage.objects.filter(is_deleted=False).order_by('-create_time')
    serializer_class = TopicManageSerializer
    pagination_class = TopicIdleJobPagination

    def list(self, request, *args, **kwargs):
        return Response()

    @action(methods=['POST'], detail=False)
    def rand_spe_sch_data(self, request):
        """将指定学校的数据随机"""
        queryset = list(TopicManage.objects.filter(school='4'))
        start_time = '2022-02-14 08:00:00'
        end_time = '2022-02-15 02:00:00'
        rand_nickname = rand_nickname_list()
        rand_avatar_path = BASE_DIR + '/media/tmp_avatars/'
        files = os.listdir(rand_avatar_path)
        with transaction.atomic():
            for q in queryset:
                nick_index = randint(0, len(rand_nickname) - 1)
                file_index = randint(0, len(files) - 1)
                nickname = rand_nickname[nick_index]
                nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
                nickname = nickname_encoder.decode('utf-8')
                avatar_url = 'tmp_avatars/' + files[file_index]
                uid = set_uid()
                view_count = randint(0, 30)
                update_data = {
                    'uid': uid,
                    'nickname': nickname,
                    'avatar_url': avatar_url,
                    'view_count': view_count,
                    'create_time': random_date(start_time, end_time)
                }
                # TopicManage.objects.select_for_update().filter(id=q.id).update(**update_data)
        return Response()

    @action(methods=['POST'], detail=False)
    def copy_data_to_sll_school(self, request):
        """将数据复制到所有学校"""
        MEDIA_ROOT = BASE_DIR + '/media/'
        TAR_IMG_PATH = MEDIA_ROOT + 'photos/2022-02-15/'
        start_time = '2022-02-14 08:00:00'
        end_time = '2022-02-15 02:00:00'
        rand_nickname = rand_nickname_list()
        rand_avatar_path = MEDIA_ROOT + 'tmp_avatars/'
        files = os.listdir(rand_avatar_path)

        base_queryset = list(TopicManage.objects.filter(school='4'))
        copy_to_school = ['1', '2', '3', '6', '7', '8', '9', '11']
        for sch in copy_to_school:
            create_data = []
            with transaction.atomic():
                for bi in base_queryset:
                    tmp_img_paths = bi.img_paths.split(',') if bi.img_paths else ''
                    t_img_paths = []
                    for ii in tmp_img_paths:
                        if not ii:
                            break
                        ini_img = MEDIA_ROOT + ii
                        img_name = '{0:%Y%m%d%H%M%S%f}'.format(datetime.now()) + str(randint(1000000, 9999999)) + '.jpg'
                        tar_img = TAR_IMG_PATH + img_name
                        # shutil.copyfile(ini_img, tar_img)
                        t_img_paths.append('photos/2022-02-15/' + img_name)

                    nick_index = randint(0, len(rand_nickname) - 1)
                    file_index = randint(0, len(files) - 1)
                    nickname = rand_nickname[nick_index]
                    nickname_encoder = base64.b64encode(nickname.encode("utf-8"))
                    nickname = nickname_encoder.decode('utf-8')
                    avatar_url = 'tmp_avatars/' + files[file_index]
                    uid = set_uid()
                    view_count = randint(0, 30)
                    create_data.append(TopicManage(
                        uid=uid,
                        nickname=nickname,
                        avatar_url=avatar_url,
                        title=bi.title,
                        content=bi.content,
                        topic_type=bi.topic_type,
                        school=sch,
                        view_count=view_count,
                        img_paths=','.join(t_img_paths),
                        create_time=random_date(start_time, end_time)
                    ))

                # TopicManage.objects.bulk_create(create_data)

        return Response()

    @action(methods=['POST'], detail=False)
    def update_create_time_view_count(self, request):
        """更新所有帖子的创建时间和浏览量"""
        query = list(TopicManage.objects.all())
        start_time = '2022-01-11 08:00:00'
        end_time = '2022-01-12 02:00:00'
        with transaction.atomic():
            for item in query:
                rand_time = random_date(start_time, end_time)
                # TopicManage.objects.select_for_update().filter(id=item.id).update(create_time=rand_time, view_count=randint(1, 200))

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
        if len(title) > 30 or len(content) > 300:
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
        is_top = request.query_params.get('is_top', None)
        manage_data = request.query_params.get('manage_data', False)

        if manage_data:
            queryset = TopicManage.objects.filter(
                Q(school=school)
                & Q(is_deleted=False)).order_by('-create_time')
        elif is_top:
            queryset = TopicManage.objects.filter(
                Q(school=school)
                & Q(is_top=True)
                & Q(is_deleted=False)).order_by('-create_time')
        elif topic_type:
            queryset = TopicManage.objects.filter(
                Q(school=school)
                & Q(is_top=False)
                & Q(topic_type=topic_type)
                & Q(is_deleted=False)).order_by('-create_time')
        else:
            queryset = TopicManage.objects.filter(
                Q(school=school)
                & Q(is_top=False)
                & Q(is_deleted=False)).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def update_comment_count(self, request):
        with transaction.atomic():
            inst_id = int(request.data.get('inst_id', -1))
            # change_status: up（提升)；down（下降）
            change_status = request.data.get('change_status', None)
            count = int(request.data.get('count', -1))
            queryset = TopicManage.objects.select_for_update().filter(id=inst_id)
            if change_status == 'up' and count >= 0:
                queryset.update(comment_count=count)
            elif change_status == 'down':
                base_comment_count = queryset[0].comment_count
                down_count = base_comment_count - 1 if base_comment_count > 0 else 0
                queryset.update(comment_count=down_count)
            return Response()

    @action(methods=['POST'], detail=False)
    def update_detail(self, request):
        with transaction.atomic():
            school = int(request.data.get('school', -1))
            user_id = str(request.data.get('user_id', '-1'))
            inst_id = int(request.data.get('inst_id', -1))
            view_count = int(request.data.get('view_count', 0))
            change_liker_ids = request.data.get('change_liker_ids', False)
            liker_ids = request.data.get('liker_ids', '')

            ret_info = {}
            update_data = {}
            topic_query = TopicManage.objects.select_for_update().filter(id=inst_id)

            # 点赞量
            if change_liker_ids:
                update_data['liker_ids'] = liker_ids

            # 浏览量
            if view_count:
                ret_info['view_count_status'] = 'plus'
                limit_query = eval(Configuration.objects.get(key='topic_view_count_limit').uni_val)
                is_limit_open = True if limit_query[school][1] == 'open' else False
                if not is_limit_open:
                    update_data['view_count'] = view_count
                else:
                    view_ids = '' if not topic_query[0].view_ids else topic_query[0].view_ids
                    if user_id in view_ids.split(','):
                        ret_info['view_count_status'] = 'original'
                    else:
                        update_data['view_count'] = view_count
                        update_data['view_ids'] = ''.join([view_ids, user_id, ','])

            update_ret = topic_query.update(**update_data)
            ret_info['up_status'] = update_ret
            if update_ret != 1:
                err_msg = '更新帖子数据失败, {data}'.format(data=json.dumps(request.data))
                logger.error(err_msg)
            return Response(ret_info)

    @action(methods=['GET'], detail=False)
    def person_data(self, request):
        uid = request.query_params.get('uid', '')
        queryset = TopicManage.objects.filter(Q(uid=uid) & Q(is_top=False)).order_by('-create_time')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST'], detail=False)
    def del_inst(self, request):
        uid = request.data.get('uid', '')
        inst_id = int(request.data.get('inst_id', 0))
        img_paths = request.data.get('img_paths', [])
        with transaction.atomic():
            TopicManage.objects.select_for_update().filter(Q(id=inst_id) & Q(uid=uid)).delete()
            CommentManage.objects.select_for_update().filter(inst_id=inst_id).delete()
            if img_paths:
                MEDIA_ROOT = settings.MEDIA_ROOT
                try:
                    for path in img_paths:
                        if '.jpg' in path or '.png' in path:
                            img_abs_path = MEDIA_ROOT + path.split('media')[1]
                            os.remove(img_abs_path)
                except:
                    pass
            return Response()

    @action(methods=['POST'], detail=False)
    def soft_del(self, request):
        with transaction.atomic():
            inst_id = int(request.data.get('inst_id', '0'))
            inst_uid = request.data.get('inst_uid', '')
            deleter_uid = request.data.get('deleter_uid', '')
            TopicManage.objects.select_for_update().filter(
                Q(id=inst_id) & Q(uid=inst_uid)
            ).update(is_deleted=True, deleter_uid=deleter_uid)
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
        uid = request.data.get('uid', '')
        inst_id = int(request.data.get('inst_id', 0))
        with transaction.atomic():
            CommentManage.objects.select_for_update().filter(Q(id=inst_id) & Q(uid=uid)).delete()
            return Response()
