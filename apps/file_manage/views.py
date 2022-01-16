from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response

from utils.tencent_sdk import get_sentence_recognition
from .models import ImageFile, AudioFile
from .serializers import ImageFileSerializer, AudioFileSerializer
from .tasks import async_del_audio_info


class ImageFileViewSet(viewsets.ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer
    pagination_class = None

    def get_queryset(self):
        inst_type = self.request.query_params.get('inst_type', '0')
        return ImageFile.objects.filter(inst_type=inst_type)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        img_paths = [settings.DOMAIN + '/media/' + i['file_path'] for i in queryset.values('file_path')]
        return Response(img_paths)


class AudioFileViewSet(viewsets.ModelViewSet):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        audio_path = settings.MEDIA_ROOT + serializer.data['audio_path'].split('/media')[1]
        # audio_path = '/Users/heroking/Documents/convertible_bond/cb_backend/media/zh_1.mp3'
        ret = get_sentence_recognition(audio_path)
        if isinstance(ret, str):
            ret_info = {'info': ret}
        else:
            ret_info = ret
        async_del_audio_info.delay(serializer.data['id'], audio_path)
        return Response(ret_info, status=status.HTTP_201_CREATED)
